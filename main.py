from fastapi import FastAPI, UploadFile, File,Query
from pathlib import Path    
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from logic import (
    get_pdf_text, get_text_chunks, get_vector_store,
    get_conversational_chain, get_response_from_chain,
    
)


app = FastAPI()

origins = [
    "http://localhost:5173",  # React or frontend URL
    "http://127.0.0.1:3000",
    "https://your-frontend.com"  # Production domain
]

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allowed origins
    allow_credentials=True,           # Allow cookies and headers
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)


UPLOAD_DIR = Path("uploads")

@app.get("/")
def home():
    return {"message": "here i am live "}   
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

import traceback

@app.post("/upload")
async def upload(upload_file: list[UploadFile] = File(...)):
    try:
        raw_text = get_pdf_text(upload_file)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)

        return {
            "message": f"{len(upload_file)} PDF(s) uploaded and processed successfully.",
            "files": [f.filename for f in upload_file],
            "raw_text_length": len(raw_text)
        }
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}



qa_chain = get_conversational_chain()

class QuestionRequest(BaseModel):
    question: str

@app.post("/convo")
def ask_question(request: QuestionRequest):
    try:
        answer = get_response_from_chain(request.question, qa_chain)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
