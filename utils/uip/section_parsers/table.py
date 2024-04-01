from typing import List


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


class TableParser:
    def __init__(self, size=2):
        self.size = size

    def __call__(self, cleared_lines: List[str]):
        data = []
        for line in cleared_lines:
            row = line.split(" ", self.size - 1)
            if len(row) < self.size:
                row += [''] * (self.size - len(row))
            row = [element.strip() for element in row]
            data.append(row)
        return data
