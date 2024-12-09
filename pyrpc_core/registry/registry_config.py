from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class RegistryConfig:
    registry_type: str
    address: str
    username: str = None
    password: str = None
    timeout: int = 10000 # ms
    properties: Dict[str, Any] = None
