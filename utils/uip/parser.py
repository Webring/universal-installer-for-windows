from loguru import logger

from .section_parsers import parse_section


def parse_script_file(file_path: str) -> dict:
    data = dict()
    current_section_name = None
    current_section_cleared_lines = list()
    with open(file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            command, *comments = line.split("//", 1)
            command = command.strip()

            if not command:
                continue

            if command.startswith("[") and command.endswith("]"):
                if current_section_name is not None:
                    data[current_section_name] = parse_section(current_section_name, current_section_cleared_lines)

                current_section_name = command[1:-1]
                current_section_cleared_lines.clear()

                if current_section_name == "end":
                    break
            else:
                current_section_cleared_lines.append(command)
    logger.debug(data)
    return data
