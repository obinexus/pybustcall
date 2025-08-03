"""Configuration management for PyBustcall - mirrors bustcall/src/core/config.rs"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class PolyCallConfig:
    """Maps to PolyCall configuration system"""
    server_mappings: Dict[str, str]  # language -> port mapping
    network_timeout: int = 5000
    max_connections: int = 1000
    log_directory: str = "/var/log/polycall"
    workspace_root: str = "/opt/polycall"
    auto_discover: bool = True
    discovery_interval: int = 60
    
    @classmethod
    def from_polycallfile(cls, config_path: str) -> 'PolyCallConfig':
        """Parse config.Polycallfile format"""
        server_mappings = {}
        config_vars = {}
        
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('server '):
                    # Parse: server node 8080:8084
                    parts = line.split()
                    if len(parts) >= 3:
                        lang, port_mapping = parts[1], parts[2]
                        server_mappings[lang] = port_mapping
                elif '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config_vars[key] = value
        
        return cls(
            server_mappings=server_mappings,
            network_timeout=int(config_vars.get('network_timeout', 5000)),
            max_connections=int(config_vars.get('max_connections', 1000)),
            log_directory=config_vars.get('log_directory', '/var/log/polycall'),
            workspace_root=config_vars.get('workspace_root', '/opt/polycall')
        )

@dataclass
class BustcallConfig:
    """Core bustcall configuration"""
    daemon_port: int = 3000
    fault_tolerance_stage: int = 3
    p2p_enabled: bool = True
    hybrid_topology: bool = True
    polycall_config: Optional[PolyCallConfig] = None
