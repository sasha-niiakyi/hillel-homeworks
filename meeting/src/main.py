import sys
sys.path.append(sys.path[0] + '/..')

from fastapi import FastAPI

from src.auth.router import user_router, login_router


app = FastAPI(
	title='Meeting'
)

app.include_router(user_router)
app.include_router(login_router)
