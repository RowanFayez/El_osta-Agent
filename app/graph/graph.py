from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import parse, geocode, route, format

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("parse", parse.parse_node)
    graph.add_node("geocode", geocode.geocode_node)
    graph.add_node("route", route.route_node)
    graph.add_node("format", format.format_node)

    graph.set_entry_point("parse")

    graph.add_edge("parse", "geocode")
    graph.add_edge("geocode", "route")
    graph.add_edge("route", "format")
    graph.add_edge("format", END)

    return graph.compile()
