



from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class RpcConfig:

    service_name: str
    version: str = '1.0.0'
    group: str = 'default'
    timeout: int = 5000
    retries: int = 2
    serializer_type: str = 'yaml'
    load_balance: str = 'random'
    extensions: Dict[str, Any] = field(default_factory=dict)
