from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict, total=False):
    query: str

    origin: Optional[str]
    destination: Optional[str]

    origin_geo: Optional[Dict[str, float]]
    destination_geo: Optional[Dict[str, float]]

    route_response: Optional[Dict[str, Any]]

    final_answer: Optional[str]
    formatted: Optional[str]
    error: Optional[str]

    walking_cutoff: Optional[float]
    max_transfers: Optional[int]

    