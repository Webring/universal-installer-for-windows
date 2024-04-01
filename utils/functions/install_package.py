import os
import shutil
import zipfile

from loguru import logger


def install_package(data):
    # ToDO все относительные адреса должны быть относительно файла .uip
    unzip_result = unzip_archives(data["archives"], "dev/packages/")

    shutil.rmtree("tmp/", ignore_errors=True)


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


def unzip(archive_path, destination_path):
    logger.info(f"Starting unzip archive '{archive_path}' to '{destination_path}'.")
    # ToDo Пусть плюет варнингом в случае, если он перезаписывает файл. Может в этом процессе поможет zip_ref.namelist()
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        logger.debug(zip_ref.namelist())
        zip_ref.extractall(destination_path)
    logger.info(f"Successfully unzip archive '{archive_path}' to '{destination_path}'.")
