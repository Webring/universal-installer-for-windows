import os
import shutil

from loguru import logger

from .system import unzip, copy_tree, get_desktop_path, create_shortcut, set_registry_value, normalise_path


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

    if not unzip_result["success"]:
        return False

    destination_absolute_path = normalise_path(data["dir"]["Dir"])
    desktop_path = get_desktop_path()

    for file, destination in data["files"]:
        file_source = os.path.join(tmp_directory_path, file)
        file_destination = os.path.join(destination_absolute_path, destination)
        copying_success = copy_tree(file_source, file_destination)

        if not copying_success:
            return False

    for shortcut_name in data["icons"]:
        file_absolute_path = os.path.join(destination_absolute_path, shortcut_name)
        shortcut_creation_success = create_shortcut(shortcut_name, file_absolute_path, desktop_path)

        if not shortcut_creation_success:
            return False

    for address, values in data["registry"].items():
        for key, value in values.items():
            set_success = set_registry_value(address, key, value)

            if not set_success:
                return False

    shutil.rmtree(tmp_directory_path, ignore_errors=True)
    logger.info(f"Deleting temporary directory : {tmp_directory_path}")
    return True
