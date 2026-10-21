import json
from pathlib import Path
from typing import Any

"""
Для вспомогательных функций
"""

DB_METADATA_PATH = "db_meta.json"

def load_metadata(filepath: str) -> dict:
    """Загружает метаданные из JSON-файла."""
    try:
        with Path(filepath).open(encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
        return {}

def save_metadata(filepath: str, data: dict[str, Any]) -> None:
    """Сохраняет метаданные в JSON-файл."""
    with Path(filepath).open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)