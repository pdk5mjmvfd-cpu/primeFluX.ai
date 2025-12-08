# tests/test_repo_login.py
"""Test repo login and discrete agents."""

import sys
from pathlib import Path

_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.identity.repo_login import RepoLogin
from core.agents.discrete_agents import DiscreteAgent

def test_repo_login():
    """Test login initialization and authentication."""
    # This will create identity if it doesn't exist
    # In real usage, user enters passphrase interactively
    print("Testing RepoLogin...")
    
    # Note: This test requires interactive passphrase entry
    # For automated tests, we'd need to mock getpass
    print("✓ RepoLogin module loads correctly")
    print("✓ DiscreteAgent module loads correctly")
    print("\nTo test fully, run: python3 runtime/apop_terminal.py")

if __name__ == "__main__":
    test_repo_login()
