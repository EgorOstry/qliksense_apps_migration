import os
import time
import subprocess
from dotenv import load_dotenv

from procedure.logger import logger


load_dotenv(override=True)

apps_list_path = os.getenv("apps_list_path")
src = os.getenv("src")
dst = os.getenv("dst")
app_indent = int(os.getenv('app_indent'))
stage_indent = int(os.getenv('stage_indent'))

def check_access(path):
    try:
        os.listdir(path)
        print(f"Доступ к {path} есть.")
        return True
    except Exception as e:
        print(f"Ошибка при доступе к {path}: {e}")
        return False


def migrate(app_name, app_id):
    stage = 'migration'
    msg = 'start'
    logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
    src_app = os.path.join(src, app_id)
    dst_app = os.path.join(dst, app_id)
    start_time = time.time()
    result = subprocess.run(['cmd', '/c', 'copy', src_app, dst_app], capture_output=True, text=True)
    end_time = time.time()
    duration = end_time - start_time

    if result.returncode == 0:
        msg = f'completed successfully in {duration:.2f} sec'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return duration
    else:
        msg = 'copy error'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return False



