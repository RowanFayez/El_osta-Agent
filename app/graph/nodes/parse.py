#parse.py

from app.services.llm import llm_parse
from app.graph.state import AgentState

def parse_node(state: AgentState) -> AgentState:
    result = llm_parse(state["query"])

    state["origin"] = result.get("origin")
    state["destination"] = result.get("destination")

    if not state["origin"] or not state["destination"]:
        state["error"] = "parse_failed"

    return state
