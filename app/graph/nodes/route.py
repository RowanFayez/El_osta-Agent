#route.py
import time

from app.services.routing_client import find_route
from app.graph.state import AgentState


def route_node(state: AgentState) -> AgentState:
    if not state.get("origin_geo") or not state.get("destination_geo"):
        print("[ROUTE] Skipping - no coordinates")
        state["error"] = "missing_coordinates"
        return state

    s = state["origin_geo"]
    e = state["destination_geo"]

    print(f"[ROUTE] Starting route from {s} to {e}")
    start = time.time()

    route_response = find_route(
        start_lat=s["lat"],
        start_lon=s["lon"],
        end_lat=e["lat"],
        end_lon=e["lon"],
        walking_cutoff=state.get("walking_cutoff", 1000.0),
        max_transfers=state.get("max_transfers", 2),
    )

    print(f"[ROUTE] Done in {time.time()-start:.1f}s -> {route_response.get('num_journeys')} journeys")

    if route_response.get("error"):
        state["error"] = "routing_failed"
        print(f"[ROUTE] Error: {route_response.get('error')}")
        return state

    state["route_response"] = route_response
    return state
