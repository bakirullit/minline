"""
Aiogram-compatible callback router middleware for unpacking and routing Minline callbacks.

Automatically injects payload as keyword argument into handler functions.
Universal handler that routes to specific route handlers.
"""

import logging
from typing import Callable, Dict
from aiogram import types, Router
from aiogram.filters import Filter

from minline.routing.registry import RouteRegistry
from minline.routing.callback_transport import CallbackTransport

logger = logging.getLogger(__name__)


class MinlineCallbackFilter(Filter):
    """
    Filter to identify Minline callbacks by command prefix.
    Used to distinguish Minline callbacks from other aiogram callbacks.
    """
    
    def __init__(self, command: str = "ml"):
        self.command = command
    
    async def __call__(self, query: types.CallbackQuery) -> bool:
        """Check if callback is from Minline"""
        return CallbackTransport.is_minline_callback(query.data, self.command)


class CallbackRouter:
    """
    Aiogram-compatible middleware for unpacking and routing Minline callbacks.
    
    Features:
    - Unpacks tight callback data by fixed positions
    - Routes to specific handlers based on hash lookup
    - Injects payload as keyword argument automatically
    - Comprehensive error handling and logging
    """
    
    def __init__(self, registry: RouteRegistry):
        self.registry = registry
        self.router = Router()
        self._handlers: Dict[str, Callable] = {}
    
    def setup(self):
        """
        Register callback handler with aiogram router.
        Must be called after registry is finalized.
        """
        self.router.callback_query.register(
            self._handle_callback,
            MinlineCallbackFilter()
        )
        logger.info("✓ CallbackRouter setup complete")
    
    async def _handle_callback(self, query: types.CallbackQuery) -> None:
        """
        Universal callback handler that unpacks and routes to specific handlers.
        
        Unpacking process:
        1. Extract command, hash, payload from fixed positions
        2. Lookup handler by hash in registry
        3. Call handler with payload as keyword argument
        4. Answer callback query
        
        Error handling:
        - Unknown hash -> show alert, log warning
        - Handler exception -> show alert, log error
        """
        try:
            # Step 1: Unpack callback by fixed positions
            callback = CallbackTransport.unpack(query.data)
            
            logger.debug(
                f"Unpacked callback: hash={callback.hash_8} "
                f"payload_len={len(callback.payload)}"
            )
            
            # Step 2: Lookup route handler
            entry = self.registry.get_by_hash(callback.hash_8)
            if not entry:
                logger.warning(
                    f"⚠️ Unknown route hash: {callback.hash_8} "
                    f"(callback_data: {query.data[:20]}...)"
                )
                await query.answer("Route not found", show_alert=True)
                return
            
            logger.debug(f"→ Routing callback to {entry.path} (payload: {callback.payload})")
            
            # Step 3: Call handler with payload as keyword argument
            if callback.payload:
                await entry.handler(query, payload=callback.payload)
            else:
                await entry.handler(query)
            
            # Step 4: Answer callback query
            await query.answer()
            
            logger.debug(f"✓ Callback handled successfully: {entry.path}")
        
        except ValueError as e:
            # Callback data structure error
            logger.error(f"❌ Callback unpacking error: {e}")
            await query.answer("Invalid callback format", show_alert=True)
        
        except Exception as e:
            # Handler or other unexpected error
            logger.error(
                f"❌ Callback handler error: {e}",
                exc_info=True
            )
            await query.answer("Error processing request", show_alert=True)
    
    def get_router(self) -> Router:
        """
        Get configured aiogram Router for inclusion in dispatcher.
        
        Returns:
            Configured Router instance
        """
        return self.router
    
    def get_stats(self) -> dict:
        """Get callback router statistics"""
        return {
            "registry_routes": len(self.registry.all_routes()),
            "router_callbacks": len(self.router.callbacks),
        }
