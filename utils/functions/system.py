import winreg
import zipfile
from typing import Union

from loguru import logger
from win32com.client import Dispatch

def set_registry_value(address: str,
                       key: str,
                       value: str,
                       value_type: Union[
                           winreg.REG_SZ,
                           winreg.REG_EXPAND_SZ,
                           winreg.REG_MULTI_SZ,
                           winreg.REG_DWORD,
                           winreg.REG_QWORD,
                           winreg.REG_BINARY,
                       ]
                       ) -> None:
    try:
        hkey_section, sub_key = address.split("\\", 1)
        reg_key = getattr(winreg, hkey_section)
        key_handle = winreg.OpenKey(reg_key, sub_key, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key_handle, key, 0, value_type, value)
        winreg.CloseKey(key_handle)
        logger.info(
            f"The value '{key}' in the registry '{address}' has been successfully set to '{value}'.")
    except Exception as e:
        logger.error(f"An error occurred while setting the value in the registry: {e}")


def create_shortcut(shortcut_name: str, target: str, destination_dir: str, arguments: str = ''):
    # Работает только с абсолютными адресами
    # ToDo Добавить совместимость с относительными адересами
    if not shortcut_name.endswith(".lnk"):
        shortcut_name += ".lnk"

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_name)
    shortcut.TargetPath = target
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = destination_dir
    shortcut.save()

def unzip(archive_path, destination_path):
    logger.info(f"Starting unzip archive '{archive_path}' to '{destination_path}'.")
    # ToDo Пусть плюет варнингом в случае, если он перезаписывает файл. Может в этом процессе поможет zip_ref.namelist()
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        logger.debug(zip_ref.namelist())
        zip_ref.extractall(destination_path)
    logger.info(f"Successfully unzip archive '{archive_path}' to '{destination_path}'.")
