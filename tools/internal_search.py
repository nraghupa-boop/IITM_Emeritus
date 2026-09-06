from langchain.tools import tool
from src.vectorstore import build_or_load_vectorstore
from src.logger import logger

vectorstore = build_or_load_vectorstore()

@tool
def query_internal_games_db(query: str) -> str:
    """Queries the internal video games database for game details, developers, platforms, and release dates."""
    logger.info(f"Tool Executing: query_internal_games_db with query: '{query}'")
    results = vectorstore.similarity_search_with_score(query, k=2)
    
    if not results:
        return "NO_RESULTS_FOUND"
    
    matched_docs = []
    for doc, score in results:
        # Tightened threshold: FAISS L2 scores above 0.85 represent weak matches
        if score < 0.85:  
            matched_docs.append(doc.page_content)
    
    if not matched_docs:
        return "NO_CONFIDENT_RESULTS_FOUND"
    
    return "\n\n---\n\n".join(matched_docs)
