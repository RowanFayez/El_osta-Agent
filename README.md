# langgraph_ai_agent


    ## Project structure (current)

    - confg.py
    - main.py
    - graph/
        - graph.py
        - state.py
        - nodes/
            - parse.py
            - geocode.py
            - route.py
            - format.py
    - grpc/
        - routing.proto
    - grpc_stubs/
        - routing_pb2.py
        - routing_pb2_grpc.py
    - memory/
    - services/
        - llm.py
        - geocoding_serv.py
        - routing_client.py
        - decode_trips.py
        - format_output.py
    - testings/
        - parse_test.py
        - geo_test.py
        - route_test.py
        - decoding_test.py
        - test_graph.py
        - tempCodeRunnerFile.py
    - __pycache__/ (generated Python bytecode; safe to ignore)

    ## What each file contains (simple)

    - confg.py — basic app configuration (constants, env settings).
    - main.py — entry point; builds and runs the agent/graph.
    - graph/graph.py — defines the LangGraph workflow and node wiring.
    - graph/state.py — shared state model passed between nodes.
    - graph/nodes/parse.py — parses user input into structured fields.
    - graph/nodes/geocode.py — turns locations into coordinates.
    - graph/nodes/route.py — requests routes given waypoints.
    - graph/nodes/format.py — formats final results for output.
    - grpc/routing.proto — gRPC service definition for routing.
    - grpc_stubs/routing_pb2.py — protobuf message classes (generated).
    - grpc_stubs/routing_pb2_grpc.py — gRPC client/server stubs (generated).
    - memory/ — helpers or stores for agent memory (placeholder).
    - services/llm.py — LLM interface (prompting, responses).
    - services/geocoding_serv.py — geocoding service wrapper.
    - services/routing_client.py — gRPC client to the routing service.
    - services/decode_trips.py — decodes encoded trip/route data.
    - services/format_output.py — shapes/cleans the output payload.
    - testings/parse_test.py — tests for input parsing.
    - testings/geo_test.py — tests for geocoding.
    - testings/route_test.py — tests for routing logic.
    - testings/decoding_test.py — tests for trip decoding.
    - testings/test_graph.py — tests for graph execution.
    - testings/tempCodeRunnerFile.py — temporary scratch file (safe to remove).




    # langgraph_ai_agent


    ## Project structure (current)

    - confg.py
    - main.py
    - graph/
    - grpc/
    - grpc_stubs/
    - memory/
    - services/
    - testings/
    - __pycache__/ (generated Python bytecode; safe to ignore)

    ## What each folder contains (simple)

    - graph — LangGraph workflow. Holds the graph definition, shared state, and node implementations for parse, geocode, route, and format steps.
    - grpc — Protobuf definitions for the routing service API used by the agent.
    - grpc_stubs — Auto-generated Python protobuf and gRPC client/server stubs. Regenerate when the proto changes; otherwise do not edit.
    - memory — Placeholder for agent memory helpers or stores. Extend as needed.
    - services — External integrations and utility functions (LLM interface, geocoding, routing client, trip decoding, output formatting).
    - testings — Unit and integration tests for parsing, geocoding, routing, decoding, and graph execution.
    - __pycache__ — Python bytecode cache; ignore or clean.

    Top-level files:
    - confg.py — Runtime configuration (constants, environment variables).
    - main.py — Entry point to build and run the agent pipeline.

    ## Overview

    This agent parses user input, geocodes locations, requests routes via gRPC, and formats results. The workflow is implemented with LangGraph, using modular nodes for each step.

    ## Prerequisites

    - Python 3.10+
    - pip
    - gRPC runtime; protoc only if you plan to regenerate stubs

    ## Setup

    - Create a virtual environment and install dependencies:
        - If you have a requirements file or pyproject, install from it.
        - Typical packages: grpcio, grpcio-tools (for regeneration), protobuf, and your chosen LLM/geocoding SDKs.
    - Configure environment variables or edit confg.py for API keys and endpoints.

    Example:
    ```
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install grpcio grpcio-tools protobuf
    # plus any LLM/geocoding client libs you use
    ```

    ## Running

    - Ensure the routing service is reachable (your gRPC server or external endpoint).
    - Start the agent:
    ```
    python main.py
    ```

    ## Testing

    - Run tests in the testings folder:
    ```
    pytest
    # or
    python -m unittest discover -s testings
    ```

    ## Regenerating gRPC stubs

    If grpc/routing.proto changes, regenerate stubs:
    ```
    python -m grpc_tools.protoc \
        -I grpc \
        --python_out=grpc_stubs \
        --grpc_python_out=grpc_stubs \
        grpc/routing.proto
    ```

    ## Architecture notes

    - Parse → Geocode → Route → Format, coordinated by graph/graph.py and shared via graph/state.py.
    - Services encapsulate external calls to keep nodes focused on data flow.

    ## Configuration

    - Adjust confg.py or environment variables for:
        - LLM provider keys
        - Geocoding API keys
        - Routing gRPC host/port
        - Any model or service tuning parameters

    ## Contributing

    - Open issues for bugs or enhancements.
    - Keep changes small and covered by tests in testings.
    - Run formatting and linters if configured.

    ## License

    - Add a LICENSE file or specify the license here.
    - Ensure third-party service usage complies with their terms.

    ## Troubleshooting

    - Import errors: verify virtual environment and installed packages.
    - gRPC errors: confirm server address matches confg.py and stubs are up to date.
    - Parsing/geocoding failures: check API keys and rate limits.
    - Test failures: run tests with verbose output and inspect logs.