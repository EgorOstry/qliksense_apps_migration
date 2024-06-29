import os
import json
import time
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


def app_export_step1(app_name, app_id, token):
    stage = 'export step 1'
    msg = 'start'
    logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")

    start_time = time.time()
    params = {
        'xrfkey': xrfkey
    }

    response = requests.post(f'https://qs/hdr/qrs/app/{app_id}/export/{token}', headers=headers, params=params, verify=False)

    if response.status_code in (200, 201):

        response = response.json()

        par = response['downloadPath'].split('?')[1].split('=')[1]
        path = response['downloadPath'].split('?')[0]

        end_time = time.time()
        duration = end_time - start_time
        msg = f'completed successfully in {duration:.2f} sec'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")

        return (app_name, app_id, par, path, duration)

    else:
        msg = 'request error'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return False


def app_export_step_2(app_name, app_id, par, path):
    stage = 'export step 2'
    msg = 'start'
    logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
    start_time = time.time()
    params = {
        'serverNodeId': par,
        'xrfkey': xrfkey
    }

    response = requests.get(f'https://qs/hdr{path}', headers=headers, params=params, verify=False)

    if response.status_code in (200, 201):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_save = os.path.abspath(os.path.join(base_dir, '..', 'exported_qvf_apps'))

        with open(os.path.join(path_to_save, app_id), 'wb') as file:
            file.write(response.content)



        end_time = time.time()
        duration = end_time - start_time
        msg = f'completed successfully in {duration:.2f} sec'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return (app_id, duration)

    else:
        msg = 'request error'
        logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
        return False