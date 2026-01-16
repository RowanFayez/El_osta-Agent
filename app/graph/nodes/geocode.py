#geocode.py
import time

from app.services.geocoding_serv import geocode_address
from app.graph.state import AgentState

def geocode_node(state: AgentState) -> AgentState:
    if not state.get("origin") or not state.get("destination"):
        print("[GEOCODE] Skipping - no origin/destination")
        return state

    print(f"[GEOCODE] Starting geocode for: {state.get('origin')} -> {state.get('destination')}")
    start = time.time()
    
    s = geocode_address(state["origin"]) or {"error": True}
    print(f"[GEOCODE] Origin done in {time.time()-start:.1f}s: {s}")
    
    e = geocode_address(state["destination"]) or {"error": True}
    print(f"[GEOCODE] Destination done in {time.time()-start:.1f}s: {e}")

    state["origin_geo"] = None if "error" in s else {"lat": s["lat"], "lon": s["lon"]}
    state["destination_geo"] = None if "error" in e else {"lat": e["lat"], "lon": e["lon"]}

    if state["origin_geo"] is None or state["destination_geo"] is None:
        state["error"] = "geocoding_failed"
        state["final_answer"] = "تعذّر تحديد المواقع. جرّب أسماء أدق."

    print(f"[GEOCODE] Complete in {time.time()-start:.1f}s")
    return state
