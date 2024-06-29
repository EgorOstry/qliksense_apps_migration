import os
import time
import json
import requests
from dotenv import load_dotenv

from procedure.logger import logger


requests.packages.urllib3.disable_warnings()
load_dotenv(override=True)


xrfkey = os.getenv('xrfkey')
hdr_usr = os.getenv('hdr-usr')
X_Qlik_xrfkey = os.getenv('X-Qlik-xrfkey')
Content_Type = os.getenv('Content-Type')
app_indent = int(os.getenv('app_indent'))
stage_indent = int(os.getenv('stage_indent'))

headers = {
  'X-Qlik-xrfkey': X_Qlik_xrfkey,
  'hdr-usr': hdr_usr,
  'Content-Type': Content_Type,
}


def initial_app_import(app_name, app_id):
    stage = 'import'
    msg = 'start'
    logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
    start_time = time.time()
    payload = json.dumps(f"{app_id}")
    params = {
        'name': f'{app_name}',
        'xrfkey': xrfkey
    }

    response = requests.post('https://qs2/hdr/qrs/app/import', headers=headers, params=params, data=payload, verify=False)

    if response.status_code in (200, 201):
        end_time = time.time()
        duration = end_time - start_time
        msg = f'completed successfully in {duration:.2f} sec'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return (response.json(), duration)

    else:
        msg = 'request error'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return False


def initial_app_publish(app_name, new_app_id, stream_id):
    stage = 'publish'
    msg = 'start'
    logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
    start_time = time.time()

    params = {
        'stream' : f'{stream_id}',
        'xrfkey' : xrfkey
    }

    response = requests.put(f'https://qs2/hdr/qrs/app/{new_app_id}/publish', headers=headers, params = params, verify=False)

    if response.status_code in (200, 201):

        end_time = time.time()
        duration = end_time - start_time
        msg = f'completed successfully in {duration:.2f} sec'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return (response.json(), duration)

    else:
        msg = 'request error'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return False


def regular_app_import_replace(app_name, app_id, new_app_id):
    stage = 'replace'
    msg = 'start'
    logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")

    start_time = time.time()
    payload = json.dumps(f"{app_id}")
    params = {
        'targetappid' : f'{new_app_id}',
        'xrfkey' : xrfkey
    }

    response = requests.post(f'https://qs2/hdr/qrs/app/import/replace', headers=headers, params = params, data=payload, verify=False)

    if response.status_code in (200, 201):

        end_time = time.time()
        duration = end_time - start_time
        msg = f'completed successfully in {duration:.2f} sec'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return (response.json(), duration)

    else:
        msg = 'request error'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return False