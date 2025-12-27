#geocode.py
from app.services.geocoding_serv import geocode_address
from app.graph.state import AgentState

def geocode_node(state: AgentState) -> AgentState:
    if not state.get("origin") or not state.get("destination"):
        return state

    s = geocode_address(state["origin"]) or {"error": True}
    e = geocode_address(state["destination"]) or {"error": True}

    state["origin_geo"] = None if "error" in s else {"lat": s["lat"], "lon": s["lon"]}
    state["destination_geo"] = None if "error" in e else {"lat": e["lat"], "lon": e["lon"]}

    if state["origin_geo"] is None or state["destination_geo"] is None:
        state["error"] = "geocoding_failed"
        state["final_answer"] = "تعذّر تحديد المواقع. جرّب أسماء أدق."

    return state
