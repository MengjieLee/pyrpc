class LocalRegistry:
    _registry = {}

    @classmethod
    def register(cls, service_name: str, service: object):
        cls._registry[service_name] = service
    
    @classmethod
    def get_service(cls, service_name: str) -> object:
        return cls._registry[service_name]
