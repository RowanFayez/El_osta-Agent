#format.py

from app.services.decode_trips import TripDecoder
from app.services.format_output import format_server_journeys_for_user_llm


def format_node(state: dict) -> dict:
    """
    state متوقع فيه:
    - route_response
    - origin
    - destination
    """

    decoder = TripDecoder()

    route_response = state.get("route_response")
    origin = state.get("origin")
    dest = state.get("destination")

    # 1️⃣ فلترة وترتيب
    best_journeys = decoder.filter_sort(route_response)

    # 2️⃣ decoding
    for j in best_journeys:
        j["readable_path"] = decoder.decode_path(j.get("path", []))

    # 3️⃣ formatting (LLM)
    user_text = format_server_journeys_for_user_llm(
        journeys=best_journeys,
        origin=origin,
        dest=dest
    )

    # 4️⃣ رجوع النتيجة
    return {
        **state,
        "final_answer": user_text
    }
