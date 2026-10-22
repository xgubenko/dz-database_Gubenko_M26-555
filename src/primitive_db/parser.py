#<command> update <имя_таблицы> set <столбец1> = <новое_значение1> 
# where <столбец_условия> = <значение_условия> - обновить запись.

def parse_command(command: str, metadata: dict) -> tuple[str, dict, dict]:
    """Парсит команду и возвращает ее составляющие."""
    parts = command.split()
    
    table_name = parts[2]
    set_clause = {}
    where_clause = {}

    if "set" in parts:
        set_index = parts.index("set")
        where_index = parts.index("where") if "where" in parts else len(parts)

        for i in range(set_index + 1, where_index):
            if "=" in parts[i]:
                key, value = parts[i].split("=")
                set_clause[key] = value
        
    if "where" in parts:
        where_index = parts.index("where") if "where" in parts else len(parts)

        key = parts[where_index + 1]
        value = parts[where_index + 3]
        where_clause[key] = value

        table_metadata = metadata[table_name]
        for prop in table_metadata:
            prop_name, prop_type = prop.split(":")
            if where_clause.get(prop_name) is not None:
                temp = where_clause[prop_name]
                if(prop_type == "int"):
                    where_clause[prop_name] = int(temp)
                if(prop_type == "bool"):
                    where_clause[prop_name] = bool(temp)
            if set_clause.get(prop_name) is not None:
                temp = set_clause[prop_name]
                if(prop_type == "int"):
                    set_clause[prop_name] = int(temp)
                if(prop_type == "bool"):
                    set_clause[prop_name] = bool(temp)
    return table_name, set_clause, where_clause