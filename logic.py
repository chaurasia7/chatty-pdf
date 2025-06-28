from PyPDF2 import PdfReader
import os
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import io

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def get_pdf_text(uploaded_files) :
    text = ""

    for file in uploaded_files:
        # Read the content as bytes
        content = file.file.read()
        # Wrap it in a BytesIO stream
        pdf_stream = io.BytesIO(content)
        # Use PdfReader
        pdf_reader = PdfReader(pdf_stream)

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    You are an AI assistant. Use the following context to answer the question at the end.
    If the answer is not in the context, say "answer is not available in the context".
    Don't make up answers.\n\n
    Context:\n{context}\n
    Conversation History:\n{chat_history}\n
    Question:\n{question}\n
    Answer:
    """

    prompt = PromptTemplate(
        input_variables=["context", "question", "chat_history"],
        template=prompt_template
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question",
        return_messages=True
    )

    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    chain = load_qa_chain(
        llm=model,
        chain_type="stuff",
        prompt=prompt,
        memory=memory
    )

    return chain

def get_response_from_chain(user_question, chain):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    result = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return result["output_text"]
