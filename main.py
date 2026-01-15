import uuid
import shutil
import os
import threading
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile

from langchain_community.document_loaders import PyMuPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
import chromadb

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

llm = ChatOllama(model="qwen2.5:7b-instruct", temperature=0.1)
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
client = chromadb.Client()
responses = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting up the FastAPI application")
    os.makedirs("user_files", exist_ok=True)
    yield
    users = os.listdir("user_files")
    for user in users:
        shutil.rmtree(f"user_files/{user}")
    logging.info("Shutting down the FastAPI application")


app = FastAPI(lifespan=lifespan)


@app.get("/id")
async def get_id():
    return {"id": str(uuid.uuid4())}


@app.post("/upload")
async def upload(id: str, files: list[UploadFile] = File(...)):
    os.makedirs(f"user_files/{id}", exist_ok=True)
    logging.info(f"Uploading files for user {id}")
    for file in files:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(f"user_files/{id}", f"{file_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logging.info(f"Saved file {file.filename} as {file_id} for user {id}")
    t = threading.Thread(target=load_data, args=(id,), daemon=True)
    t.start()
    return {"file_upload": True}


@app.post("/answer-query")
async def answer_query(id: str, query: str):
    embedded_query = embeddings.embed_query(query)
    collection = client.get_or_create_collection(name=id)
    results = collection.query(query_embeddings=[embedded_query], n_results=20)
    retrieved_docs = []
    if results["documents"] and results["documents"][0]:
        documents = results["documents"][0]
        metadata = results["metadatas"][0]
        distances = results["distances"][0]
        ids = results["ids"][0]

        for i, (doc_id, document, metadata, distance) in enumerate(
            zip(ids, documents, metadata, distances)
        ):
            similarity_score = 1 - distance

            if similarity_score >= 0.0:
                retrieved_docs.append(
                    {
                        "id": doc_id,
                        "content": document,
                        "metadata": metadata,
                        "similarity_score": similarity_score,
                        "distance": distance,
                        "rank": i + 1,
                    }
                )
    logging.info(
        f"Retrieved {len(retrieved_docs)} documents for query '{query}' and user {id}"
    )
    logging.info(retrieved_docs)
    context = "\n\n".join(doc["content"] for doc in retrieved_docs)
    prompt = f"Use the following context to answer the question:\n\nContext: {context}\n\nQuestion: {query}\n\nAnswer:"
    job_id = str(uuid.uuid4())
    responses[job_id] = {"status": "processing", "response": None}
    t = threading.Thread(target=generate_response, args=(prompt, job_id), daemon=True)
    t.start()
    return {"job_id": job_id}


@app.get("/get-response/{job_id}")
async def get_response(job_id: str):
    if responses[job_id]["status"] == "completed":
        response = responses[job_id]["response"]
        # del responses[job_id]
        return {"response": response}
    else:
        return {"response": "Response not ready yet"}


def load_data(id: str):
    documents = []
    logging.info(f"Loading data for user {id}")
    for file in os.listdir(f"user_files/{id}"):
        if not file.startswith("_"):
            if file.endswith(".pdf"):
                loader = PyMuPDFLoader(os.path.join(f"user_files/{id}", file))
            elif file.endswith(".csv"):
                loader = CSVLoader(os.path.join(f"user_files/{id}", file))
            docs = loader.load()
            for doc in docs:
                doc.metadata["user_id"] = id
                doc.metadata["file_type"] = file.split(".")[-1]
            documents.extend(docs)
            logging.info(f"Loaded {len(docs)} docs from {file} for user {id}")
            os.rename(
                os.path.join(f"user_files/{id}", file),
                os.path.join(f"user_files/{id}", f"_{file}"),
            )
    logging.info(f"Loaded {len(documents)} documents for user {id}")
    chunking_and_embedding(documents, id)


def chunking_and_embedding(documents, id):
    logging.info(f"Starting chunking and embedding for user {id}")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )
    pdf_docs = [doc for doc in documents if doc.metadata["file_type"] == "pdf"]
    logging.info(f"Found {len(pdf_docs)} PDF documents for chunking for user {id}")
    other_docs = [doc for doc in documents if doc.metadata["file_type"] != "pdf"]
    logging.info(f"Found {len(other_docs)} non-PDF documents for user {id}")
    chunks = text_splitter.split_documents(pdf_docs)
    chunks.extend(other_docs)
    logging.info(f"Generated {len(chunks)} chunks for user {id}")
    texts = [chunk.page_content for chunk in chunks]
    embedded_texts = embeddings.embed_documents(texts)
    logging.info(f"Generated embeddings for {len(chunks)} chunks for user {id}")
    store_in_chromadb(chunks, embedded_texts, id)


def store_in_chromadb(chunks, embedded_texts, id):
    logging.info(f"Storing data in ChromaDB for user {id}")
    collection = client.get_or_create_collection(name=id)
    collection.add(
        ids=[str(uuid.uuid4()) for _ in range(len(chunks))],
        documents=[chunk.page_content for chunk in chunks],
        metadatas=[chunk.metadata for chunk in chunks],
        embeddings=embedded_texts,
    )
    logging.info(f"Stored {len(chunks)} chunks in ChromaDB for user {id}")
    logging.info(f"Data processing completed for user {id}")


def generate_response(prompt: str, job_id: str):
    response = llm.invoke(prompt)
    logging.info("Generated response from LLM")
    responses[job_id]["status"] = "completed"
    responses[job_id]["response"] = response.content
