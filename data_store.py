import json
import os
import shutil
from datetime import datetime
from typing import List


class DataStore:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def get_path(self, filename: str) -> str:
        return os.path.join(self.data_dir, filename)

    def backup_file(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            return
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        backup_path = f"{filepath}.{timestamp}.bak"
        shutil.copy2(filepath, backup_path)

    def load_list(self, filename: str) -> List[dict]:
        filepath = self.get_path(filename)
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("data must be a list")
            return data
        except (OSError, json.JSONDecodeError, ValueError):
            return []

    def save_list(self, filename: str, items: List[dict]) -> None:
        filepath = self.get_path(filename)
        self.backup_file(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)
