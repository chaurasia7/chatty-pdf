from fastapi import FastAPI, UploadFile, File
from pathlib import Path    
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from logic import (
    get_pdf_text, get_text_chunks, get_vector_store,
    get_conversational_chain, get_response_from_chain,
)

import traceback

app = FastAPI()

# Allow cross-origin requests from frontend
origins = [
    "http://localhost:5173",  # Local React frontend
    "http://127.0.0.1:3000",  # Another local frontend
    "https://your-frontend.com"  # Placeholder for production domain
]

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = Path("uploads")  # Directory to store uploads (if needed)

@app.get("/")
def home():
    return {"message": "here i am live"}  # Simple health check



# --Below api call stores the pdf loacally
# @app.post("/upload")
# async def upload(upload_file: list[UploadFile] = File(...)):
#     pdf_paths = []

#     for file in upload_file:
#         try:
#             data = await file.read()
#             save_to = UPLOAD_DIR / file.filename
#             with open(save_to, 'wb') as f:  
#                 f.write(data)
#             pdf_paths.append(str(save_to))  
#         except Exception as e:
#             return {"error": str(e)}

#     raw_text = get_pdf_text(pdf_paths)
#     text_chunks = get_text_chunks(raw_text)
#     get_vector_store(text_chunks)

#     return {
#         "message": f"{len(pdf_paths)} PDF(s) uploaded and processed successfully.",
#         "files": pdf_paths
#     }


# Endpoint to handle PDF upload and vector store creation
@app.post("/upload")
async def upload(upload_file: list[UploadFile] = File(...)):
    try:
        # Extract raw text from uploaded PDFs
        raw_text = get_pdf_text(upload_file)
        # Chunk the text for vector embedding
        text_chunks = get_text_chunks(raw_text)
        # Store embeddings in FAISS index
        get_vector_store(text_chunks)

        return {
            "message": f"{len(upload_file)} PDF(s) uploaded and processed successfully.",
            "files": [f.filename for f in upload_file],
            "raw_text_length": len(raw_text)
        }
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

# Initialize the QA chain (LLM + prompt + optional memory)
qa_chain = get_conversational_chain()

# Define the request schema for asking questions
class QuestionRequest(BaseModel):
    question: str

# Endpoint for asking questions
@app.post("/convo")
def ask_question(request: QuestionRequest):
    try:
        # Get the LLM response using semantic search + chain
        answer = get_response_from_chain(request.question, qa_chain)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
