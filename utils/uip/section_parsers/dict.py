def parse_dict_section(cleared_lines):
    data = dict()
    for line in cleared_lines:
        if "=" in line:
            key, value = line.split("=", 1)
            data[key] = value.strip()
    return data
