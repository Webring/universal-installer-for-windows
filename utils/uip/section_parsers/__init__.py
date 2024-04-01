from typing import Any

from .str import parse_str_section
from .list import parse_list_section
from .dict import parse_dict_section
from .dict_in_dict import parse_dict_in_dict_section
from .table import TableParser

DEFAULT_PARSER = parse_list_section

SECTIONS_PARSERS = {
    "title": parse_str_section,
    "archives": parse_list_section,
    "dir": parse_dict_section,
    "icons": parse_list_section,
    "files": TableParser(2),
    "registry": parse_dict_in_dict_section,
}


def parse_section(section_name: str, cleared_section_lines: list) -> Any:  # ToDo сделать норм нотацию типов
    return SECTIONS_PARSERS.get(section_name, DEFAULT_PARSER)(cleared_section_lines)
