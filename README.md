# RAG API with LangChain, FastAPI, ChromaDB, and Ollama

This project is a Retrieval-Augmented Generation (RAG) API built with FastAPI. It allows users to upload documents (PDFs, CSVs), automatically chunk and embed them, and then query the data using a Large Language Model (LLM) via Ollama. The system uses ChromaDB for vector storage and retrieval.

## Features
- Upload PDF and CSV files per user
- Automatic chunking (PDFs) and embedding of documents
- Store and retrieve document embeddings using ChromaDB
- Query your data with semantic search and LLM-powered answers
- Async LLM response generation with job polling
- Background processing for file ingestion
- WSL/Linux compatible, Docker-ready

## API Endpoints

### `GET /id`
Get a new unique user ID.
- **Response:** `{ "id": <uuid> }`

### `POST /upload`
Upload one or more files for a user.
- **Params:**
  - `id`: User ID (string, required)
  - `files`: List of files (PDF or CSV)
- **Response:** `{ "file_upload": true }`

### `POST /answer-query`
Ask a question about your uploaded documents.
- **Params:**
  - `id`: User ID (string, required)
  - `query`: Your question (string, required)
- **Response:** `{ "job_id": <job_id> }`

### `GET /get-response/{job_id}`
Poll for the LLM's answer to your query.
- **Response:** `{ "response": <answer or status> }`

## How It Works
1. **Upload:** User uploads files. Files are saved and processed in the background.
2. **Ingestion:** PDFs are chunked, CSVs are loaded row-wise, all are embedded and stored in ChromaDB.
3. **Query:** User submits a question. The API retrieves the most relevant chunks/rows and sends them as context to the LLM.
4. **Async Answer:** LLM response is generated in a background thread. User polls for the answer using the job ID.

## Setup & Requirements
- Python 3.10+
- FastAPI
- ChromaDB
- LangChain
- Ollama (for LLM and embeddings)
- PyMuPDF (for PDF loading)
- Docker (optional, for containerization)

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the API:
```bash
uvicorn main:app --reload
```

## Notes
- All user files are stored in `user_files/{user_id}` and cleaned up on server shutdown.
- Only PDFs are chunked; CSVs are embedded row-wise.

## Example Query
```json
{
  "id": "<user_id>",
  "query": "What is the manufacturer of Cheerios?"
}
```

## License
MIT