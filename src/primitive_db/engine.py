import prompt

"""
запуск, игровой цикл и парсинг команд
"""

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
    Первая попытка запустить проект!

    ***
    <command> exit - выйти из программы
    <command> help - справочная информация
    Введите команду: help

    <command> exit - выйти из программы
    <command> help - справочная информация
    """)

    name = prompt.string('Введите команду: ') 
    print(name)