#!/bin/bash
# Setup the 'apop' alias for easy access

APOP_PATH="$HOME/PrimeFluxAI/primeFluX.ai"
SHELL_RC="$HOME/.zshrc"

# Check if alias already exists
if grep -q "alias apop=" "$SHELL_RC" 2>/dev/null; then
    echo "⚠️  'apop' alias already exists in $SHELL_RC"
    echo "   Remove it first or edit manually"
else
    # Add alias
    echo "" >> "$SHELL_RC"
    echo "# PrimeFlux AI - ApopToSiS v3" >> "$SHELL_RC"
    echo "alias apop='cd $APOP_PATH && source venv/bin/activate && python3 runtime/offline_llm_bridge.py'" >> "$SHELL_RC"
    echo "✅ Alias 'apop' added to $SHELL_RC"
    echo ""
    echo "Run: source $SHELL_RC"
    echo "Then type: apop"
fi
