import sys
sys.path.append(sys.path[0] + "/../..")
from uuid import uuid4, UUID

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from tests.conftest import async_session_maker, create_test_auth_headers_for_user
from tests.conftest import create_users, get_participants, get_expect_participants
from src.config import password_hasher
from src.auth.user_service import UserCRUD
from tests.utils import is_valid_uuid
from src.auth.models import User
from src.auth.schemas import UserRead
from src.meet.models import Meeting
from src.meet.schemas import MeetingCreate, MeetingRead, MeetingUpdate
from src.meet.meet_service import MeetingCRUD


# async def test_create_meeting_auth(async_client: AsyncClient):
# 	users = await create_users(number=2)

# 	expect_data = MeetingCreate(**data)

# 	response = await async_client.post(
# 		"/meetings",
# 		json=data,
# 		headers=create_test_auth_headers_for_user(users[0].email),
# 	)
