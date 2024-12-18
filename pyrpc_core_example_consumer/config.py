from pyrpc_core.config import RpcConfig, RegistryConfig

# RPC配置
DEFAULT_RPC_CONFIG = RpcConfig(
    service_name="user-service",
    version="1.0.0",
    group="default",
    timeout=5000,
    retries=2,
    serializer_type="yaml",
    load_balance="random"
)

# 注册中心配置
DEFAULT_REGISTRY_CONFIG = RegistryConfig(
    registry_type="redis",
    address="localhost:6379",
    namespace="pyrpc",
    connect_timeout=5000
)