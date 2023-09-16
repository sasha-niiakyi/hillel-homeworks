from typing import AsyncGenerator
import asyncio
import sys
sys.path.append(sys.path[0] + '/..')
from uuid import uuid4, UUID
from typing import List
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from httpx import AsyncClient
import pytest
from sqlalchemy import select

from src.auth.models import User
from src.database import get_async_session
from src.main import app
from src.config import DATABASE_URL_TEST, password_hasher
from src.auth.jwt_utils import create_jwt_token
from src.meet.models import Meeting, Participant
from src.meet.meet_service import MeetingCRUD
from src.meet.schemas import MeetingCreate
from src.auth.models import User
from src.auth.user_service import UserCRUD
from tests.utils import is_valid_uuid
from src.check.models import Purchase
from src.comment.models import Comment


engine_test = create_async_engine(DATABASE_URL_TEST)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session
User.metadata.bind = engine_test

@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Meeting.metadata.create_all)
        await conn.run_sync(Participant.metadata.create_all)
        await conn.run_sync(Purchase.metadata.create_all)
        await conn.run_sync(Comment.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)
        await conn.run_sync(Meeting.metadata.drop_all)
        await conn.run_sync(Participant.metadata.drop_all)
        await conn.run_sync(Purchase.metadata.drop_all)
        await conn.run_sync(Comment.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test", follow_redirects = True) as ac:
        yield ac


def create_test_auth_headers_for_user(email: str):
    access_token = create_jwt_token(email)
    return {"Authorization": f"Bearer {access_token}"}


async def create_users(number: int) -> List[User]:
    users = []
    async with async_session_maker() as session:
        for i in range(number):
            user = User(
                id=uuid4(),
                name=f"Sasha{i}",
                email=f"user{i}@gmail.com",
                last_name=f"Niy{i}",
                hashed_password=password_hasher.hash(f"password{i}"),
            )
            users.append(user)
            session.add(user)
        await session.commit()
    return users


async def get_participants(meeting_id) -> List[User]:
    async with async_session_maker() as session:
        query = select(Participant).where(Participant.meeting_id == meeting_id)
        request_participants = await session.execute(query)
        saved_participants = request_participants.scalars().all()

        #get from db
        result_participants = []
        for participant in saved_participants:
            assert is_valid_uuid(str(participant.id))

            pat_dict = participant.as_dict()
            del pat_dict["id"]
            result_participants.append(pat_dict)

        return result_participants


async def get_expect_participants(meeting_id: UUID, users: List[User]) -> List[User]:
    async with async_session_maker() as session:
        expect_participants = []
        for user in users:
            if user.id == users[0].id:
                expect_participants.append({
                        "user_id": user.id,
                        "meeting_id": UUID(meeting_id),
                        "is_owner": True
                    }
                )
            else:
                expect_participants.append({
                        "user_id": user.id,
                        "meeting_id": UUID(meeting_id),
                        "is_owner": False
                    }
                )

        return expect_participants


async def create_comment():
    users = await create_users(number=2)

    temp_data = {
        "place": "Odesa",
        "datetime": "2023-09-15 20:37",
        "participants": [user.email for user in users[1:]],
    }

    add_data = MeetingCreate(**temp_data)

    async with async_session_maker() as session:
        meeting_worker = MeetingCRUD(session)
        created_meeting_id = await meeting_worker.create_meeting(add_data, users[0].email)
        participants = await meeting_worker.get_participants(created_meeting_id)

        comments = []
        for participant in participants:
            comment = Comment(
                id=uuid4(),
                participant_id=participant.id,
                created_at=datetime.now(),
                comment='hello'
            )
            session.add(comment)
            comments.append(comment)

        await session.commit()

        return comments
