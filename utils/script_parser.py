def parse_script_file(config_file_name: str) -> dict:
    data = dict()
    with open(config_file_name, mode="r", encoding="utf-8") as file:
        print(file.readlines())  # ToDo  Написать парсер скриптов
    return data
