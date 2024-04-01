def parse_dict_in_dict_section(cleared_lines):
    data = dict()
    subsection_name = None
    for line in cleared_lines:
        if "=" in line:
            if subsection_name is not None:
                key, value = line.split("=", 1)
                data[subsection_name][key] = value.strip()
        else:
            subsection_name = line.strip()
            data[subsection_name] = dict()

    return data
