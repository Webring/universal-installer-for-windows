import os
import shutil

from .system import unzip
from loguru import logger


def normalise_path(path: str, start_path=None):
    expanded_path = os.path.expandvars(path)
    if os.path.isabs(expanded_path):
        return expanded_path
    return os.path.abspath(expanded_path)


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

    unzip_result = unzip_archives(data["archives"], tmp_directory_path)

    shutil.rmtree(tmp_directory_path, ignore_errors=True)
    logger.info(f"Deleting temporary directory : {tmp_directory_path}")
