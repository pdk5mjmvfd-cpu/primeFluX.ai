"""
Experience Graph — graph representation of experiences.

Nodes:
- shells
- triplets
- objects
- habits
- skills
- shortcuts

Edges:
- flux
- curvature
- entropy change
- collapse
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path


@dataclass
class GraphNode:
    """A node in the experience graph."""
    node_id: str
    node_type: str  # shell, triplet, object, habit, skill, shortcut
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    """An edge in the experience graph."""
    source_id: str
    target_id: str
    edge_type: str  # flux, curvature, entropy_change, collapse
    weight: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


class ExperienceGraph:
    """
    Graph representation of experiences, transitions, dualities, and clusters.
    
    This gives a persistent experience graph per user.
    """

    def __init__(self, repo_path: str = ".") -> None:
        """
        Initialize ExperienceGraph.

        Args:
            repo_path: Path to repository
        """
        self.repo_path = Path(repo_path)
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []
        self._load_graph()

    def add_node(
        self,
        node_id: str,
        node_type: str,
        data: dict[str, Any] | None = None
    ) -> None:
        """
        Add a node to the graph.

        Args:
            node_id: Node identifier
            node_type: Type of node
            data: Optional node data
        """
        if node_id not in self.nodes:
            self.nodes[node_id] = GraphNode(
                node_id=node_id,
                node_type=node_type,
                data=data or {}
            )

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: str,
        weight: float = 1.0,
        metadata: dict[str, Any] | None = None
    ) -> None:
        """
        Add an edge to the graph.

        Args:
            source_id: Source node ID
            target_id: Target node ID
            edge_type: Type of edge
            weight: Edge weight
            metadata: Optional edge metadata
        """
        # Ensure nodes exist
        if source_id not in self.nodes:
            self.add_node(source_id, "unknown")
        if target_id not in self.nodes:
            self.add_node(target_id, "unknown")
        
        edge = GraphEdge(
            source_id=source_id,
            target_id=target_id,
            edge_type=edge_type,
            weight=weight,
            metadata=metadata or {}
        )
        self.edges.append(edge)

    def update_from_experience(
        self,
        habits: dict[str, Any],
        shortcuts: dict[str, Any],
        objects: dict[str, Any],
        skills: dict[str, Any]
    ) -> None:
        """
        Update graph from experience data.

        Args:
            habits: Dictionary of habits
            shortcuts: Dictionary of shortcuts
            objects: Dictionary of objects
            skills: Dictionary of skills
        """
        # Add habit nodes
        for habit_id, habit in habits.items():
            self.add_node(f"habit_{habit_id}", "habit", habit)
        
        # Add shortcut nodes
        for shortcut_id, shortcut in shortcuts.items():
            self.add_node(f"shortcut_{shortcut_id}", "shortcut", shortcut)
            
            # Add edges from shell sequence
            if "shell_sequence" in shortcut:
                seq = shortcut["shell_sequence"]
                for i in range(len(seq) - 1):
                    self.add_edge(
                        f"shell_{seq[i]}",
                        f"shell_{seq[i+1]}",
                        "flux",
                        weight=shortcut.get("count", 1)
                    )
        
        # Add object nodes
        for object_id, obj in objects.items():
            self.add_node(f"object_{object_id}", "object", obj)
        
        # Add skill nodes
        for skill_id, skill in skills.items():
            self.add_node(f"skill_{skill_id}", "skill", skill)
            
            # Add edges from skill components
            if "habits_used" in skill:
                for habit_id in skill["habits_used"]:
                    self.add_edge(
                        f"skill_{skill_id}",
                        f"habit_{habit_id}",
                        "uses",
                        weight=1.0
                    )
            
            if "shortcuts_used" in skill:
                for shortcut_id in skill["shortcuts_used"]:
                    self.add_edge(
                        f"skill_{skill_id}",
                        f"shortcut_{shortcut_id}",
                        "uses",
                        weight=1.0
                    )

    def save_to_repo(self) -> None:
        """
        Save graph to repository.
        """
        graph_dir = self.repo_path / "experience"
        graph_dir.mkdir(parents=True, exist_ok=True)
        
        graph_file = graph_dir / "experience_graph.json"
        
        graph_data = {
            "nodes": {
                node_id: {
                    "node_id": node.node_id,
                    "node_type": node.node_type,
                    "data": node.data,
                }
                for node_id, node in self.nodes.items()
            },
            "edges": [
                {
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                    "edge_type": edge.edge_type,
                    "weight": edge.weight,
                    "metadata": edge.metadata,
                }
                for edge in self.edges
            ],
        }
        
        with open(graph_file, 'w') as f:
            json.dump(graph_data, f, indent=2)

    def _load_graph(self) -> None:
        """
        Load graph from repository.
        """
        graph_file = self.repo_path / "experience" / "experience_graph.json"
        
        if not graph_file.exists():
            return
        
        try:
            with open(graph_file, 'r') as f:
                graph_data = json.load(f)
            
            # Load nodes
            for node_id, node_data in graph_data.get("nodes", {}).items():
                self.nodes[node_id] = GraphNode(
                    node_id=node_data["node_id"],
                    node_type=node_data["node_type"],
                    data=node_data.get("data", {})
                )
            
            # Load edges
            for edge_data in graph_data.get("edges", []):
                self.edges.append(GraphEdge(
                    source_id=edge_data["source_id"],
                    target_id=edge_data["target_id"],
                    edge_type=edge_data["edge_type"],
                    weight=edge_data.get("weight", 1.0),
                    metadata=edge_data.get("metadata", {}),
                ))
        except Exception as e:
            print(f"Error loading graph: {e}")
    
    def update_from_capsule(self, capsule: Any, state: Any) -> None:
        """
        Update experience graph from capsule and state.
        
        PF Logic: Edges correspond to distinction flow, the core of PF's combinatoric manifold.
        
        Args:
            capsule: Capsule
            state: PF state
        """
        if not hasattr(capsule, 'raw_tokens'):
            return
        
        tokens = capsule.raw_tokens
        
        # Create nodes
        for token in tokens:
            node_id = f"token_{token}"
            if node_id not in self.nodes:
                self.add_node(node_id, "token", {"token": token, "count": 0})
            
            # Update count
            if node_id in self.nodes:
                self.nodes[node_id].data["count"] = self.nodes[node_id].data.get("count", 0) + 1
        
        # Create edges between consecutive tokens (distinction flow)
        for i in range(len(tokens) - 1):
            a, b = tokens[i], tokens[i + 1]
            source_id = f"token_{a}"
            target_id = f"token_{b}"
            
            # Add edge (distinction flow)
            self.add_edge(
                source_id,
                target_id,
                "distinction_flow",
                weight=1.0,
                metadata={"curvature": state.curvature if hasattr(state, 'curvature') else 0.0}
            )
    
    def summary(self) -> dict[str, Any]:
        """
        Get experience graph summary.
        
        Returns:
            Dictionary with nodes and edges
        """
        return {
            "nodes": {
                node_id: {
                    "node_id": node.node_id,
                    "node_type": node.node_type,
                    "data": node.data,
                }
                for node_id, node in self.nodes.items()
            },
            "edges": [
                {
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                    "edge_type": edge.edge_type,
                    "weight": edge.weight,
                }
                for edge in self.edges
            ],
        }

