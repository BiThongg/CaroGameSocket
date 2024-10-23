from enum import Enum
import random
import string

def serializationFilter(obj, exclude: list[str] = []):
    def should_exclude(key):
        return any(ex in key for ex in exclude)
    if isinstance(obj, Enum):
        return obj.name
    elif isinstance(obj, dict):  
        return {
            k: serializationFilter(v, exclude) for k, v in obj.items() if not str(k).startswith("_") and not should_exclude(k)
        }
    elif hasattr(obj, "__dict__"):
        return {
            k: serializationFilter(v, exclude) for k, v in vars(obj).items() if not str(k).startswith("_") and  not should_exclude(k)
        }
    elif isinstance(obj, list):
        return [serializationFilter(i, exclude) for i in obj]
    else:
        return obj

def name_generation(length):
    characters = string.ascii_letters
    random_string = "".join(random.choices(characters, k=length))
    return random_string

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
