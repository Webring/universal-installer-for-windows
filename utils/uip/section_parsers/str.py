def parse_str_section(cleared_lines: list) -> str:
    data = str()
    for line in cleared_lines:
        if isinstance(line, str):
            data = line
    return data
