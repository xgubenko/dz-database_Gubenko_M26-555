import shlex
from unittest import result

import prompt
from prettytable import PrettyTable

from primitive_db.core import create_table, drop_table, insert, select
from primitive_db.parser import parse_command
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

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
    print("Добро пожаловать в PrimitiveDB!")

    while True:
        metadata = load_metadata(DB_METADATA_PATH)
        user_input = prompt.string('Введите команду: ')
        args = shlex.split(user_input)
        cmd_name = args[0] if args else None

        if args[0] == "insert" and args[1] == "into":
            cmd_name = "insert into"
        elif args[0] == "delete" and args[1] == "from":
            cmd_name = "delete from"
        elif args[0] == "select" and args[1] == "from":
            cmd_name = "select from"

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

            case "list_tables":
                if metadata:
                    print("Список таблиц:")
                    for table_name in metadata.keys():
                        print(f"- {table_name}")
                else:
                    print("Нет таблиц.")

            case "help":
                print_help()

            case "exit":
                print("Выход из программы.")
                break

            case "insert into":
                metadata = load_metadata(DB_METADATA_PATH)
                insert_args = " ".join(args[4:])[1:-1].split(",")
                insert_args = [x.strip() for x in insert_args]
                table_name = args[2]

                new_record = insert(metadata, table_name, insert_args)
                table_data = load_table_data(table_name)
                id = max([record["ID"] for record in table_data] + [0]) + 1
                new_record["ID"] = id
                table_data.append(new_record)
                print(f"Запись успешно добавлена в таблицу '{table_name}': {new_record}")
                save_table_data(table_name, table_data)

            case "select from":
                if(len(args) < 3):
                        print("Введенная команда некорректна")
                        continue
                
                metadata = load_metadata(DB_METADATA_PATH)
                table_data = load_table_data(args[2])
                table_name, _, where_clause = parse_command(user_input)
                selected_records = select(table_data, where_clause)

                if selected_records:
                    table = PrettyTable()
                    table.field_names = selected_records[0].keys()
                    for record in selected_records:
                        table.add_row(record.values())
                    if not table.rows:
                        print("Таблица пуста")
                    else: 
                        print(table)
                        
            case "update":
                pass

            case "delete drom":
                pass