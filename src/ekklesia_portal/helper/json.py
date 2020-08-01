import inspect
import json
from dataclasses import asdict, is_dataclass
from enum import Enum

from ekklesia_portal import enums

PUBLIC_ENUMS = {
    name: value
    for name, value in inspect.getmembers(enums) if inspect.isclass(value) and issubclass(value, Enum)
}


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        elif type(obj) in PUBLIC_ENUMS.values():
            return obj.value

        return json.JSONEncoder.default(self, obj)
