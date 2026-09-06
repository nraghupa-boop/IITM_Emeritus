import os
import json
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from src.embeddings import get_gemini_embeddings
from src.logger import logger

INDEX_PATH = "data/faiss_index"
JSON_DATA_PATH = "data/games.json"

def build_or_load_vectorstore():
    embeddings = get_gemini_embeddings()
    
    if os.path.exists(INDEX_PATH):
        logger.info(f"Loading existing FAISS index from {INDEX_PATH}")
        return FAISS.load_local(
            INDEX_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    
    logger.info("FAISS index not found. Building index from dataset...")
    with open(JSON_DATA_PATH, "r", encoding="utf-8") as f:
        games = json.load(f)
    
    docs = []
    for game in games:
        content = f"Title: {game['title']}\nDeveloper: {game['developer']}\nPublisher: {game['publisher']}\nRelease Date: {game['release_date']}\nPlatforms: {', '.join(game['platforms'])}\nDescription: {game['description']}"
        docs.append(Document(page_content=content, metadata={"title": game['title']}))
    
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(INDEX_PATH)
    logger.info(f"FAISS index built and saved successfully to {INDEX_PATH}")
    return vectorstore
