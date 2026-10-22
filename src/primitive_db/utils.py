import json
from pathlib import Path
from typing import Any

"""
Для вспомогательных функций
"""

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

def load_table_data(table_name: str) -> dict:
    """Загружает данные таблицы из JSON-файла."""
    try:
        with Path(f"data/{table_name}.json").open(encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: data/{table_name}.json")
        return {}

def save_table_data(table_name: str, data: dict) -> None:
    """Сохраняет данные таблицы в JSON-файл."""
    with Path(f"data/{table_name}.json").open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)