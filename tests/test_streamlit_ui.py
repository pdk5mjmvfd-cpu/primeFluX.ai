"""
Tests for Streamlit UI.
"""

import pytest
from unittest.mock import Mock, patch
import networkx as nx


def test_streamlit_ui_graph_nodes():
    """Test graph node creation."""
    # Mock streamlit session state
    with patch('streamlit.session_state') as mock_session:
        mock_session.graph = nx.DiGraph()
        mock_session.node_count = 0
        
        # Simulate adding nodes
        mock_session.graph.add_node(0, query="test", quanta=10.0, mode="research")
        mock_session.graph.add_node(1, query="test2", quanta=20.0, mode="refinement")
        mock_session.graph.add_edge(0, 1, quanta=15.0)
        
        assert len(mock_session.graph.nodes()) == 2
        assert len(mock_session.graph.edges()) == 1


def test_presence_operator():
    """Test presence operator logic."""
    import math
    from api.streamlit_ui import presence_operator
    
    # Test with presence on
    phase = math.pi / 4
    assert presence_operator(phase, "research", True) == pytest.approx(math.sin(phase))
    assert presence_operator(phase, "refinement", True) == pytest.approx(math.cos(phase))
    assert presence_operator(phase, "relations", True) == pytest.approx(math.tan(phase))
    
    # Test with presence off
    assert presence_operator(phase, "research", False) == 0.0
    assert presence_operator(phase, "refinement", False) == 0.0
    assert presence_operator(phase, "relations", False) == 0.0


def test_trig_mode_mapping():
    """Test trig mode mapping."""
    from api.streamlit_ui import TRIG_MAP
    
    assert "research" in TRIG_MAP
    assert "refinement" in TRIG_MAP
    assert "relations" in TRIG_MAP
    assert "sin" in TRIG_MAP["research"]
    assert "cos" in TRIG_MAP["refinement"]
    assert "tan" in TRIG_MAP["relations"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
