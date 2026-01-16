#parse.py
import time

from app.services.llm import llm_parse
from app.graph.state import AgentState

def parse_node(state: AgentState) -> AgentState:
    print(f"[PARSE] Starting parse for query: {state.get('query', '')[:50]}")
    start = time.time()
    
    result = llm_parse(state["query"])
    
    print(f"[PARSE] Done in {time.time()-start:.1f}s -> origin={result.get('origin')}, dest={result.get('destination')}")

    state["origin"] = result.get("origin")
    state["destination"] = result.get("destination")

    if not state["origin"] or not state["destination"]:
        state["error"] = "parse_failed"

    return state
