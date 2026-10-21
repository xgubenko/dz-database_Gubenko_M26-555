"""
Основная логика работы с таблицами и данными
"""

def create_table(metadata: dict[str, list[str]], table_name: str, columns: list[str]) -> dict[str, list[str]]:
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

def drop_table(metadata: dict[str, list[str]], table_name: str) -> dict[str, list[str]]:
    """Проверяет существование таблицы. Если таблицы нет, выводит ошибку.
    Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    """
    if table_name not in metadata:
        print(f"Таблица '{table_name}' не существует.")
        return
    del metadata[table_name]
    return metadata