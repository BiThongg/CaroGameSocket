from enum import Enum

def serialization(obj):
    if isinstance(obj, Enum):
        return obj.name
    elif isinstance(obj, dict):
        return {k: serialization(v) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        return {k: serialization(v) for k, v in vars(obj).items()}
    elif isinstance(obj, list):
        return [serialization(i) for i in obj]
    else:
        return obj
