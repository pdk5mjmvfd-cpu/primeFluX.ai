"""
Streamlit LCM Real-Time UI - Interactive Apop interface.

Features:
- 3-mode trig split (Research=sin, Refinement=cos, Relations=tan)
- Presence operator (g_PF toggles event spaces)
- 2/5 salts (mod 2/5 phase)
- pi/e secrets (hidden in curvature)
- Discrete shells (local only, no auto-sync)
"""

import streamlit as st
import requests
import json
import math  # For pi/e secrets
from datetime import datetime
import networkx as nx
import plotly.graph_objects as go
import logging

st.set_page_config(page_title="Apop LCM UI", layout="wide")
logger = logging.getLogger(__name__)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "graph" not in st.session_state:
    st.session_state.graph = nx.DiGraph()
if "quanta_minted" not in st.session_state:
    st.session_state.quanta_minted = 0.0
if "node_count" not in st.session_state:
    st.session_state.node_count = 0
if "presence_on" not in st.session_state:
    st.session_state.presence_on = True  # Default on

API_URL = "http://localhost:8000"

# Trig Mode Mapping (user emphasis: mathematical trig for 3 modes)
TRIG_MAP = {
    "research": "sin (Wave Flows)",
    "refinement": "cos (Balance Curvature)",
    "relations": "tan (Projection Spaces)"
}


def presence_operator(phase: float, mode: str, presence_on: bool) -> float:
    """
    Presence operator: g_PF(phase) = trig(mode) if presence_on else 0.
    
    Args:
        phase: Rail phase
        mode: Mode (research/refinement/relations)
        presence_on: Whether presence is enabled
        
    Returns:
        Presence value
    """
    if not presence_on:
        return 0.0
    
    if mode == "research":
        return math.sin(phase)
    elif mode == "refinement":
        return math.cos(phase)
    elif mode == "relations":
        return math.tan(phase)
    else:
        return 0.0


# Sidebar
st.sidebar.title("⚙️ Apop Controls")
mode_label = st.sidebar.radio(
    "📋 Mode (Trig Config)",
    list(TRIG_MAP.keys()),
    format_func=lambda x: TRIG_MAP[x]
)
mode = mode_label.lower()

agent_override = st.sidebar.selectbox(
    "🤖 Agent Salt (Override)",
    ["Auto", "Eidos", "Praxis", "Aegis"]
)
agent_salt = None if agent_override == "Auto" else agent_override.lower()

show_graph = st.sidebar.checkbox("📊 Show Experience Graph", value=True)
st.session_state.presence_on = st.sidebar.checkbox(
    "🕹️ Presence Operator (Event Spaces On/Off)",
    value=st.session_state.presence_on
)
st.sidebar.metric("💎 Quanta Minted (Session)", f"{st.session_state.quanta_minted:.2f}")
st.sidebar.markdown("---")
st.sidebar.info(
    "**FluxAI Runtime**\n"
    "Powered by PrimeFlux. Discrete shells: Local only. 2/5 salts mod phase."
)

# Main UI
st.title("🌀 Apop LCM Interactive")
st.caption(
    f"Running in **{TRIG_MAP[mode]}** | "
    f"Presence: {'On' if st.session_state.presence_on else 'Off'} | "
    f"Connected to {API_URL}"
)

# Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
user_input = st.chat_input("Query the flux...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        st.write("🔄 *Thinking...*")
        
        try:
            # Presence op: If off, skip event spaces (stub output)
            if not st.session_state.presence_on:
                output = "[Event Spaces Off: Presence operator disabled mode trig.]"
                quanta = 0.0
                audit = {"note": "g_PF toggled off", "presence": 0.0}
            else:
                payload = {
                    "input": user_input,
                    "agent_salt": agent_salt,
                    "mode": mode
                }
                response = requests.post(f"{API_URL}/flux/{mode}", json=payload, timeout=30)
                result = response.json()
                
                output = result.get("output", "[No output]")
                quanta = result.get("quanta_minted", 0.0)
                audit = result.get("audit", {})
                
                # Apply presence operator
                phase = audit.get("rail_phase", 0.0)
                presence_value = presence_operator(phase, mode, st.session_state.presence_on)
                audit["presence_value"] = presence_value
                audit["g_PF"] = presence_value
                
                # 2/5 salts: Mod phase
                mod25 = phase % (2 * 5)
                st.sidebar.metric("🔢 2/5 Salt Mod Phase", f"{mod25:.2f}")
                audit["salt_mod_2_5"] = mod25
                
                # pi/e secret curvature (internal, not displayed in UI)
                secret_curv = (math.pi - math.e) * abs(phase)
                logger.debug(f"Secret curvature: {secret_curv:.3f} (pi-e factor)")
                audit["_secret_curvature"] = secret_curv  # Hidden in audit
            
            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
            st.session_state.quanta_minted += quanta
            
            # Graph Update (discrete: local only)
            node_id = st.session_state.node_count
            st.session_state.graph.add_node(
                node_id,
                query=user_input,
                quanta=quanta,
                mode=mode,
                presence=st.session_state.presence_on
            )
            if node_id > 0:
                st.session_state.graph.add_edge(
                    node_id - 1,
                    node_id,
                    quanta=quanta,
                    mode=mode
                )
            st.session_state.node_count += 1
            
            with st.expander("📋 Audit Trail"):
                # Filter out secret curvature from display
                display_audit = {k: v for k, v in audit.items() if not k.startswith("_")}
                st.json(display_audit)
            
            st.rerun()
        
        except Exception as e:
            st.error(f"Error: {e}")
            logger.exception("Error in streamlit UI")

# Graph Viz
if show_graph and len(st.session_state.graph) > 0:
    st.markdown("---")
    st.subheader("📈 Experience Graph (Local Discrete Shell)")
    
    try:
        pos = nx.spring_layout(st.session_state.graph, k=1, iterations=50)
        
        # Extract node data
        node_x = [pos[node][0] for node in st.session_state.graph.nodes()]
        node_y = [pos[node][1] for node in st.session_state.graph.nodes()]
        node_text = [
            f"Query: {st.session_state.graph.nodes[node].get('query', '')[:30]}...<br>"
            f"Quanta: {st.session_state.graph.nodes[node].get('quanta', 0):.2f}"
            for node in st.session_state.graph.nodes()
        ]
        node_colors = [
            st.session_state.graph.nodes[node].get('quanta', 0)
            for node in st.session_state.graph.nodes()
        ]
        
        # Extract edge data
        edge_x = []
        edge_y = []
        for edge in st.session_state.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Create Plotly figure
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                size=10,
                color=node_colors,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Quanta")
            )
        ))
        
        fig.update_layout(
            title="Experience Graph (Discrete Shell - Local Only)",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Graph visualization error: {e}")
        logger.exception("Error in graph visualization")
