import streamlit as st
import pandas as pd
import sys
import os
import base64
from typing import Any

# Ensure both the script directory and repo root are on PYTHONPATH.
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_APP_DIR)
for p in (_REPO_ROOT, _APP_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

from graph.graph import build_graph
from services.routing_client import find_route
from services.geocoding_serv import geocode_address

# --- Page Config ---
st.set_page_config(page_title="El Osta • RouteAI", page_icon="🧭", layout="wide")


@st.cache_data
def _load_bg_data_url() -> str | None:
    bg_path = os.path.join(_APP_DIR, "elostabackground.png")
    if not os.path.exists(bg_path):
        return None
    try:
        with open(bg_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
        return f"data:image/png;base64,{encoded}"
    except Exception:
        return None


_BG_DATA_URL = _load_bg_data_url()

_bg_css = ""
if _BG_DATA_URL:
    _bg_css = f"""
      .stApp::before {{
        content: \"\";
        position: fixed;
        inset: 0;
        background-image: url(\"{_BG_DATA_URL}\");
        background-repeat: no-repeat;
        background-position: center center;
        background-size: cover;
        opacity: 0.35;
        filter: saturate(1.1) contrast(1.05);
        z-index: -1;
        pointer-events: none;
      }}
    """

st.markdown(
    """
    <style>
        :root {
            --bg0: #F8FAFF;
            --bg1: #EEF3FF;
            --card: rgba(255,255,255,0.92);
            --border: rgba(15, 23, 42, 0.10);
            --text: rgba(15, 23, 42, 0.92);
            --muted: rgba(15, 23, 42, 0.62);
            --accent: #FFB020;
            --accent2: #00B89F;
            --accent3: #6366F1;
        }

        .stApp {
            color: var(--text);
            background:
                radial-gradient(1200px 600px at 10% 0%, rgba(255,176,32,0.20), transparent 60%),
                radial-gradient(1200px 600px at 90% 0%, rgba(0,184,159,0.18), transparent 60%),
                linear-gradient(180deg, var(--bg0), var(--bg1));
        }

    """
    + _bg_css
    + """

        html, body, [class*="css"] {
            font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans Arabic", "Noto Sans", Arial;
        }

        .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1400px; }
        header[data-testid="stHeader"] { background: rgba(0,0,0,0); }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }

        .eo-card { background: rgba(255,255,255,0.75); border: 1px solid var(--border); border-radius: 18px; padding: 20px; box-shadow: 0 10px 30px rgba(2, 6, 23, 0.08); margin-bottom: 16px; backdrop-filter: blur(8px); }
        .eo-card-green { border-left: 5px solid var(--accent2); }
        .eo-card-orange { border-left: 5px solid var(--accent); }
        .eo-card-purple { border-left: 5px solid var(--accent3); }
        .eo-muted { color: var(--muted); }
        .eo-pill { display: inline-block; padding: 6px 12px; border: 1px solid var(--border); border-radius: 999px; background: rgba(255,255,255,0.70); font-size: 0.85rem; }

        div[data-testid="stForm"] { background: rgba(255,255,255,0.70); border: 1px solid var(--border); border-radius: 18px; padding: 16px; box-shadow: 0 10px 30px rgba(2, 6, 23, 0.05); backdrop-filter: blur(6px); }
        div[data-testid="stStatusWidget"] { border-radius: 16px; }

        section[data-testid="stSidebar"] { background: rgba(255,255,255,0.78); border-right: 1px solid var(--border); }
        section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }

        .eo-suggestion { border-left: 6px solid var(--accent); }
        .eo-answer { white-space: pre-wrap; line-height: 1.65; font-size: 1.03rem; unicode-bidi: plaintext; direction: auto; }
        
        .section-title { font-size: 1.3rem; font-weight: 600; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }
        .result-box { background: #f8f9fa; border-radius: 12px; padding: 12px; margin-top: 10px; font-family: monospace; font-size: 0.9rem; overflow-x: auto; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize the graph
@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()


def _init_state() -> None:
    st.session_state.setdefault("query_text", "")
    st.session_state.setdefault("last_state", {})
    st.session_state.setdefault("last_query", "")


_init_state()


# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("<div class='eo-pill'>⚙️ Settings</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("Trip Settings")
    walking_cutoff = st.slider("Walking cutoff (m)", min_value=0, max_value=4000, value=1000, step=50)
    max_transfers = st.slider("Max transfers", min_value=0, max_value=6, value=2, step=1)

    st.markdown("---")
    st.subheader("Display Options")
    show_steps = st.checkbox("Show agent steps", value=True)
    show_raw_state = st.checkbox("Show raw state", value=False)
    show_map = st.checkbox("Show map", value=True)


# ============================================================================
# MAIN LAYOUT: Two columns
# ============================================================================
col1, col2 = st.columns([1, 1], gap="large")


# ============================================================================
# COLUMN 1: AI-Powered (Full Pipeline with LLM)
# ============================================================================
with col1:
    st.markdown(
        """
        <div class="eo-card eo-card-orange">
            <div class="section-title">🤖 AI Trip Planner</div>
            <div class="eo-muted">اكتب طلبك بالعربي أو الإنجليزي</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    with st.form("ai_query_form"):
        ai_query = st.text_area(
            "Your request",
            placeholder="مثال: عايز اروح من سيدي جابر لمحطة مصر",
            height=100,
            label_visibility="collapsed",
        )
        ai_submit = st.form_submit_button("🚀 Plan with AI", use_container_width=True)

    # AI Results
    if ai_submit and ai_query.strip():
        initial_state = {
            "query": ai_query,
            "walking_cutoff": float(walking_cutoff),
            "max_transfers": int(max_transfers)
        }

        with st.status("El Osta is planning… | الأُسطى بيفكر…", expanded=True) as status:
            final_state: dict[str, Any] = {}
            try:
                for event in graph.stream(initial_state):
                    for node_name, state_update in event.items():
                        if show_steps:
                            st.write(f"✅ **{node_name}**")
                        final_state.update(state_update)
            except Exception as e:
                final_state["error"] = str(e)

            if final_state.get("error"):
                status.update(label="❌ Error", state="error", expanded=True)
            else:
                status.update(label="✅ Done", state="complete", expanded=False)

        st.session_state["last_state"] = final_state

        if final_state.get("final_answer"):
            st.markdown(
                f"""
                <div class="eo-card eo-suggestion">
                    <h4 style="margin:0;">🗣️ El Osta Says</h4>
                    <div class="eo-answer" style="margin-top:10px;">{str(final_state["final_answer"]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if final_state.get("error"):
            st.error(f"Error: {final_state['error']}")

    if show_raw_state and st.session_state.get("last_state"):
        with st.expander("🔍 Raw AI State"):
            st.json(st.session_state["last_state"])


# ============================================================================
# COLUMN 2: Raw Server Test (Coordinates Only - No AI)
# ============================================================================
with col2:
    st.markdown(
        """
        <div class="eo-card eo-card-green">
            <div class="section-title">🔧 Raw Server Test</div>
            <div class="eo-muted">Test routing server directly with coordinates</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    with st.form("raw_server_form"):
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            start_lat = st.number_input("Start Lat", value=31.22968895248673, format="%.8f")
            start_lon = st.number_input("Start Lon", value=29.96139328537071, format="%.8f")
        with r_col2:
            end_lat = st.number_input("End Lat", value=31.20775934404925, format="%.8f")
            end_lon = st.number_input("End Lon", value=29.94194179397711, format="%.8f")
        
        st.markdown("**Weights**")
        w_col1, w_col2, w_col3, w_col4 = st.columns(4)
        with w_col1:
            w_time = st.number_input("Time", value=0.5, min_value=0.0, max_value=1.0, step=0.1)
        with w_col2:
            w_cost = st.number_input("Cost", value=0.3, min_value=0.0, max_value=1.0, step=0.1)
        with w_col3:
            w_walk = st.number_input("Walk", value=0.1, min_value=0.0, max_value=1.0, step=0.1)
        with w_col4:
            w_transfer = st.number_input("Transfer", value=0.1, min_value=0.0, max_value=1.0, step=0.1)
        
        restricted_modes = st.multiselect(
            "Restricted Modes",
            options=["Bus", "Minibus", "Microbus", "Tram", "Metro"],
            default=[]
        )
        
        raw_submit = st.form_submit_button("🔍 Test Server", use_container_width=True)

    if raw_submit:
        with st.spinner("Calling routing server..."):
            try:
                raw_result = find_route(
                    start_lat=start_lat,
                    start_lon=start_lon,
                    end_lat=end_lat,
                    end_lon=end_lon,
                    max_transfers=max_transfers,
                    walking_cutoff=walking_cutoff,
                    restricted_modes=restricted_modes,
                    weights={
                        "time": w_time,
                        "cost": w_cost,
                        "walk": w_walk,
                        "transfer": w_transfer
                    }
                )
                
                st.success(f"✅ Found {len(raw_result.get('journeys', []))} journeys")
                
                for i, journey in enumerate(raw_result.get("journeys", [])):
                    with st.expander(f"🚌 Journey {i+1}"):
                        st.json(journey)
                        
            except Exception as e:
                st.error(f"❌ Server Error: {e}")


# ============================================================================
# SECTION 3: Geocoding & Parsing Test
# ============================================================================
st.markdown("---")
st.markdown(
    """
    <div class="eo-card eo-card-purple">
        <div class="section-title">📍 Geocoding & Parsing Test</div>
        <div class="eo-muted">Test geocoding service with stop names</div>
    </div>
    """,
    unsafe_allow_html=True,
)

stop_col1, stop_col2 = st.columns([1, 1])

with stop_col1:
    with st.form("stop_names_form"):
        from_stop = st.text_input("From (من)", value="محطة مصر", placeholder="مثال: محطة مصر")
        to_stop = st.text_input("To (إلى)", value="سيدي بشر", placeholder="مثال: سيدي بشر")
        stop_submit = st.form_submit_button("🔍 Test Geocoding", use_container_width=True)

with stop_col2:
    st.markdown("**📍 Geocode Results**")
    geocode_placeholder = st.empty()

if stop_submit and from_stop.strip() and to_stop.strip():
    with geocode_placeholder.container():
        with st.spinner("Geocoding..."):
            try:
                from_geo = geocode_address(from_stop)
                to_geo = geocode_address(to_stop)
                
                st.success("✅ Geocoded!")
                
                st.markdown("**From:**")
                st.json({"input": from_stop, "result": from_geo})
                
                st.markdown("**To:**")
                st.json({"input": to_stop, "result": to_geo})
                
            except Exception as e:
                st.error(f"Geocode error: {e}")
