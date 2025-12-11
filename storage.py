import json
import threading
from typing import Dict, Any, List

DATA_FILE = "media_store.json"
_LOCK = threading.Lock()

def _load_all() -> Dict[str, Dict[str, Any]]:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        # corrupted file -> start fresh (could also backup)
        return {}

def _save_all(data: Dict[str, Dict[str, Any]]) -> None:
    with _LOCK:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def list_all() -> List[Dict[str, Any]]:
    return list(_load_all().values())

def list_by_category(category: str) -> List[Dict[str, Any]]:
    return [m for m in _load_all().values() if m.get("category","").lower() == category.lower()]

def find_by_name_exact(name: str):
    return _load_all().get(name)

def get_metadata(name: str):
    return find_by_name_exact(name)

def create_media(media: Dict[str, Any]) -> bool:
    data = _load_all()
    name = media.get("name")
    if not name or name in data:
        return False
    # Add borrow/return fields
    media["available"] = True
    media["borrowed_by"] = None
    media["borrow_date"] = None
    data[name] = media
    _save_all(data)
    return True

def delete_media(name: str) -> bool:
    data = _load_all()
    if name in data:
        del data[name]
        _save_all(data)
        return True
    return False

def borrow_media(name: str, borrower: str) -> bool:
    """Mark an item as borrowed by a person."""
    data = _load_all()
    if name not in data:
        return False
    item = data[name]
    if not item.get("available", True):
        return False  # Already borrowed
    
    from datetime import datetime
    item["available"] = False
    item["borrowed_by"] = borrower
    item["borrow_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _save_all(data)
    return True

def return_media(name: str) -> bool:
    """Mark a borrowed item as returned."""
    data = _load_all()
    if name not in data:
        return False
    item = data[name]
    if item.get("available", True):
        return False  # Not borrowed
    
    item["available"] = True
    item["borrowed_by"] = None
    item["borrow_date"] = None
    _save_all(data)
    return True

def get_borrowed_items() -> List[Dict[str, Any]]:
    """Get all currently borrowed items."""
    return [m for m in _load_all().values() if not m.get("available", True)]
