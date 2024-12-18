import pytest
from pyrpc_core.serializer import YamlSerializer


@pytest.fixture
def serializer():
    return YamlSerializer()


def test_serialize_and_deserialize(serializer):
    data = {'key': 'value', 'number': 42}
    serialized_data = serializer.serialize(data)
    deserialized_data = serializer.deserialize(serialized_data)

    assert deserialized_data == data
