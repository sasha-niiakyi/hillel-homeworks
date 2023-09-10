from fastapi import FastAPI
from auth.router import user_router


app = FastAPI(
	title='Meeting'
)

app.include_router(user_router)