from enum import Enum
from threading import Lock

def serialization(obj, visited=None):
    if visited is None:
        visited = set()
    
    # Handle circular references
    if id(obj) in visited:
        return None
    
    if isinstance(obj, Enum):
        return obj.name
    elif isinstance(obj, dict):
        visited.add(id(obj))
        return {str(k): serialization(v, visited) for k, v in obj.items() if not str(k).startswith("_")}
    elif hasattr(obj, "__dict__"):
        visited.add(id(obj))
        return {str(k): serialization(v, visited) for k, v in vars(obj).items() if not str(k).startswith("_")}
    elif isinstance(obj, list):
        visited.add(id(obj))
        return [serialization(i, visited) for i in obj]
    else:
        return obj
