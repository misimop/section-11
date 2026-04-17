#!/usr/bin/env python3
"""
MCP tool: trigger push-workout GitHub Actions workflow
"""
import json
import os
import sys
import urllib.request
import urllib.error

def trigger_push(workouts: list, confirm: bool = False) -> dict:
    token = os.getenv("PUSH_TOKEN")
    repo = os.getenv("GITHUB_REPO", "misimop/section-11")
    
    if not token:
        return {"success": False, "error": "PUSH_TOKEN not set"}
    
    url = f"https://api.github.com/repos/{repo}/actions/workflows/push-workout.yml/dispatches"
    
    payload = json.dumps({
        "ref": "main",
        "inputs": {
            "command": "push",
            "workouts": json.dumps(workouts),
            "confirm": "true" if confirm else "false"
        }
    }).encode()
    
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as resp:
            return {"success": True, "status": resp.status, "message": "Workflow triggered!"}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.read().decode()}"}

if __name__ == "__main__":
    # Test
    result = trigger_push([{
        "name": "Test workout",
        "date": "2026-04-20",
        "type": "Ride",
        "duration_minutes": 60,
        "tss": 50,
        "description": "- 10m ramp 50%-65%\n- 40m 65-75%\n- 10m ramp 65%-50%"
    }], confirm=False)
    print(json.dumps(result, indent=2))
