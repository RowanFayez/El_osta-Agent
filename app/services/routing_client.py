import os
import sys
import grpc
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv


load_dotenv()

# We expect generated stubs to live under `app/grpc_stubs/`.
_STUBS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "grpc_stubs")
if _STUBS_DIR not in sys.path:
    sys.path.insert(0, _STUBS_DIR)
try:
    # Generated code imports sibling modules as top-level (e.g., `import routing_pb2`).
    # Keep `_STUBS_DIR` on sys.path and import directly.
    import routing_pb2  # type: ignore
    import routing_pb2_grpc  # type: ignore
except ImportError as e:
    raise ImportError(
        "gRPC stubs not found. Generate them via: "
        "python -m grpc_tools.protoc -I app/grpc --python_out app/grpc_stubs --grpc_python_out app/grpc_stubs app/grpc/routing.proto"
    ) from e


def _default_routing_addr() -> str:
    # In Docker compose, the server is reachable via service/container name.
    # If user hasn't set ROUTING_SERVER_ADDR, prefer that when running in-container.
    if os.getenv("ROUTING_SERVER_ADDR"):
        return os.environ["ROUTING_SERVER_ADDR"]
    if os.path.exists("/.dockerenv"):
        return "routing_server:50051"
    return "localhost:50051"


def _get_stub():
    channel = grpc.insecure_channel(_default_routing_addr())
    return routing_pb2_grpc.RoutingServiceStub(channel)


def health_check() -> Dict[str, Any]:
    stub = _get_stub()
    try:
        resp = stub.HealthCheck(routing_pb2.HealthRequest())
        return {"status": resp.status, "message": resp.message}
    except Exception as e:
        return {"status": "unreachable", "message": str(e)}


def find_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    walking_cutoff: float = 1000.0,
    max_transfers: int = 2,
    restricted_modes: Optional[List[str]] = None,
    weights: Optional[Dict[str, float]] = None,
    top_k: int = 5,
) -> Dict[str, Any]:
    """Call the remote gRPC FindRoute and return parsed dict."""
    stub = _get_stub()

    routing_weights = None
    if weights is not None:
        routing_weights = routing_pb2.RoutingWeights(
            time=float(weights.get("time", 1.0)),
            cost=float(weights.get("cost", 1.0)),
            walk=float(weights.get("walk", 1.0)),
            transfer=float(weights.get("transfer", 1.0)),
        )

    req = routing_pb2.RouteRequest(
        start_lon=start_lon,
        start_lat=start_lat,
        end_lon=end_lon,
        end_lat=end_lat,
        max_transfers=max_transfers,
        walking_cutoff=walking_cutoff,
        restricted_modes=list(restricted_modes or []),
        weights=routing_weights,
        top_k=int(top_k),
    )
    try:
        resp = stub.FindRoute(req)
    except grpc.RpcError as e:
        code = e.code()
        details = e.details() if hasattr(e, "details") else str(e)

        # The updated server uses NOT_FOUND to indicate "no suitable trips".
        # Treat that as a valid empty response so downstream formatting can say
        # "no journeys" instead of "routing failed".
        if code == grpc.StatusCode.NOT_FOUND:
            return {
                "num_journeys": 0,
                "journeys": [],
                "start_trips_found": 0,
                "end_trips_found": 0,
                "total_routes_found": 0,
                "message": details,
            }

        return {"num_journeys": 0, "journeys": [], "error": details}
    except Exception as e:
        return {"num_journeys": 0, "journeys": [], "error": str(e)}

    if getattr(resp, "error", ""):
        return {
            "num_journeys": 0,
            "journeys": [],
            "error": str(resp.error),
            "start_trips_found": getattr(resp, "start_trips_found", 0),
            "end_trips_found": getattr(resp, "end_trips_found", 0),
            "total_routes_found": getattr(resp, "total_routes_found", 0),
        }

    journeys: List[Dict[str, Any]] = []
    for j in resp.journeys:
        legs: List[Dict[str, Any]] = []
        for leg in j.legs:
            # oneof: walk/trip/transfer
            if leg.HasField("walk"):
                wl = leg.walk
                legs.append(
                    {
                        "type": "walk",
                        "distance_meters": int(wl.distance_meters),
                        "duration_minutes": int(wl.duration_minutes),
                        "path": [{"lon": float(p.lon), "lat": float(p.lat)} for p in wl.path],
                    }
                )
            elif leg.HasField("trip"):
                tl = leg.trip
                # protobuf may expose "from" as "from_" (newer) or via getattr (older)
                from_stop = getattr(tl, "from_", None) or getattr(tl, "from", None)
                to_stop = tl.to
                legs.append(
                    {
                        "type": "trip",
                        "trip_id": str(tl.trip_id),
                        "mode": str(tl.mode),
                        "route_short_name": str(tl.route_short_name),
                        "headsign": str(tl.headsign),
                        "fare": float(tl.fare),
                        "duration_minutes": int(tl.duration_minutes),
                        "from": {
                            "stop_id": int(from_stop.stop_id) if from_stop else 0,
                            "name": str(from_stop.name) if from_stop else "",
                            "coord": {"lon": float(from_stop.coord.lon), "lat": float(from_stop.coord.lat)} if from_stop else {"lon": 0, "lat": 0},
                        },
                        "to": {
                            "stop_id": int(to_stop.stop_id) if to_stop else 0,
                            "name": str(to_stop.name) if to_stop else "",
                            "coord": {"lon": float(to_stop.coord.lon), "lat": float(to_stop.coord.lat)} if to_stop else {"lon": 0, "lat": 0},
                        },
                        "path": [{"lon": float(p.lon), "lat": float(p.lat)} for p in tl.path],
                    }
                )
            elif leg.HasField("transfer"):
                tr = leg.transfer
                legs.append(
                    {
                        "type": "transfer",
                        "from_trip_id": str(tr.from_trip_id),
                        "to_trip_id": str(tr.to_trip_id),
                        "from_trip_name": str(tr.from_trip_name),
                        "to_trip_name": str(tr.to_trip_name),
                        "walking_distance_meters": int(tr.walking_distance_meters),
                        "duration_minutes": int(tr.duration_minutes),
                        "path": [{"lon": float(p.lon), "lat": float(p.lat)} for p in tr.path],
                    }
                )

        summary = getattr(j, "summary", None)
        journeys.append(
            {
                "id": int(getattr(j, "id", 0)),
                "text_summary": str(getattr(j, "text_summary", "")),
                "summary": {
                    "total_time_minutes": int(getattr(summary, "total_time_minutes", 0)) if summary else 0,
                    "total_distance_meters": int(getattr(summary, "total_distance_meters", 0)) if summary else 0,
                    "walking_distance_meters": int(getattr(summary, "walking_distance_meters", 0)) if summary else 0,
                    "transfers": int(getattr(summary, "transfers", 0)) if summary else 0,
                    "cost": float(getattr(summary, "cost", 0.0)) if summary else 0.0,
                    "modes": list(getattr(summary, "modes", [])) if summary else [],
                },
                "legs": legs,
            }
        )

    return {
        "num_journeys": resp.num_journeys,
        "journeys": journeys,
        "start_trips_found": resp.start_trips_found,
        "end_trips_found": resp.end_trips_found,
        "total_routes_found": getattr(resp, "total_routes_found", 0),
    }
