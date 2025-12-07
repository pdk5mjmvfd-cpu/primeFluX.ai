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
import logging

# Plotly for visualization
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    go = None

# Matplotlib fallback
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None

# Particle engine imports
try:
    from core.particle_engine.simulator import ParticleSimulator
    from core.particle_engine.particle import PFParticle
    from core.particle_engine.analysis import analyze_results, plot_particle_cloud, plot_phase_space
    PARTICLE_ENGINE_AVAILABLE = True
except ImportError:
    PARTICLE_ENGINE_AVAILABLE = False
    ParticleSimulator = None
    PFParticle = None

# Check for plotly
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

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

# Main UI with tabs
tab1, tab2 = st.tabs(["🌀 LCM Chat", "🔬 Particle Lab"])

with tab1:
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

with tab2:
    st.title("🔬 Particle Lab")
    st.caption("PrimeFlux particle physics simulation")
    
    if not PARTICLE_ENGINE_AVAILABLE:
        st.warning("Particle engine not available. Install dependencies.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            num_particles = st.number_input("Number of Particles", min_value=1, max_value=100, value=10)
        
        with col2:
            prime_p = st.number_input("Prime p", min_value=2, max_value=97, value=7, step=2)
        
        with col3:
            steps = st.number_input("Simulation Steps", min_value=10, max_value=1000, value=100, step=10)
        
        # Mode selector for trig
        sim_mode = st.selectbox(
            "Simulation Mode (Trig)",
            ["research", "refinement", "relations"],
            format_func=lambda x: TRIG_MAP.get(x, x),
            index=1
        )
        
        sim_presence = st.checkbox("Presence Operator On", value=True)
        
        if st.button("Run Simulation", type="primary"):
            with st.spinner("Running particle simulation..."):
                try:
                    # Create simulator
                    simulator = ParticleSimulator(
                        mode=sim_mode,
                        presence_on=sim_presence
                    )
                    
                    # Run simulation
                    result = simulator.run_simulation(
                        prime=int(prime_p),
                        steps=int(steps),
                        dt=0.01,
                        curvature=1.0
                    )
                    
                    # Display results
                    st.success(f"Simulation complete: {result['particle_count']} particles, {result['steps']} steps")
                    
                    # Statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Initial Energy", f"{result['initial_energy']:.3f}")
                    with col2:
                        st.metric("Final Energy", f"{result['final_energy']:.3f}")
                    with col3:
                        st.metric("Conservation", f"{1.0 - result['energy_conservation']:.4f}")
                    
                    # Get particles for visualization
                    particles = simulator.get_particles()
                    
                    if particles:
                        # Plot particle cloud
                        st.subheader("Particle Cloud Visualization")
                        fig = plot_particle_cloud(
                            particles,
                            title=f"Particle Cloud (Prime {prime_p}, Mode: {sim_mode})",
                            show_plot=False
                        )
                        if fig:
                            if PLOTLY_AVAILABLE:
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.pyplot(fig)
                        
                        # Phase space plot
                        st.subheader("Phase Space")
                        phase_fig = plot_phase_space(
                            particles,
                            title="Phase Space (x vs px)",
                            show_plot=False
                        )
                        if phase_fig and MATPLOTLIB_AVAILABLE:
                            st.pyplot(phase_fig)
                        
                        # Analysis
                        analysis = analyze_results(result)
                        with st.expander("📊 Analysis"):
                            st.json(analysis)
                    
                    # Stream log
                    st.subheader("Simulation Log")
                    log_text = f"""
**Simulation Parameters:**
- Prime: {prime_p}
- Steps: {steps}
- Mode: {sim_mode} ({TRIG_MAP.get(sim_mode, sim_mode)})
- Presence: {'On' if sim_presence else 'Off'}
- Particles: {result['particle_count']}

**Results:**
- Energy Conservation: {1.0 - result['energy_conservation']:.4f}
- History Points: {len(result.get('history', []))}
"""
                    st.markdown(log_text)
                    
                except Exception as e:
                    st.error(f"Simulation error: {e}")
                    logger.exception("Error in particle simulation")
