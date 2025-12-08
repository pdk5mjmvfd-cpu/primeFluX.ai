# runtime/terminal_backend.py
# YOUR PERMANENT BACKEND

from pathlib import Path
import json
import subprocess
import os
from datetime import datetime

class TerminalBackend:
    """
    Terminal backend for ApopToSiS v3.
    
    Manages:
    - Master experience log
    - Memory across sessions
    - Communication with Cursor, Grok, Perplexity
    - Workflow orchestration
    """
    
    def __init__(self):
        """Initialize terminal backend."""
        self.log = Path("experience_log/memory_master.jsonl")
        self.log.parent.mkdir(exist_ok=True)
        if not self.log.exists():
            self.log.write_text("")
    
    def log_entry(self, role: str, content: str, quanta: float = 0.0, metadata: dict = None):
        """
        Log an entry to master memory.
        
        Args:
            role: "user", "assistant", "system"
            content: The content to log
            quanta: QuantaCoin minted (if applicable)
            metadata: Additional metadata
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "quanta_minted": round(quanta, 3),
        }
        if metadata:
            entry.update(metadata)
        
        self.log.write_text(self.log.read_text() + json.dumps(entry) + "\n")
    
    def remember(self, n_lines: int = 20) -> str:
        """
        Load recent memory.
        
        Args:
            n_lines: Number of recent entries to load
            
        Returns:
            Formatted memory string
        """
        content = self.log.read_text().strip()
        if not content:
            return "This is our first conversation."
        
        lines = content.split("\n")[-n_lines:]
        memory_parts = []
        
        for line in lines:
            if line.strip():
                try:
                    entry = json.loads(line)
                    role = entry.get("role", "unknown")
                    content = entry.get("content", "")
                    if content:
                        memory_parts.append(f"[{role}]: {content}")
                except:
                    continue
        
        if not memory_parts:
            return "This is our first conversation."
        
        return "\n".join(memory_parts)
    
    def send_to_cursor(self, task: str):
        """
        Send task to Cursor.
        
        Args:
            task: Task description for Cursor
        """
        print(f"→ Sending to Cursor: {task}")
        self.log_entry("system", f"Task sent to Cursor: {task}")
        # In the future: POST to Cursor API or write to shared file
    
    def send_to_grok(self, question: str):
        """
        Send question to Grok.
        
        Args:
            question: Question for Grok
        """
        print(f"→ Asking Grok: {question}")
        self.log_entry("system", f"Question to Grok: {question}")
        # In the future: POST to Grok API
    
    def send_to_perplexity(self, query: str):
        """
        Send query to Perplexity.
        
        Args:
            query: Search query for Perplexity
        """
        print(f"→ Querying Perplexity: {query}")
        self.log_entry("system", f"Query to Perplexity: {query}")
        # In the future: POST to Perplexity API
    
    def get_stats(self) -> dict:
        """Get backend statistics."""
        content = self.log.read_text().strip()
        if not content:
            return {"total_entries": 0, "total_quanta": 0.0}
        
        lines = content.split("\n")
        total_quanta = sum(
            json.loads(line).get("quanta_minted", 0) 
            for line in lines 
            if line.strip()
        )
        
        return {
            "total_entries": len([l for l in lines if l.strip()]),
            "total_quanta": round(total_quanta, 3)
        }


# Global backend instance
backend = TerminalBackend()
