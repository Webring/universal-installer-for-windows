def parse_config_file(config_file_name: str) -> dict:
    data = dict()
    with open(config_file_name, mode="r", encoding="utf-8") as file:
        print(file.readlines())
    return data
