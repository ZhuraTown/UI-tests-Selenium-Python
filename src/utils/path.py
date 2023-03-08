import os
import random
from time import sleep
from typing import BinaryIO


class Files:
    _BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _FILE_DIR = "files"
    _UTILS_DIR = "utils"
    _DOWNLOAD_DIR = 'download'
    _SRC_DIR = "src"
    _CORE_DIR = 'core'
    RESULT_DIR = 'results_reports'

    DOCUMENT_PDF = "sample_card.pdf"
    DOCUMENT_DOC = "document.doc"
    IDENTITY_CARD = "identity_card.jpg"
    IDENTITY_CARD_SMALL = "identity_card_small.jpg"
    # IMAGE = "avatar.png"
    SIGNATURE = "signature.png"
    ADMISSION_ORDER = "admission_order.pdf"
    AVATAR_USER, AVATAR_WORKER = f"user_{random.randint(1, 2)}.png", f"worker_{random.randint(1, 3)}.png"
    IMAGE_COMPANY = "avatar_company.png"
    TABLE_GSM = "table_gsm.xlsx"

    IDENTITY_CARD_PATH = os.path.join(_BASE_DIR, _SRC_DIR, _FILE_DIR, IDENTITY_CARD)
    IDENTITY_CARD_SMALL_PATH = os.path.join(_BASE_DIR, _SRC_DIR, _FILE_DIR, IDENTITY_CARD_SMALL)
    SIGNATURE_PATH = os.path.join(_BASE_DIR, _SRC_DIR, _FILE_DIR, SIGNATURE)
    AVATAR_WORKER_PATH = os.path.join(_BASE_DIR, _SRC_DIR, _FILE_DIR, AVATAR_WORKER)
    AVATAR_USER_PATH = os.path.join(_BASE_DIR, _SRC_DIR, _FILE_DIR, AVATAR_USER)
    AVATAR_COMPANY_PNG_PATH = os.path.join(_BASE_DIR, _SRC_DIR, _FILE_DIR, IMAGE_COMPANY)
    DOCUMENT_PDF_PATH = os.path.join(_BASE_DIR, _SRC_DIR, _FILE_DIR, DOCUMENT_PDF)
    DOCUMENT_DOC_PATH = os.path.join(_BASE_DIR, _SRC_DIR, _FILE_DIR, DOCUMENT_DOC)
    ADMISSION_ORDER_PATH = os.path.join(_BASE_DIR, _SRC_DIR, _FILE_DIR, ADMISSION_ORDER)
    TABLE_GSM_PATH = os.path.join(_BASE_DIR, _SRC_DIR, _FILE_DIR, TABLE_GSM)

    DOWNLOAD_FILES_PATH = os.path.join(_BASE_DIR, _DOWNLOAD_DIR)

    @staticmethod
    def get_path_to_file(file_type: str) -> str:
        match file_type:
            case "PDF":
                return Files.DOCUMENT_PDF_PATH
            case "DOC":
                return Files.DOCUMENT_DOC_PATH
            case "XLSX":
                return Files.TABLE_GSM_PATH
            case "PNG":
                return Files.AVATAR_COMPANY_PNG_PATH
            case "JPG":
                return Files.IDENTITY_CARD_PATH
            case _:
                raise Exception(f"Формата файла {file_type} нет.")

    @staticmethod
    def get_file_bytes(path_to_file: str) -> BinaryIO:
        return open(path_to_file, "rb")

    @staticmethod
    def wait_while_file_download(attempt: int = 20):
        n = 0
        while n < attempt:
            sleep(0.6)
            if len(os.listdir(Files.DOWNLOAD_FILES_PATH)) == 0:
                n += 1
            else:
                return None

    @staticmethod
    def delete_all_download_files():
        sleep(2)
        for file in os.listdir(Files.DOWNLOAD_FILES_PATH):
            os.remove(os.path.join(Files.DOWNLOAD_FILES_PATH, file))
        return None

    @staticmethod
    def find_file_in_dir_with_name(name_file: str = None) -> bool or (bool, str):
        for file in os.listdir(Files.DOWNLOAD_FILES_PATH):
            if name_file in file:
                return True
        return False, f"Файлы в папках, {os.listdir(Files.DOWNLOAD_FILES_PATH)}"

    @staticmethod
    def get_path_for_first_file_in_download() -> str:
        file = os.listdir(Files.DOWNLOAD_FILES_PATH)[0]
        return os.path.join(Files.DOWNLOAD_FILES_PATH, file)

