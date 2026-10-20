import prompt


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