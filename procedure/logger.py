import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv


load_dotenv(override=True)

script_name = os.getenv("script_name")

# Конфигурация логгирования
# log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

# Логгер с ротацией файлов
log_file = '../app.log'
log_max_size = 10 * 1024 * 1024  # 10MB
log_backup_count = 5  # количество файлов бэкапа

file_handler = RotatingFileHandler(log_file, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Логгер для консоли
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# Главный логгер
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


logger.info(f'START {script_name}')

