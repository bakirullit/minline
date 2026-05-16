import logging
from typing import Optional
from aiogram.types import InlineKeyboardButton

logger = logging.getLogger(__name__)


class Button:
    """
    Minline button with support for tight callback packing.
    
    Attributes:
        text: Button display text
        callback: Custom callback data (max 64 bytes)
        url: URL button (no callback packing)
        route: Route path for tight-packed callbacks (requires registry)
        payload: User payload embedded in callback (max 54 bytes)
    """
    
    def __init__(
        self,
        text: str,
        callback: str = None,
        url: str = None,
        route: str = None,
        payload: str = ""
    ):
        self.text = text
        self.callback = callback
        self.url = url
        self.route = route
        self.payload = payload
    
    def render(self, registry=None):
        """
        Render button as aiogram InlineKeyboardButton.
        
        Args:
            registry: RouteRegistry instance (required if route is used)
        
        Returns:
            InlineKeyboardButton
        
        Raises:
            ValueError: If callback exceeds size limits or route not registered
        """
        # URL button (no packing)
        if self.url:
            return InlineKeyboardButton(text=self.text, url=self.url)
        
        # Route button with tight packing using CallbackTransport
        if self.route:
            if not registry:
                raise ValueError(
                    "registry is required to render route buttons. "
                    "Pass registry=app.route_registry to button.render()"
                )
            
            hash_8 = registry.get_hash_by_path(self.route)
            if not hash_8:
                raise ValueError(f"Route {self.route} not registered")
            
            # Import here to avoid circular dependency
            from minline.routing.callback_transport import CallbackTransport
            
            # Pack callback with payload using tight layout
            callback_data = CallbackTransport.pack(
                command="ml",
                hash_8=hash_8,
                payload=self.payload
            )
            
            size_info = CallbackTransport.get_size_info(callback_data)
            logger.debug(
                f"Rendered route button: '{self.text}' -> {self.route} "
                f"(payload: {self.payload}, size: {size_info['total_bytes']}/{size_info['max_bytes']} bytes)"
            )
            
            return InlineKeyboardButton(text=self.text, callback_data=callback_data)
        
        # Custom callback button
        if self.callback:
            if len(self.callback.encode()) > 64:
                raise ValueError(
                    f"callback_data exceeds 64 bytes: {len(self.callback.encode())} bytes"
                )
            return InlineKeyboardButton(text=self.text, callback_data=self.callback)
        
        raise ValueError("Button must have url, route, or callback")
