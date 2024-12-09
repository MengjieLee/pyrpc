import struct
from dataclasses import dataclass
from typing import Any


@dataclass
class ProtocolMessage:
    """
    Protocol Message structure
    """
    magic_number: int = None
    version: int = None
    serializer_type: int = None
    message_type: int = None
    compressor_type: int = None
    request_id: int = None
    body_length: int = None
    body: Any = None

    def to_bytes(self) -> bytes:
        """
        Convert ProtocolMessage to bytes
        +---------------+---------------+-----------------+-------------+
        | magic number | version       | serializer type | msg type    |
        | 4 bytes      | 1 byte        | 1 byte          | 1 byte      |
        +---------------+---------------+-----------------+-------------+
        | compressor   | request id    | body length     | body        |
        | 1 byte       | 8 bytes       | 4 bytes         | variable    |
        +---------------+---------------+-----------------+-------------+
        """
        header = struct.pack(
            '>IbbbbQI', # > means big-endian, I is 4-byte unsigned int, bbbb are four 1-byte unsigned ints, Q is 8-byte unsigned int
            self.magic_number,
            self.version,
            self.serializer_type,
            self.message_type,
            self.compressor_type,
            self.request_id,
            self.body_length
        )

        if self.body and self.body_length > 0:
            return header + self.body
        return header
    
    @classmethod
    def from_bytes(cls, data:bytes) -> 'ProtocolMessage':
        """
        Convert bytes to ProtocolMessage
        """
        # Read header
        header_size = struct.calcsize('>IbbbbQI')
        header = data[:header_size]

        # Unpack header
        magic_number, version, serializer_type, message_type, \
        compressor_type, request_id, body_length = struct.unpack('>IbbbbQI', header)

        # Read body
        body = None
        if body_length > 0:
            body = data[header_size:header_size + body_length]

        return cls(
            magic_number = magic_number,
            version = version,
            serializer_type = serializer_type,
            message_type = message_type,
            compressor_type = compressor_type,
            request_id = request_id,
            body_length = body_length,
            body = body
        )

    @staticmethod
    def get_header_length() -> int:
        return struct.calcsize('>IbbbbQI')
