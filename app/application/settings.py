import os

COUNT_RECORDS = 1_000_000
BULK_SIZE = 10_000

FORMAT_DATE = '%d-%m-%Y'
RU_FORMAT_DATE = "ДД-ММ-ГГГГ"

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
PATH_TO_DATABASE = os.path.join(BASE_DIR, "database.db")
PATH_TO_DESCRIPTION = os.path.join(BASE_DIR, "description.txt")