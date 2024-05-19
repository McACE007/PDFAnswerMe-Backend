from fastapi.middleware.cors import CORSMiddleware
from db import prisma
from api import app

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv(".env"))

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    try:
        await prisma.connect()
    except Exception as e:
        print("Error", e)


@app.on_event("shutdown")
async def stutdown():
    await prisma.disconnect()
