import os
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini for Embeddings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class KnowledgeManager:
    def __init__(self, db_path="christin_knowledge"):
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Using Gemini for high-quality embeddings if key is present
        if GEMINI_API_KEY:
            self.emb_fn = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
                api_key=GEMINI_API_KEY,
                task_type="retrieval_document"
            )
        else:
            self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
            
        self.collection = self.client.get_or_create_collection(
            name="sir_intel", 
            embedding_function=self.emb_fn
        )

    def ingest_file(self, file_path):
        """Extracts text from PDF or Text files and stores them in the vector DB."""
        if not os.path.exists(file_path):
            return f"File {file_path} not found, Sir."

        text = ""
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif file_path.endswith((".txt", ".md", ".py")):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            return "File format not supported for neural indexing, Sir."

        if not text.strip():
            return "File appears to be empty, Sir."

        # Split text into chunks for better retrieval
        chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
        ids = [f"{os.path.basename(file_path)}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": file_path} for _ in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        return f"File '{os.path.basename(file_path)}' has been successfully indexed into your neural knowledge base, Sir."

    def query_knowledge(self, query_text):
        """Queries the vector DB and returns relevant context."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=3
        )
        
        if not results['documents'][0]:
            return None
            
        context = "\n---\n".join(results['documents'][0])
        return context

# Global Instance
knowledge = KnowledgeManager()

if __name__ == "__main__":
    # Test
    print("Initializing Neural Knowledge Base...")
