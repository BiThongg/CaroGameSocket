from enum import Enum

def serializationFilter(obj, exclude = []):
    def should_exclude(key):
        return any(ex in key for ex in exclude)

    if isinstance(obj, Enum):
        return obj.name
    elif isinstance(obj, dict):  
        return {
            k: serializationFilter(v, exclude) for k, v in obj.items() if not should_exclude(k)
        }
    elif hasattr(obj, "__dict__"):
        return {
            k: serializationFilter(v, exclude) for k, v in vars(obj).items() if not should_exclude(k)
        }
    elif isinstance(obj, list):
        return [serializationFilter(i, exclude) for i in obj]
    else:
        return obj
