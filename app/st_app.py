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

# Change this line to match your folder structure
from graph.graph import build_graph
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
        opacity: 0.22;
        filter: saturate(1.05) contrast(1.02);
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

            .block-container { padding-top: 1.6rem; padding-bottom: 2.2rem; max-width: 1200px; }
            header[data-testid="stHeader"] { background: rgba(0,0,0,0); }
            #MainMenu { visibility: hidden; }
            footer { visibility: hidden; }

            .eo-card { background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 16px; box-shadow: 0 10px 30px rgba(2, 6, 23, 0.06); }
            .eo-muted { color: var(--muted); }
            .eo-pill { display: inline-block; padding: 6px 10px; border: 1px solid var(--border); border-radius: 999px; background: rgba(255,255,255,0.70); font-size: 0.85rem; }

            div[data-testid="stForm"] { background: rgba(255,255,255,0.88); border: 1px solid var(--border); border-radius: 18px; padding: 16px; box-shadow: 0 10px 30px rgba(2, 6, 23, 0.05); }
            div[data-testid="stStatusWidget"] { border-radius: 16px; }

            /* Sidebar */
            section[data-testid="stSidebar"] { background: rgba(255,255,255,0.78); border-right: 1px solid var(--border); }
            section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }

            /* Suggestion */
            .eo-suggestion { border-left: 6px solid var(--accent); }
            .eo-answer { white-space: pre-wrap; line-height: 1.65; font-size: 1.03rem; unicode-bidi: plaintext; direction: auto; }
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


def _set_example_query() -> None:
    example_value = st.session_state.get("example_query", "")
    if example_value:
        st.session_state["query_text"] = example_value


def _get_map_style(choice: str) -> str | None:
    # Mapbox styles require MAPBOX_API_KEY to be set. Without it, keep default.
    if not os.getenv("MAPBOX_API_KEY"):
        return None
    styles: dict[str, str] = {
        "Dark": "mapbox://styles/mapbox/dark-v11",
        "Light": "mapbox://styles/mapbox/light-v11",
        "Streets": "mapbox://styles/mapbox/streets-v12",
    }
    return styles.get(choice)


with st.sidebar:
    st.markdown("<div class='eo-pill'>El Osta • Options</div>", unsafe_allow_html=True)
    page = st.radio("Menu", ["Trip Planner", "About"], horizontal=False)
    st.caption("Open using `http://localhost:8501` (not `0.0.0.0`).")

    st.markdown("---")
    st.subheader("Quick Inputs")
    st.selectbox(
        "Examples",
        [
            "",
            "عايز اروح من سيدي جابر لمحطة مصر",
            "من سان ستيفانو لبحري",
            "ازاي اروح محطة مصر",
            "بقولك يا صاحبي ازاي اروح من سيدي جابر لسيدي بشر",
            "How can I go from Sidi Gaber to Misr Station?",
        ],
        key="example_query",
        on_change=_set_example_query,
    )

    st.markdown("---")
    st.subheader("Trip Settings")
    walking_cutoff = st.slider("Walking cutoff (m)", min_value=0, max_value=4000, value=1000, step=50)
    max_transfers = st.slider("Max transfers", min_value=0, max_value=6, value=2, step=1)

    st.markdown("---")
    st.subheader("Display")
    show_steps = st.checkbox("Show agent steps", value=True)
    show_raw_state = st.checkbox("Show raw state", value=False)
    show_map = st.checkbox("Show map", value=True)
    map_style_choice = st.selectbox("Map style", ["Dark", "Light", "Streets"], index=0)


if page == "About":
        st.markdown(
                """
                <div class="eo-card">
                    <h2 style="margin: 0;">El Osta RouteAI</h2>
                    <div class="eo-muted" style="margin-top: 8px;">
                        A smart trip-planning assistant powered by a LangGraph workflow:
                        Parse → Geocode → Route → Format.
                    </div>
                    <div class="eo-muted" style="margin-top: 10px;">
                        Tip: If parsing/formatting fails, ensure <b>GOOGLE_API_KEY</b> is set in the .env.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
        )
        st.stop()


st.markdown(
        """
        <div class="eo-card">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
                <div>
                    <h1 style="margin:0;">El Osta: RouteAI</h1>
                    <div class="eo-muted" style="margin-top:6px;">اكتب طلبك بالعربي أو بالإنجليزي — وخلّيني أظبطلك المشوار. | Type it in Arabic or English.</div>
                </div>
                <div style="text-align:right;" class="eo-muted">
                    <div class="eo-pill">Map-first trip planning</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)

st.write("")
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    with st.form("query_form"):
        st.subheader("Your Request")
        user_query = st.text_area(
            "Trip request",
            key="query_text",
            placeholder="مثال: عايز اروح من سيدي جابر لمحطة مصر",
            height=140,
        )
        cta = st.form_submit_button("Plan Route", use_container_width=True)

        st.caption("Tip: Use the sidebar to choose examples and settings.")

if cta and not (user_query or "").strip():
    st.warning("Please enter a trip request.")

if cta and (user_query or "").strip():
    # Prepare initial state based on your AgentState
    initial_state = {
        "query": user_query,
        "walking_cutoff": float(walking_cutoff),
        "max_transfers": int(max_transfers)
    }

    with col2:
        st.subheader("Results")

        # We use stream to capture updates from each node
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
                status.update(label="Couldn’t complete the plan | حصلت مشكلة", state="error", expanded=True)
            else:
                status.update(label="Trip planned | تمام", state="complete", expanded=False)

        st.session_state["last_state"] = final_state
        st.session_state["last_query"] = user_query

        # --- Final Answer Display (Prominent) ---
        if final_state.get("final_answer"):
            st.markdown(
                """
                <div class="eo-card eo-suggestion">
                  <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:12px;">
                    <div>
                      <h3 style="margin:0;">El Osta Suggestion • اقتراح الأُسطى</h3>
                      <div class="eo-muted" style="margin-top:6px;">Mixed Arabic + English text is supported (auto direction).</div>
                    </div>
                  </div>
                  <div class="eo-answer" style="margin-top:10px;">{ANSWER}</div>
                </div>
                """.replace("{ANSWER}", str(final_state["final_answer"]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")),
                unsafe_allow_html=True,
            )

        # --- Map ---
        if show_map and final_state.get("origin_geo") and final_state.get("destination_geo"):
            st.write("")
            st.markdown("### Map • الخريطة")
            try:
                import pydeck as pdk

                o = final_state["origin_geo"]
                d = final_state["destination_geo"]
                origin = {"lat": float(o["lat"]), "lon": float(o["lon"]), "label": "Origin • البداية"}
                dest = {"lat": float(d["lat"]), "lon": float(d["lon"]), "label": "Destination • النهاية"}
                points = pd.DataFrame([origin, dest])
                line = pd.DataFrame(
                    [
                        {
                            "path": [[origin["lon"], origin["lat"]], [dest["lon"], dest["lat"]]],
                            "color": [255, 176, 32],
                        }
                    ]
                )
                view_state = pdk.ViewState(
                    latitude=(origin["lat"] + dest["lat"]) / 2,
                    longitude=(origin["lon"] + dest["lon"]) / 2,
                    zoom=12,
                    pitch=30,
                )
                deck = pdk.Deck(
                    map_style=_get_map_style(map_style_choice),
                    initial_view_state=view_state,
                    tooltip={"text": "{label}"},
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=points,
                            get_position="[lon, lat]",
                            get_fill_color=[0, 184, 159],
                            get_radius=120,
                            pickable=True,
                        ),
                        pdk.Layer(
                            "PathLayer",
                            data=line,
                            get_path="path",
                            get_color="color",
                            width_scale=20,
                            width_min_pixels=2,
                        ),
                    ],
                )
                st.pydeck_chart(deck, use_container_width=True)
            except Exception:
                map_data = pd.DataFrame(
                    [
                        {"lat": final_state["origin_geo"]["lat"], "lon": final_state["origin_geo"]["lon"], "name": "Origin"},
                        {"lat": final_state["destination_geo"]["lat"], "lon": final_state["destination_geo"]["lon"], "name": "Destination"},
                    ]
                )
                st.map(map_data)
        
        if final_state.get("error"):
            st.error(f"Error: {final_state['error']}")

if show_raw_state:
    with st.expander("Raw State"):
        st.json(st.session_state.get("last_state", {}))