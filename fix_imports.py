#!/usr/bin/env python3
"""
Script to fix imports in ApopToSiS to use ApopToSiS.* format.
This is a helper script for the patch.
"""

import re
from pathlib import Path

# Mapping of old import patterns to new ones
IMPORT_REPLACEMENTS = [
    # Core imports
    (r'^from \.icm import', r'from ApopToSiS.core.icm import'),
    (r'^from \.math\.', r'from ApopToSiS.core.math.'),
    (r'^from core\.', r'from ApopToSiS.core.'),
    (r'^import core\.', r'import ApopToSiS.core.'),
    
    # Runtime imports
    (r'^from \.\.state\.state import', r'from ApopToSiS.runtime.state.state import'),
    (r'^from \.\.capsules import', r'from ApopToSiS.runtime.capsules import'),
    (r'^from \.\.context\.context import', r'from ApopToSiS.runtime.context.context import'),
    (r'^from \.\.router\.router import', r'from ApopToSiS.runtime.router.router import'),
    (r'^from \.\.supervisor\.supervisor import', r'from ApopToSiS.runtime.supervisor.supervisor import'),
    (r'^from \.\.distinction\.distinction import', r'from ApopToSiS.runtime.distinction.distinction import'),
    (r'^from \.\.user_safety_risk import', r'from ApopToSiS.runtime.user_safety_risk import'),
    (r'^from runtime\.', r'from ApopToSiS.runtime.'),
    (r'^import runtime\.', r'import ApopToSiS.runtime.'),
    
    # Agent imports
    (r'^from \.\.base\.base_agent import', r'from ApopToSiS.agents.base.base_agent import'),
    (r'^from \.\.eidos\.eidos import', r'from ApopToSiS.agents.eidos.eidos import'),
    (r'^from \.\.praxis\.praxis import', r'from ApopToSiS.agents.praxis.praxis import'),
    (r'^from \.\.aegis\.aegis import', r'from ApopToSiS.agents.aegis.aegis import'),
    (r'^from \.\.registry\.registry import', r'from ApopToSiS.agents.registry.registry import'),
    (r'^from agents\.', r'from ApopToSiS.agents.'),
    (r'^import agents\.', r'import ApopToSiS.agents.'),
    
    # Experience imports
    (r'^from experience\.', r'from ApopToSiS.experience.'),
    (r'^import experience\.', r'import ApopToSiS.experience.'),
    
    # Combinatoric imports
    (r'^from combinatoric\.', r'from ApopToSiS.combinatoric.'),
    (r'^import combinatoric\.', r'import ApopToSiS.combinatoric.'),
    
    # Quanta imports
    (r'^from quanta\.', r'from ApopToSiS.quanta.'),
    (r'^import quanta\.', r'import ApopToSiS.quanta.'),
    
    # API imports
    (r'^from api\.', r'from ApopToSiS.api.'),
    (r'^import api\.', r'import ApopToSiS.api.'),
]

def fix_imports_in_file(filepath: Path) -> bool:
    """Fix imports in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for pattern, replacement in IMPORT_REPLACEMENTS:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # Only write if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Fix imports in all Python files."""
    base_dir = Path(__file__).parent
    
    # Find all Python files
    python_files = list(base_dir.rglob('*.py'))
    
    # Exclude certain directories
    excluded = {'__pycache__', '.git', 'venv', 'env'}
    python_files = [f for f in python_files if not any(ex in str(f) for ex in excluded)]
    
    print(f"Found {len(python_files)} Python files to process...")
    
    fixed_count = 0
    for filepath in python_files:
        if fix_imports_in_file(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files.")

if __name__ == '__main__':
    main()

