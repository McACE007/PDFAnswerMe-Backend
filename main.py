import os
from fastapi import FastAPI, UploadFile
from dotenv import find_dotenv, load_dotenv
from fastapi.middleware.cors import CORSMiddleware

import boto3


load_dotenv(find_dotenv(".env"))

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

app = FastAPI()

app.add_middleware(CORSMiddleware)


@app.get("/")
def index():
    return {"name": "First Data"}


@app.post("/upload-file")
async def upload_file(file: UploadFile):
    print(file)
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, file.filename)

    return {"message": "File uploaded succefully"}
