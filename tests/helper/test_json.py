import json
from dataclasses import dataclass
from enum import Enum

import ekklesia_portal.helper.json
from ekklesia_portal.helper.json import JSONEncoder


def test_json_encoder():

    @dataclass
    class AB:
        a: int

    class E(Enum):
        A = 'a'

    @dataclass
    class A:
        b: int
        sub: AB
        enum: E

    ekklesia_portal.helper.json.PUBLIC_ENUMS['E'] = E

    data = A(4, AB(4), E.A)
    serialized = json.dumps(data, cls=JSONEncoder)
    assert serialized == '{"b": 4, "sub": {"a": 4}, "enum": "a"}'

    serialized = json.dumps({'a': 'b'}, cls=JSONEncoder)
    assert serialized == '{"a": "b"}'
