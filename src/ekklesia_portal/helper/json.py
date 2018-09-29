from enum import Enum
from dataclasses import asdict, is_dataclass
import inspect
import json
from ekklesia_portal import enums

PUBLIC_ENUMS = {e.__name__: e for e in inspect.getmembers(enums) if inspect.isclass(e) and issubclass(e, Enum)}


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        elif type(obj) in PUBLIC_ENUMS.values():
            return obj.value

        return json.JSONEncoder.default(self, obj)
