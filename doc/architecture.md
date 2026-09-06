# UdaPlay Architecture Architecture

```
[ User Prompt ] -> [ Streamlit Client ]
                        |
                        v
            [ Agent Orchestrator ]
                        |
        +---------------+---------------+
        |                               |
        v                               v
[ Internal FAISS DB ]        [ Tavily Web Search ]
(Gemini Embeddings)              (Fallback)
        |                               |
        +---------------+---------------+
                        |
                        v
             [ Gemini 2.5 Flash Synthesis ]
                        |
                        v
              [ Response + Telemetry ]
```
