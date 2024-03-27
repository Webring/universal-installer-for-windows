from typing import List


def parse_list_section(cleared_lines) -> List[str]:
    data = []
    for line in cleared_lines:
        if isinstance(line, str):
            data.append(line)
    return data
