def parse_dict_section(cleared_lines):
    data = ""
    for line in cleared_lines:
        if isinstance(line, str):
            data = line
    return data
