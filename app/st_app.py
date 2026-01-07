import streamlit as st
import pandas as pd
import sys
import os

# Ensure both the script directory and repo root are on PYTHONPATH.
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_APP_DIR)
for p in (_REPO_ROOT, _APP_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

# Change this line to match your folder structure
from graph.graph import build_graph
# --- Page Config ---
st.set_page_config(page_title="RouteAI Explorer", page_icon="🌐", layout="wide")

# Initialize the graph
@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()

st.title("🌐 RouteAI: Smart Trip Planner")
st.markdown("Enter your trip details in Arabic or English to find the best route.")

# --- Sidebar: Logic Flow Diagram ---
with st.sidebar:
    st.header("Graph Architecture")
    try:
        # Generates a visual representation of your StateGraph
        st.image(graph.get_graph().draw_mermaid_png(), caption="Agent Workflow")
    except Exception:
        st.info("Workflow: Parse → Geocode → Route → Format")

# --- UI Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    with st.form("query_form"):
        user_query = st.text_area("Trip Request:", placeholder="عايزة اروح من سيدي جابر لمحطة مصر")
        
        c1, c2 = st.columns(2)
        walk_limit = c1.number_input("Walking Cutoff (m)", value=1000.0)
        transfers = c2.number_input("Max Transfers", value=2)
        
        submit = st.form_submit_button("Plan Route")

if submit and user_query:
    # Prepare initial state based on your AgentState
    initial_state = {
        "query": user_query,
        "walking_cutoff": walk_limit,
        "max_transfers": transfers
    }

    with col2:
        st.subheader("Processing & Results")
        
        # We use stream to capture updates from each node
        with st.status("Agent is thinking...", expanded=True) as status:
            final_state = {}
            
            for event in graph.stream(initial_state):
                for node_name, state_update in event.items():
                    st.write(f"✅ Completed: **{node_name}**")
                    final_state.update(state_update)
            
            status.update(label="Route Found!", state="complete", expanded=False)

        # --- B. Visualizing Coordinates ---
        if final_state.get("origin_geo") and final_state.get("destination_geo"):
            st.markdown("### 🗺️ Route Map")
            
            # Prepare data for streamlit map
            map_data = pd.DataFrame([
                {"lat": final_state["origin_geo"]["lat"], "lon": final_state["origin_geo"]["lon"], "name": "Origin"},
                {"lat": final_state["destination_geo"]["lat"], "lon": final_state["destination_geo"]["lon"], "name": "Destination"}
            ])
            st.map(map_data)

        # --- Final Answer Display ---
        if final_state.get("final_answer"):
            st.success("### Final Route Suggestion")
            st.write(final_state["final_answer"])
        
        if final_state.get("error"):
            st.error(f"Error: {final_state['error']}")

# --- Details Expander ---
with st.expander("View Raw State Data"):
    st.json(st.session_state.get("last_state", {}))