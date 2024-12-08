# pyrpc
## Introduction
pyrpc is a RPC framework established by Python.


## Features
- Uses Python's built-in pickle for serialization
- Uses Python's http.server instead of Vertx
- Uses Python's type hints and dataclasses for better type safety
- Simplified implementation while maintaining the core RPC concepts
- This implementation provides a basic RPC framework with:
  - Service registration
  - Request/response serialization
  - HTTP transport
  - Basic error handling


## TODO
- Better error handling
- Connection pooling
- Service discovery
- Load balancing
- Security features
- Async support


## Directory Structure
```bash
pyrpc/
├── example/
│   ├── common/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   └── service.py
│   ├── consumer/
│   │   ├── __init__.py
│   │   └── consumer.py
│   └── provider/
│       ├── __init__.py
│       └── provider.py
├── pyrpc/
│   ├── __init__.py
│   ├── model.py
│   ├── proxy.py
│   ├── registry.py
│   ├── serializer.py
│   └── server.py
└── README.md
```


## Quick Start
```bash
python3 -m venv <venv_name>

# run venv
source <venv_name>/bin/activate
pip install --upgrade pip
# pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org requests
pip install requests

# start provider
# python -m example/provider/provider.py
python -m example.provider.provider

# start consumer
# python -m example/consumer/consumer.py
python -m example.consumer.consumer

# exit venv
deactivate
```


## example
```bash
(pyrpc) limengjie@limengjiedeMacBook-Pro pyrpc % python -m example.provider.provider
Server running on ('127.0.0.1', 8080)
127.0.0.1 - - [09/Dec/2024 00:09:45] "POST / HTTP/1.1" 200 -

(pyrpc) limengjie@limengjiedeMacBook-Pro pyrpc % python -m example.consumer.consumer
Response: Hello, MJ!
```