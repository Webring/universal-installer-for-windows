import os
import shutil
import ctypes
import winreg

from .system import delete_subkeys, delete_registry_key, get_desktop_path, normalise_path
from loguru import logger


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def remove_package(data, is_force_removing):
    if is_force_removing is None:
        logger.info("Wrong way of removing has been selected")
        return

    for icon_name in data['icons']:
        icon_absolute_path = os.path.join(get_desktop_path(), icon_name + ".lnk")
        if os.path.exists(icon_absolute_path):
            os.remove(icon_absolute_path)
            logger.info(f"Icon '{icon_absolute_path}' successfully removed")
        else:
            logger.info(f"Icon '{icon_absolute_path}' does not exist")

    destination_absolute_path = normalise_path(data["dir"]["Dir"])

    if is_force_removing:
        if os.path.exists(destination_absolute_path):
            shutil.rmtree(destination_absolute_path)
            logger.info(f"Program directory '{destination_absolute_path}' successfully deleted")
        else:
            logger.info(f"Program directory '{destination_absolute_path}' not found")

    else:
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

    if is_force_removing:
        registry_paths = data["registry"]
        for key, values in registry_paths.items():

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

            # for _ in values.items():
            #     delete_subkeys(getattr(winreg, key.split('\\')[0]), "\\".join(key.split('\\')[1:]))
            #     delete_registry_key(getattr(winreg, key.split('\\')[0]), "\\".join(key.split('\\')[1:]))
    else:
        registry_paths = data["registry"]
        for key, values in registry_paths.items():
            for sub_key, sub_value in values.items():
                delete_registry_key(getattr(winreg, key.split('\\')[0]), "\\".join(key.split('\\')[1:]), sub_key)

    if is_force_removing:
        logger.success(f"Package '{data['title']}' forced removed")
    else:
        logger.success(f"Package '{data['title']}' softly removed")
