# UdaPlay - AI Gaming Analytics Research Agent

UdaPlay is an intelligent agent architecture that provides video game intelligence using Google Gemini, FAISS, and Tavily Web Search.

## Tech Stack
- **Framework**: LangChain
- **LLM & Embeddings**: Google Gemini (`gemini-2.5-flash`, `text-embedding-004`)
- **Vector Database**: FAISS
- **Evaluation**: DeepEval (Faithfulness, Completeness, Correctness)
- **Web Search**: Tavily API
- **UI**: Streamlit (Python)

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set `.env` file credentials:
   ```env
   GEMINI_API_KEY="your_key"
   TAVILY_API_KEY="your_key"
   ```
3. Run Streamlit Chat Interface:
   ```bash
   streamlit run client/app.py
   ```
4. Run DeepEval Suite:
   ```bash
   python -m eval.run_eval
   ```
