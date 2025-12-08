#!/usr/bin/env python3
"""Quick test of workflow API."""

import requests
import json

API_URL = "http://localhost:8000"

print("="*60)
print("Testing PrimeFlux Workflow API")
print("="*60)

# Test 1: Health check
print("\n1. Health Check...")
try:
    response = requests.get(f"{API_URL}/health")
    print(f"✅ API is running: {response.json()}")
except Exception as e:
    print(f"❌ API not responding: {e}")
    print("   Make sure the server is running: python3 api/workflow_api.py")
    exit(1)

# Test 2: Start a workflow
print("\n2. Starting workflow...")
workflow_request = {
    "user_input": "add authentication to my API",
    "target_tools": ["cursor", "grok", "perplexity"]
}

try:
    response = requests.post(
        f"{API_URL}/workflow/start",
        json=workflow_request
    )
    result = response.json()
    print(f"✅ Workflow started!")
    print(f"   Workflow ID: {result['workflow_id']}")
    print(f"   Tools: {list(result['tool_contexts'].keys())}")
    
    workflow_id = result['workflow_id']
    
    # Test 3: Get context for a tool
    print("\n3. Getting context for Cursor...")
    response = requests.get(f"{API_URL}/workflow/{workflow_id}/context/cursor")
    cursor_context = response.json()
    print(f"✅ Cursor context:")
    print(json.dumps(cursor_context, indent=2))
    
    # Test 4: Submit a tool result
    print("\n4. Submitting Cursor result...")
    tool_result = {
        "tool": "cursor",
        "workflow_id": workflow_id,
        "result": {
            "summary": "Created api/auth.py with JWT middleware",
            "files_created": ["api/auth.py", "api/middleware.py"],
            "status": "complete"
        },
        "next_steps": ["Add tests", "Update documentation"]
    }
    response = requests.post(
        f"{API_URL}/workflow/result",
        json=tool_result
    )
    print(f"✅ Result submitted: {response.json()}")
    
    # Test 5: Check workflow state
    print("\n5. Checking workflow state...")
    response = requests.get(f"{API_URL}/workflow/{workflow_id}")
    workflow = response.json()
    print(f"✅ Workflow status: {workflow['status']}")
    print(f"   Tools completed: {list(workflow['tool_results'].keys())}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Test complete!")
print("="*60)
