from io import BytesIO
from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile
from db import prisma
from utils import (
    get_conversation_chain,
    get_pdf_text,
    get_text_chunks,
    get_vector_store,
)

app = FastAPI()

vector_store = None


@app.get("/")
def index():
    return {"name": "First Data"}


@app.post("/upload-file")
async def upload_file(
    file: Annotated[UploadFile, File(...)], userId: Annotated[str, Form()]
):
    global vector_store
    vector_store = None

    # text = await get_pdf_text(file)
    # chunks = get_text_chunks(text)
    # vector_store = get_vector_store(chunks)

    try:
        newUser = await prisma.user.create({"userId": userId})
    except Exception as e:
        print("User Already exitsit")

    newChat = await prisma.chat.create(
        {"title": file.filename or "Unknown", "user_Id": userId}
    )
    # await s3.saveToS3(file, userId, newChat.chatId)
    return {
        "chatId": newChat.chatId,
    }


@app.post("/answer-question")
async def answer_question_from_pdf(prompt: Annotated[str, Form()]):
    global vector_store
    conversation_chain = get_conversation_chain(vector_store)
    response = conversation_chain.run(prompt)

    print(response)

    return {response}
