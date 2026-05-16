"""
Ultra-optimized callback transport layer for Telegram's 64-byte callback_data limit.

Fixed-position string splitting strategy (no delimiters):
- [0:2]    Command prefix (2 bytes)
- [2:10]   Deterministic route hash (8 bytes)
- [10:64]  User payload (up to 54 bytes)

Total: 64 bytes maximum, zero-copy design.
"""

import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

# Constants
COMMAND_SIZE = 2
HASH_SIZE = 8
MAX_PAYLOAD_SIZE = 54
TOTAL_SIZE = 64


@dataclass
class CallbackData:
    """Unpacked callback data structure"""
    command: str
    hash_8: str
    payload: str


class CallbackTransport:
    """
    Ultra-optimized callback packing/unpacking layer.
    Fixed-position string splitting strategy for Telegram's 64-byte limit.
    
    Zero delimiters, deterministic layout, collision-resistant hashing.
    """
    
    @staticmethod
    def pack(command: str, hash_8: str, payload: str = "") -> str:
        """
        Pack command, hash, and payload into tight 64-byte callback string.
        
        Args:
            command: 2-character command prefix (e.g., "ml")
            hash_8: 8-character route hash
            payload: User-provided payload (max 54 bytes)
        
        Returns:
            Packed callback string
        
        Raises:
            ValueError: If any component exceeds size limits
        """
        if len(command) != COMMAND_SIZE:
            raise ValueError(
                f"Command must be exactly {COMMAND_SIZE} bytes, got {len(command)}"
            )
        
        if len(hash_8) != HASH_SIZE:
            raise ValueError(
                f"Hash must be exactly {HASH_SIZE} bytes, got {len(hash_8)}"
            )
        
        payload_bytes = len(payload.encode())
        if payload_bytes > MAX_PAYLOAD_SIZE:
            raise ValueError(
                f"Payload exceeds {MAX_PAYLOAD_SIZE} bytes. "
                f"Got {payload_bytes} bytes: {payload[:20]}..."
            )
        
        # Pack without delimiters
        packed = f"{command}{hash_8}{payload}"
        
        # Validate final size
        packed_bytes = len(packed.encode())
        if packed_bytes > TOTAL_SIZE:
            raise ValueError(
                f"Final packed size exceeds {TOTAL_SIZE} bytes, got {packed_bytes}"
            )
        
        logger.debug(
            f"Packed callback: cmd={command} hash={hash_8} "
            f"payload_len={payload_bytes}/{MAX_PAYLOAD_SIZE}"
        )
        return packed
    
    @staticmethod
    def unpack(data: str) -> CallbackData:
        """
        Unpack tight callback string into components by fixed positions.
        
        Args:
            data: Packed callback string
        
        Returns:
            CallbackData with command, hash, payload
        
        Raises:
            ValueError: If data structure is invalid
        """
        min_size = COMMAND_SIZE + HASH_SIZE
        if len(data) < min_size:
            raise ValueError(
                f"Invalid callback data. Minimum size is {min_size}, got {len(data)}"
            )
        
        command = data[0:COMMAND_SIZE]
        hash_8 = data[COMMAND_SIZE:COMMAND_SIZE + HASH_SIZE]
        payload = data[COMMAND_SIZE + HASH_SIZE:]
        
        logger.debug(
            f"Unpacked callback: cmd={command} hash={hash_8} "
            f"payload_len={len(payload)}"
        )
        
        return CallbackData(command=command, hash_8=hash_8, payload=payload)
    
    @staticmethod
    def is_minline_callback(data: str, command_prefix: str = "ml") -> bool:
        """
        Check if callback is from Minline (starts with command prefix).
        
        Args:
            data: Callback data string
            command_prefix: Expected command prefix (default: "ml")
        
        Returns:
            True if callback is a valid Minline callback
        """
        if len(data) < COMMAND_SIZE:
            return False
        return data[:COMMAND_SIZE] == command_prefix
    
    @staticmethod
    def get_size_info(data: str) -> dict:
        """Get detailed size breakdown for callback data"""
        return {
            "total_bytes": len(data.encode()),
            "max_bytes": TOTAL_SIZE,
            "remaining_bytes": TOTAL_SIZE - len(data.encode()),
            "utilization_percent": round((len(data.encode()) / TOTAL_SIZE) * 100, 1),
        }
