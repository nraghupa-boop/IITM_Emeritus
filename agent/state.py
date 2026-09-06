from typing import TypedDict, List

class AgentState(TypedDict):
    query: str
    context: str
    source_type: str
    final_response: str
    logs: List[str]
