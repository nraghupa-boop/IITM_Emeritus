from langchain_google_genai import ChatGoogleGenerativeAI
from tools.internal_search import query_internal_games_db
from tools.web_search import search_web_gaming_data
from src.logger import logger

class UdaPlayOrchestrator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.2)

    def run(self, query: str) -> dict:
        """Main execution loop for handling query evaluation and automated fallbacks."""
        logger.info(f"Processing query: '{query}'")
        
        # Step 1: Execute internal vector store search tool
        internal_result = query_internal_games_db.invoke(query)

        # Step 2: Check for valid vector DB documents
        if internal_result not in ["NO_RESULTS_FOUND", "NO_CONFIDENT_RESULTS_FOUND"]:
            logger.info("High-confidence internal match found. Generating response from internal context...")
            prompt = f"Answer the user query based ONLY on this internal context:\n\n{internal_result}\n\nQuery: {query}"
            response = self.llm.invoke(prompt)
            
            return {
                "final_response": f"{response.content}\n\n*Source: Internal Database (FAISS)*",
                "source_type": "Internal Database (FAISS)",
                "context": internal_result
            }

        # Step 3: Trigger DuckDuckGo fallback if internal matches fail
        logger.info("Internal context missing or weak. Triggering DuckDuckGo fallback search...")
        web_result = search_web_gaming_data.invoke(query)

        if web_result and "Web search error" not in web_result:
            prompt = f"Answer the user query using the following web search context:\n\n{web_result}\n\nQuery: {query}"
            response = self.llm.invoke(prompt)
            
            return {
                "final_response": f"{response.content}\n\n*Source: Web Search (DuckDuckGo)*",
                "source_type": "Web Search (DuckDuckGo)",
                "context": web_result
            }

        # Fallback if both searches yield no usable data
        fallback_msg = "I apologize, but I could not find relevant information in either the internal database or via web search."
        return {
            "final_response": fallback_msg,
            "source_type": "None",
            "context": "No context retrieved."
        }

    def route_and_execute(self, query: str) -> dict:
        """Interface method wrapper to support client calls in app.py."""
        return self.run(query)
