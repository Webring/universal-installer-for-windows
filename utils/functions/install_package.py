import os
import shutil

from loguru import logger

from .system import unzip, copy_tree, get_desktop_path, create_shortcut, set_registry_value


def normalise_path(path: str, start_path=None):
    expanded_path = os.path.expandvars(path)
    if os.path.isabs(expanded_path):
        return expanded_path

    if start_path is None:
        return os.path.abspath(path)

    if not os.path.isabs(start_path):
        start_path = os.path.abspath(start_path)

    return os.path.join(start_path, path)


def unzip_archives(archives, destination):
    result = {"success": True}
    for archive in archives:
        if os.path.exists(archive):
            unzip(archive, destination)
        else:
            logger.critical(f"Archive '{archive}' not exists !")
            result["success"] = False
            break

    return result


def install_package(data):
    # ToDO Проверки, очень много проверок!
    script_file_dir_path = os.path.dirname(data["path_to_package"])
    tmp_directory_path = os.path.join(script_file_dir_path, "tmp")

    os.makedirs(tmp_directory_path, exist_ok=True)

    normalised_archives_paths = [normalise_path(i, script_file_dir_path) for i in data["archives"]]
    unzip_result = unzip_archives(normalised_archives_paths, tmp_directory_path)

    destination_absolute_path = normalise_path(data["dir"]["Dir"])
    desktop_path = get_desktop_path()

    for file, destination in data["files"]:
        file_source = os.path.join(tmp_directory_path, file)
        file_destination = os.path.join(destination_absolute_path, destination)
        copy_tree(file_source, file_destination)

    for shortcut_name in data["icons"]:
        file_absolute_path = os.path.join(destination_absolute_path, shortcut_name)
        create_shortcut(shortcut_name, file_absolute_path, desktop_path)

    for address, values in data["registry"].items():
        for key, value in values.items():
            set_registry_value(address, key, value)

    shutil.rmtree(tmp_directory_path, ignore_errors=True)
    logger.info(f"Deleting temporary directory : {tmp_directory_path}")
