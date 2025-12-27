#route.py

from app.services.routing_client import find_route
from app.graph.state import AgentState


def route_node(state: AgentState) -> AgentState:
    if not state.get("origin_geo") or not state.get("destination_geo"):
        state["error"] = "missing_coordinates"
        return state

    s = state["origin_geo"]
    e = state["destination_geo"]

    route_response = find_route(
        start_lat=s["lat"],
        start_lon=s["lon"],
        end_lat=e["lat"],
        end_lon=e["lon"],
        walking_cutoff=state.get("walking_cutoff", 1000.0),
        max_transfers=state.get("max_transfers", 2),
    )

    if "error" in route_response:
        state["error"] = "routing_failed"
        return state

    state["route_response"] = route_response
    return state
