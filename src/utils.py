from io import BytesIO
import os
from dotenv import find_dotenv, load_dotenv
import boto3
from fastapi import File, UploadFile
from fitz import open as pdf_open
from langchain.chains import question_answering
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from transformers import AutoModelForSeq2SeqLM

load_dotenv(find_dotenv(".env"))

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")


s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


# AWS S3 Functions
async def saveToS3(file, userId, chatId):
    s3_client.upload_fileobj(
        file.file, S3_BUCKET_NAME, f"{userId}/{chatId}/{file.filename}"
    )


# Fucntion for converting given UploadFile type file to text
async def get_pdf_text(pdf_doc: UploadFile):
    pdf_content = await pdf_doc.read()
    pdf_stream = BytesIO(pdf_content)

    with pdf_open(stream=pdf_stream) as doc:
        raw_text = ""
    for page in doc:
        raw_text += page.get_text()

    return raw_text


# Function for creating chunks from this text
def get_text_chunks(text: str):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks


# Function for creating a vector store
def get_vector_store(text_chunks):
    embeddings = HuggingFaceEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    return vector_store


def get_conversation_chain(vector_store):
    client = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-xl")
    llm = HuggingFaceEndpoint(
        client, model_kwargs={"temperature": 0, "max_length": 512}
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vector_store.as_retriever(), memory=memory
    )
    return conversation_chain
