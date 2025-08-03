import json
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class BustResult:
    success: bool
    cache_key: str
    execution_time_ms: int
    fault_stage: int

class BustcallClient:
    def __init__(self, daemon_url: str = "http://localhost:3000"):
        self.daemon_url = daemon_url
        self.session = requests.Session()
    
    def bust_cache(self, target: str, strategy: str = "dimensional") -> BustResult:
        """Execute cache bust operation via daemon."""
        payload = {
            "target": target,
            "strategy": strategy,
            "binding": "python"
        }
        
        response = self.session.post(
            f"{self.daemon_url}/api/v1/bust",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return BustResult(
                success=True,
                cache_key=data.get("cache_key", ""),
                execution_time_ms=data.get("execution_time_ms", 0),
                fault_stage=data.get("fault_stage", 0)
            )
        else:
            return BustResult(success=False, cache_key="", execution_time_ms=0, fault_stage=12)
    
    def get_status(self) -> Dict:
        """Get daemon status and health information."""
        response = self.session.get(f"{self.daemon_url}/api/v1/status")
        return response.json() if response.status_code == 200 else {}
