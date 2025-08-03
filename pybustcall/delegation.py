"""Delegation management - mirrors bustcall/src/delegation.rs"""

import aiohttp
import asyncio
from typing import Dict, Any, List
from .utils.error import BustcallError
from .core.config import BustcallConfig

class DelegationManager:
    """Manages delegation to other services and P2P coordination"""
    
    def __init__(self, config: BustcallConfig):
        self.config = config
        self.known_peers: Dict[str, str] = {}  # binding_type -> endpoint
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def execute_bust(self, target: str, strategy: str, fault_tolerance: int) -> Dict[str, Any]:
        """Execute cache bust with delegation and fault tolerance"""
        
        # Try central daemon first (star topology)
        try:
            return await self._delegate_to_daemon(target, strategy, fault_tolerance)
        except Exception as e:
            # Fallback to P2P resolution (ring topology)
            return await self._p2p_execute_bust(target, strategy, fault_tolerance)
    
    async def _delegate_to_daemon(self, target: str, strategy: str, fault_tolerance: int) -> Dict[str, Any]:
        """Delegate to central Rust daemon"""
        daemon_url = f"http://localhost:{self.config.daemon_port}"
        
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        payload = {
            "target": target,
            "strategy": strategy,
            "binding": "python",
            "fault_tolerance": fault_tolerance
        }
        
        async with self.session.post(f"{daemon_url}/api/v1/bust", json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise BustcallError(f"Daemon delegation failed: {response.status}")
    
    async def _p2p_execute_bust(self, target: str, strategy: str, fault_tolerance: int) -> Dict[str, Any]:
        """Execute via P2P network when daemon unavailable"""
        
        # Discover available peers (gobustcall, luabustcall, etc.)
        available_peers = await self._discover_peers()
        
        if not available_peers:
            raise BustcallError("No peers available for P2P execution")
        
        # Try peers in order of preference
        for peer_endpoint in available_peers:
            try:
                return await self._execute_on_peer(peer_endpoint, target, strategy, fault_tolerance)
            except Exception as e:
                continue  # Try next peer
        
        raise BustcallError("All P2P peers failed")
    
    async def _discover_peers(self) -> List[str]:
        """Discover other bustcall peers on network"""
        # Implement peer discovery protocol
        # Could use multicast, service discovery, or configuration-based
        peers = []
        
        # Check common ports for other language bindings
        potential_peers = [
            "http://localhost:8080",  # gobustcall
            "http://localhost:8082",  # luabustcall  
            "http://localhost:8083",  # other bindings
        ]
        
        for peer in potential_peers:
            try:
                if not self.session:
                    self.session = aiohttp.ClientSession()
                
                async with self.session.get(f"{peer}/api/v1/capabilities", timeout=1) as response:
                    if response.status == 200:
                        peers.append(peer)
            except:
                continue  # Peer not available
        
        return peers
    
    async def _execute_on_peer(self, peer_endpoint: str, target: str, strategy: str, fault_tolerance: int) -> Dict[str, Any]:
        """Execute cache bust on a peer node"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        payload = {
            "target": target,
            "strategy": strategy,
            "binding": "python-p2p",
            "fault_tolerance": fault_tolerance
        }
        
        async with self.session.post(f"{peer_endpoint}/api/v1/bust", json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise BustcallError(f"Peer execution failed: {response.status}")
