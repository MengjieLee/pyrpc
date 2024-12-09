from dataclasses import dataclass
from typing import Any, List, Type


@dataclass
class RpcRequest:
    service_name: str
    method_name: str
    parameter_types: List[Type]
    args: List[Any]


@dataclass
class RpcResponse:
    data: Any
    message: str = ""
    exception: Exception = None
