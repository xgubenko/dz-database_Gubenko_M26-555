from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.utils import can_convert_to_bool, can_convert_to_int

"""
Основная логика работы с таблицами и данными
"""


@handle_db_errors
def create_table(metadata: dict[str, list[str]], table_name: str, columns: list[str]) \
      -> dict[str, list[str]]:
    """Создает новую таблицу с указанными столбцами.
    Она должна принимать текущие метаданные, имя таблицы и список столбцов.
    Автоматически добавлять столбец ID:int в начало списка столбцов.
    Проверять, не существует ли уже таблица с таким именем. Если да, выводить ошибку.
    Проверять корректность типов данных (только int, str, bool).
    В случае успеха, обновлять словарь metadata и возвращать его.
    """
    if table_name in metadata:
        print(f"Таблица '{table_name}' уже существует.")
        return

    col_names = {col.split(":")[0] for col in columns}
    if "ID" not in col_names:
        columns.insert(0, "ID:int")
    else:
        for idx, col in enumerate(columns):
            if col.startswith("ID:"):
                columns.insert(0, columns.pop(idx))
                break


    correct_types = {"int", "str", "bool"}
    for column in columns:
        dtype = column.split(":")[1]
        if dtype not in correct_types:
            print(f"Некорректный тип данных '{dtype}' для столбца '{column}'.")
            return
    metadata[table_name] = columns
    return metadata

@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata: dict[str, list[str]], table_name: str) \
      -> dict[str, list[str]]:
    """Проверяет существование таблицы. Если таблицы нет, выводит ошибку.
    Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    """
    if table_name not in metadata:
        print(f"Таблица '{table_name}' не существует.")
        return
    del metadata[table_name]
    return metadata

@log_time
@handle_db_errors
def insert(metadata: dict[str, list[str]], table_name: str, values: list) -> dict:
    """Проверяет, существует ли таблица.
    Проверяет, что количество переданных значений соответствует 
    количеству столбцов (минус ID).
    Валидирует типы данных для каждого значения в соответствии со схемой в metadata.
    Генерирует новый ID (например, max(IDs) + 1 или len(data) + 1).
    Добавляет новую запись (в виде словаря) в данные таблицы и возвращает их."""

    if table_name not in metadata:
        print(f"Таблица '{table_name}' не существует.")
        return
    columns = metadata[table_name]
    if len(values) != len(columns) - 1:
        print("Количество значений не соответствует количеству столбцов") +\
        (f"ожидалось {len(columns) - 1}, получено {len(values)}).")
        return

    for i, column in enumerate(columns[1:]):
        col_name, col_type = column.split(":")
        if col_type == "int" and not can_convert_to_int(values[i]):
            print(f"Некорректный тип данных для столбца '{col_name}': ожидался int.")
            return
        elif col_type == "bool" and not can_convert_to_bool(values[i]):
            print(f"Некорректный тип данных для столбца '{col_name}': ожидался bool.")
            return
        if(col_type == "int"):
                    values[i] = int(values[i])
        if(col_type == "bool"):
            values[i] = bool(values[i])
        
    new_record = {}
    for i, column in enumerate(columns[1:]):
        new_record[column.split(":")[0]] = values[i]

    return new_record

@log_time
@handle_db_errors
def select(table_data: list[dict], where_clause: dict=None) -> list[dict]:
    """Возвращает все записи из таблицы, удовлетворяющие условию where_clause.
    Если where_clause не задан, возвращает все записи.
    """
    if where_clause is None:
        return table_data

    filtered_data = []
    for record in table_data:
        if all(record.get(key) == value for key, value in where_clause.items()):
            filtered_data.append(record)

    
    return filtered_data

@handle_db_errors
def update(table_data: list[dict], set_clause: dict, where_clause: dict) -> tuple[list[dict], list[int]]:
    """Обновляет записи в таблице, удовлетворяющие условию where_clause.
    set_clause - словарь с новыми значениями для обновления.
    """
    ids = []
    for record in table_data:
        if all(record.get(key) == value for key, value in where_clause.items()):
            for key, value in set_clause.items():
                record[key] = value
                ids.append(record["ID"])
    return table_data, ids

@confirm_action("удаление записи")
@handle_db_errors
def delete(table_data: list[dict], where_clause: dict) -> tuple[list[dict], list[int]]:
    """Удаляет записи из таблицы, удовлетворяющие условию where_clause."""
    ids = []
    updated_data = []
    for record in table_data:
        if all(record.get(key) == value for key, value in where_clause.items()):
                ids.append(record["ID"])
        else:
            updated_data.append(record)
    return updated_data, ids

        