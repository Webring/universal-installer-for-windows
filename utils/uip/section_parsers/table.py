from typing import List


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
