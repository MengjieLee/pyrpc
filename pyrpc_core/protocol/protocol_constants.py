class ProtocolConstants:
    """
    Protocol constants
    """

    # Message type
    REQUEST_TYPE = 1
    RESPONSE_TYPE = 2

    # Serializer type
    SERIALIZER_JDK = 1
    SERIALIZER_JSON = 2
    SERIALIZER_KRYO = 3

    # Compress type
    COMPRESSOR_NONE = 0
    COMPRESSOR_GZIP = 1

    # Protocol mask
    MAGIC_NUMBER = 0xCAFEBABE

    # Protocol version
    VERSION = 1
