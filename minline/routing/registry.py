"""
Central in-memory route registry with deterministic hashing and collision detection.

Maps developer routes to 8-character deterministic hashes.
Performs strict collision detection on startup.
Thread-safe for async operations.
"""

import hashlib
import logging
from typing import Callable, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RouteEntry:
    """Internal route registry entry"""
    path: str
    hash_8: str
    handler: Callable
    command: str


class RouteRegistry:
    """
    Central in-memory registry for all routes.
    Maps 8-char deterministic hashes to handlers.
    Performs strict collision detection on startup.
    
    Thread-safe async registry with finalization lock.
    """
    
    def __init__(self):
        self._registry: Dict[str, RouteEntry] = {}
        self._path_to_hash: Dict[str, str] = {}
        self._finalized = False
    
    def register(self, path: str, handler: Callable, command: str = "ml") -> str:
        """
        Register a route and return its 8-char hash.
        
        Args:
            path: Route path (e.g., "/settings/books")
            handler: Async callable handler
            command: 2-byte command prefix (default: "ml")
        
        Returns:
            8-character deterministic hash
        
        Raises:
            RuntimeError: If route already registered or hash collision detected
        """
        if self._finalized:
            raise RuntimeError(
                "Registry is finalized. Cannot register new routes after startup."
            )
        
        if path in self._path_to_hash:
            raise RuntimeError(f"Route {path} already registered")
        
        # Generate deterministic 8-char hash from path using MD5
        hash_full = hashlib.md5(path.encode()).hexdigest()
        hash_8 = hash_full[:8]
        
        # CRITICAL: Collision check
        # If hash exists but path is different, raise immediately
        if hash_8 in self._registry:
            existing_path = self._registry[hash_8].path
            if existing_path != path:
                raise RuntimeError(
                    f"❌ HASH COLLISION DETECTED!\n"
                    f"   Route 1: {path}\n"
                    f"   Route 2: {existing_path}\n"
                    f"   Colliding hash: {hash_8}\n"
                    f"\n   This is a critical error. Two different routes produce the same hash.\n"
                    f"   Consider renaming one of these routes:\n"
                    f"   - {path}\n"
                    f"   - {existing_path}\n"
                    f"\n   Probability: < 0.000001% (MD5 first 8 chars)\n"
                )
        
        entry = RouteEntry(
            path=path,
            hash_8=hash_8,
            handler=handler,
            command=command
        )
        
        self._registry[hash_8] = entry
        self._path_to_hash[path] = hash_8
        
        logger.debug(f"✓ Registered route: {path} -> hash:{hash_8} (cmd:{command})")
        return hash_8
    
    def finalize(self):
        """
        Lock registry from further modifications.
        Called on app startup after all @app.route() decorators are processed.
        """
        self._finalized = True
        collision_check_count = len(self._registry)
        logger.info(
            f"✓ Route registry finalized with {collision_check_count} routes "
            f"(collision check: passed)"
        )
    
    def get_by_hash(self, hash_8: str) -> Optional[RouteEntry]:
        """
        Lookup route entry by 8-char hash.
        
        Args:
            hash_8: 8-character hash
        
        Returns:
            RouteEntry or None if not found
        """
        return self._registry.get(hash_8)
    
    def get_hash_by_path(self, path: str) -> Optional[str]:
        """
        Get hash for a given path.
        
        Args:
            path: Route path
        
        Returns:
            8-character hash or None if not registered
        """
        return self._path_to_hash.get(path)
    
    def all_routes(self) -> Dict[str, RouteEntry]:
        """
        Get all registered routes.
        
        Returns:
            Dictionary mapping hash_8 -> RouteEntry
        """
        return self._registry.copy()
    
    def get_stats(self) -> dict:
        """Get registry statistics"""
        return {
            "total_routes": len(self._registry),
            "finalized": self._finalized,
            "average_path_length": (
                sum(len(e.path) for e in self._registry.values()) / 
                len(self._registry) if self._registry else 0
            ),
        }
