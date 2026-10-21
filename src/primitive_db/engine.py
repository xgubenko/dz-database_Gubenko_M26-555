import prompt
import shlex
from primitive_db.utils import load_metadata, save_metadata
from primitive_db.core import create_table, drop_table

"""
запуск, игровой цикл и парсинг команд
"""

#Вся информация о таблицах (их имена и структура столбцов) будет храниться в одном файле
DB_METADATA_PATH = "db_meta.json"

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print("""
    Введите команду!

    ***
    <command> create_table name asd:str
    <command> drop_table name
    """)

    while True:
        metadata = load_metadata(DB_METADATA_PATH)
        user_input = prompt.string('Введите команду: ')
        args = shlex.split(user_input)
        cmd_name = args[0] if args else None
        match cmd_name:
            case "create_table":
                name = args[1]
                columns = args[2:]
                metadata = create_table(metadata, name, columns)
                if metadata is not None:
                    save_metadata(DB_METADATA_PATH, metadata)

            case "drop_table":
                name = args[1]
                metadata = drop_table(metadata, name)
                if metadata is not None:
                    save_metadata(DB_METADATA_PATH, metadata)
        