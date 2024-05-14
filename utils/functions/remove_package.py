import os
import shutil
import ctypes
import winreg

from .system import delete_subkeys, delete_registry_key, get_desktop_path
from loguru import logger


def normalise_path(path: str, start_path=None):
    expanded_path = os.path.expandvars(path)
    if os.path.isabs(expanded_path):
        return expanded_path

    if start_path is None:
        return os.path.abspath(path)

    if not os.path.isabs(start_path):
        start_path = os.path.abspath(start_path)

    return os.path.join(start_path, path)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def remove_package(data, is_force_removing):
    if is_force_removing is None:
        logger.info("Wrong way of removing has been selected")
        return
    if is_force_removing:
        destination_absolute_path = normalise_path(data["dir"]["Dir"])
        shutil.rmtree(destination_absolute_path)

        for icon_name in data['icons']:
            icon_absolute_path = os.path.join(get_desktop_path(), icon_name + ".lnk")
            os.remove(icon_absolute_path)

        registry_pathes = data["registry"]
        for key, values in registry_pathes.items():
            count = 0
            for i in key:
                if i == "\\":
                    key_path = key[:count]
                    key_sub = key[count + 1:]
                    delete_subkeys(getattr(winreg, key_path), key_sub)
                    delete_registry_key(getattr(winreg, key_path), key_sub)
                    break
                else:
                    count += 1

        logger.info(f"Forced removing package: {data['title']}")
        return

    for files in data['files']:
        destination_absolute_path = normalise_path(data["dir"]["Dir"])
        if files[1] == "":
            destination_absolute_path += "\\" + files[0]
        else:
            destination_absolute_path += "\\" + files[1] + "\\" + files[0]
        os.remove(destination_absolute_path)
        if not os.listdir(os.path.dirname(destination_absolute_path)):
            os.rmdir(os.path.dirname(destination_absolute_path))
        else:
            print("Directory is not empty")

    for icon_name in data['icons']:
        icon_absolute_path = os.path.join(get_desktop_path(), icon_name + ".lnk")
        os.remove(icon_absolute_path)

    registry_pathes = data["registry"]
    for key, values in registry_pathes.items():
        for sub_key, sub_value in values.items():
            delete_registry_key(getattr(winreg, key.split('\\')[0]), "\\".join(key.split('\\')[1:]), sub_key)

    logger.info(f"Soft removing package: {data['title']}")
    return
