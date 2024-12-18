from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class RegistryConfig:
    registry_type: str
    address: str
    username: Optional[str] = None
    password: Optional[str] = None
    namespace: str = 'default'
    connect_timeout: int = 5000
    session_timeout: int = 30000
    extensions: Dict[str, Any] = field(default_factory=dict)
