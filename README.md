This is a full-stack AI-powered application that allows users to upload PDF documents, process them using Google Gemini, and interact with the contents through conversational Q\&A.
---
*NOTE* -- "This project is working with the versions of Library as mentioned in the requirements.txt and it might not work with other Version. You are free to experiment, but do so at your own discretion."
---

## 🧠 Tech Stack

### Backend

* Python (FastAPI)
* LangChain
* Google Generative AI (Gemini 1.5 Pro)
* FAISS (for vector storage)
* PyPDF2 (PDF text extraction)

### Frontend

* React
* Tailwind CSS
---

## 📁 Project Structure

```
fast/
├── .env                  # Environment variables (must be at the same level as logic.py)
├── .gitignore
├── logic.py              # Core logic for processing PDFs and handling Q&A
├── main.py               # FastAPI server with endpoints
├── requirements.txt      # Backend dependencies
├── uploads/              # (Optional) Directory for storing PDFs
├── __pycache__/          # Python cache
└── frontend/             # React + Tailwind frontend
```

---

## 🔧 Backend Setup

### 1. Clone the repository

```bash
git clone https://github.com/chaurasia7/chatty-pdf
cd fast
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
env\Scripts\activate    # On Windows
# OR
source env/bin/activate  # On Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file (same directory level as `logic.py`)

```
GOOGLE_API_KEY=your_google_generative_ai_key
```

### 5. Run the backend

```bash
uvicorn main:app --reload
```

> FastAPI will start at: `http://127.0.0.1:8000`

---

## 💻 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

> React app will run on: `http://localhost:5173`

---

## 🚀 Usage

1. Upload PDFs via the `/upload` endpoint or the React UI.
2. The server will extract and chunk the text.
3. The vector store is created using Gemini embeddings and saved with FAISS.
4. Ask questions via the `/convo` endpoint or frontend chat UI.
5. Gemini responds using context-aware Q\&A logic.

---

## 🚫 Note

* If you are uploading it to GitHub then `.env` file should **not** be committed to Git. It's included in `.gitignore`.
* Make sure `GOOGLE_API_KEY` is valid and has access to Gemini 1.5 Pro.
* Ensure internet access is enabled when using Google Generative AI services.

---

