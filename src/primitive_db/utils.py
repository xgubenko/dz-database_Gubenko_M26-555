import json
from pathlib import Path
from typing import Any
from primitive_db.constants import DB_TABLE_STORAGE_PATH

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

def load_table_data(table_name: str) -> list[dict]:
    """Загружает данные таблицы из JSON-файла."""
    try:
        with Path(f"{DB_TABLE_STORAGE_PATH}/{table_name}.json").open(encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {DB_TABLE_STORAGE_PATH}/{table_name}.json")
        return []

def save_table_data(table_name: str, data: dict) -> None:
    """Сохраняет данные таблицы в JSON-файл."""
    print(f"Сохраняем данные таблицы '{table_name}' в файл {DB_TABLE_STORAGE_PATH}/{table_name}.json")
    with Path(f"{DB_TABLE_STORAGE_PATH}/{table_name}.json").open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def can_convert_to_int(value: str) -> bool:
    """Возможность приведения к целому числу"""
    try:
        int(value)
        return True
    except ValueError:
        return False

def can_convert_to_bool(value: str) -> bool:
    """Возможность приведения к bool"""
    try:
        bool(value)
        return True
    except ValueError:
        return False