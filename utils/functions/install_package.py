import os
import shutil

from .system import unzip
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
    # ToDO все относительные адреса должны быть относительно файла .uip
    script_file_dir_path = os.path.dirname(data["path_to_package"])
    tmp_directory_path = os.path.join(script_file_dir_path, "tmp")

    os.makedirs(tmp_directory_path, exist_ok=True)

    normalised_archives_paths = [normalise_path(i, script_file_dir_path) for i in data["archives"]]
    unzip_result = unzip_archives(normalised_archives_paths, tmp_directory_path)

    #shutil.rmtree(tmp_directory_path, ignore_errors=True)
    logger.info(f"Deleting temporary directory : {tmp_directory_path}")
