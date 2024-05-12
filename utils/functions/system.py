import os
import shutil
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
                       ] = winreg.REG_SZ
                       ) -> bool:
    try:
        hkey_section, sub_key = address.split("\\", 1)
        reg_key = getattr(winreg, hkey_section)
        winreg.CreateKey(reg_key, sub_key)
        key_handle = winreg.OpenKey(reg_key, sub_key, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key_handle, key, 0, value_type, value)
        winreg.CloseKey(key_handle)
        logger.info(
            f"The value '{key}' in the registry '{address}' has been successfully set to '{value}'.")
        return True
    except Exception as e:
        logger.error(f"An error occurred while setting the value in the registry: {e}")
        return False


def delete_registry_key(key, subkey, subkeys=''):
    try:
        if subkeys == "":
            hkey = winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteKey(hkey, subkeys)
        else:
            hkey = winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(hkey, subkeys)
        winreg.CloseKey(hkey)
        logger.info(f"Ключ {subkeys} успешно удален")
    except FileNotFoundError:
        logger.error(f"Ключ {subkeys} не найден")
    except PermissionError:
        logger.error(f"Нет разрешения на удаление ключа {subkey}")


def delete_subkeys(key, subkey):
    try:
        hkey = winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS)
        i = 0
        while True:
            subkey_name = winreg.EnumKey(hkey, i)
            full_key_path = f"{subkey}\\{subkey_name}"
            delete_subkeys(key, full_key_path)
            delete_registry_key(key, full_key_path)
            i += 1
    except WindowsError:
        pass


def create_shortcut(shortcut_name: str, target: str, destination_dir: str, arguments: str = ''):
    # Работает только с абсолютными адресами
    # ToDo Добавить совместимость с относительными адересами

    if not os.path.exists(target):
        logger.critical(f"Target file '{target}' doesn't exist. Impossible to create shortcut.")
        return False

    if not shortcut_name.endswith(".lnk"):
        shortcut_name += ".lnk"

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(os.path.join(destination_dir, shortcut_name))
    shortcut.TargetPath = target
    shortcut.save()
    logger.info(f"The shortcut '{destination_dir}\\{shortcut_name}' has been successfully created.")
    return True


def unzip(archive_path, destination_path):
    logger.info(f"Starting unzip archive '{archive_path}' to '{destination_path}'.")
    # ToDo Пусть плюет варнингом в случае, если он перезаписывает файл. Может в этом процессе поможет zip_ref.namelist()
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        # logger.debug(zip_ref.namelist())
        zip_ref.extractall(destination_path)
    logger.info(f"Successfully unzip archive '{archive_path}' to '{destination_path}'.")


def copy_tree(source_path, destination_path) -> bool:
    if not os.path.exists(source_path):
        logger.critical(f"{source_path} does not exist.")
        return False

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    logger.info(f"Copying '{source_path}' to '{destination_path}'.")
    if os.path.isdir(source_path):
        shutil.copytree(source_path, destination_path)
    else:
        shutil.copy(source_path, destination_path)

    return True


def get_desktop_path() -> str:
    shell = Dispatch('WScript.Shell')
    return shell.SpecialFolders("Desktop")
