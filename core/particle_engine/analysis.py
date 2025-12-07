"""
Analysis - Particle simulation analysis and visualization.

Merged from analyze_pf_results.py and analyze_results.py
"""

from __future__ import annotations

import math
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import numpy as np

# Try to import plotly for interactive plots
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from .particle import PFParticle


def analyze_results(simulation_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze simulation results.
    
    Args:
        simulation_result: Simulation result dictionary
        
    Returns:
        Analysis dictionary
    """
    particles = simulation_result.get("particles", [])
    history = simulation_result.get("history", [])
    
    if not particles:
        return {"error": "No particles to analyze"}
    
    # Calculate statistics
    energies = [p.energy for p in particles]
    positions = [p.position for p in particles]
    
    # Position statistics
    x_coords = [pos[0] for pos in positions]
    y_coords = [pos[1] for pos in positions]
    z_coords = [pos[2] for pos in positions]
    
    # Energy statistics
    avg_energy = sum(energies) / len(energies) if energies else 0.0
    max_energy = max(energies) if energies else 0.0
    min_energy = min(energies) if energies else 0.0
    
    # Position spread
    x_spread = max(x_coords) - min(x_coords) if x_coords else 0.0
    y_spread = max(y_coords) - min(y_coords) if y_coords else 0.0
    z_spread = max(z_coords) - min(z_coords) if z_coords else 0.0
    
    # Energy conservation
    energy_conservation = simulation_result.get("energy_conservation", 0.0)
    
    return {
        "particle_count": len(particles),
        "avg_energy": avg_energy,
        "max_energy": max_energy,
        "min_energy": min_energy,
        "energy_spread": max_energy - min_energy,
        "x_spread": x_spread,
        "y_spread": y_spread,
        "z_spread": z_spread,
        "energy_conservation": energy_conservation,
        "history_length": len(history)
    }


def plot_particle_cloud(
    particles: List[PFParticle],
    title: str = "Particle Cloud",
    show_plot: bool = False
) -> Optional[Any]:
    """
    Plot particle cloud visualization.
    
    Args:
        particles: List of particles
        title: Plot title
        show_plot: Whether to show plot immediately
        
    Returns:
        Plot figure (matplotlib or plotly)
    """
    if not particles:
        return None
    
    positions = [p.position for p in particles]
    x_coords = [pos[0] for pos in positions]
    y_coords = [pos[1] for pos in positions]
    z_coords = [pos[2] for pos in positions]
    energies = [p.energy for p in particles]
    
    if PLOTLY_AVAILABLE:
        # Use Plotly for 3D visualization
        fig = go.Figure(data=go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='markers',
            marker=dict(
                size=5,
                color=energies,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Energy")
            ),
            text=[f"Prime: {p.prime}, E: {p.energy:.3f}" for p in particles]
        ))
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z"
            ),
            height=600
        )
        
        if show_plot:
            fig.show()
        
        return fig
    else:
        # Fallback to matplotlib
        try:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            scatter = ax.scatter(
                x_coords, y_coords, z_coords,
                c=energies,
                cmap='viridis',
                s=50
            )
            
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            ax.set_title(title)
            
            plt.colorbar(scatter, ax=ax, label="Energy")
            
            if show_plot:
                plt.show()
            
            return fig
        except Exception:
            # If matplotlib 3D not available, use 2D
            fig, ax = plt.subplots(figsize=(8, 6))
            scatter = ax.scatter(
                x_coords, y_coords,
                c=energies,
                cmap='viridis',
                s=50
            )
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_title(title)
            plt.colorbar(scatter, ax=ax, label="Energy")
            
            if show_plot:
                plt.show()
            
            return fig


def plot_phase_space(
    particles: List[PFParticle],
    title: str = "Phase Space",
    show_plot: bool = False
) -> Optional[Any]:
    """
    Plot phase space visualization.
    
    Args:
        particles: List of particles
        title: Plot title
        show_plot: Whether to show plot immediately
        
    Returns:
        Plot figure
    """
    if not particles:
        return None
    
    positions = [p.position for p in particles]
    momenta = [p.momentum for p in particles]
    
    # 2D phase space (x vs px)
    x_coords = [pos[0] for pos in positions]
    px_coords = [mom[0] for mom in momenta]
    
    try:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(x_coords, px_coords, alpha=0.6)
        ax.set_xlabel("Position (x)")
        ax.set_ylabel("Momentum (px)")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        if show_plot:
            plt.show()
        
        return fig
    except Exception:
        return None
