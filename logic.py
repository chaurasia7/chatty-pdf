from PyPDF2 import PdfReader
import os
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import io

# Load environment variables from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Extract text from uploaded PDF files
def get_pdf_text(uploaded_files):
    text = ""
    for file in uploaded_files:
        content = file.file.read()                      # Read file content as bytes
        pdf_stream = io.BytesIO(content)                # Wrap bytes in a stream
        pdf_reader = PdfReader(pdf_stream)              # Load into PDF reader

        for page in pdf_reader.pages:
            page_text = page.extract_text()             # Extract text from page
            if page_text:
                text += page_text

    return text

# Split long text into smaller chunks for embeddings
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000            # Custom chunking strategy
    )
    return text_splitter.split_text(text)

# Create and save vector embeddings using FAISS
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",                   # Gemini embedding model
        google_api_key=GOOGLE_API_KEY
    )
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")              # Save locally

# Create a LangChain QA chain with prompt, LLM, and memory
def get_conversational_chain():
    # Define a custom prompt template
    prompt_template = """
    You are an AI assistant. Use the following context to answer the question at the end.
    If the answer is not in the context, say "Answer is not available in the context".
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

    # Initialize memory to retain conversation history
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question",
        return_messages=True
    )

    # Load Gemini model for the QA system
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    # Create the QA chain using 'stuff' method
    chain = load_qa_chain(
        llm=model,
        chain_type="stuff",
        prompt=prompt,
        memory=memory
    )

    return chain

# Run similarity search + invoke LLM to generate a response
def get_response_from_chain(user_question, chain):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    # Load vector index and retrieve relevant chunks
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    # Pass documents and question to chain
    result = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    return result["output_text"]
