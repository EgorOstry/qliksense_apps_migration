import os
import json
import pprint
import requests
from typing import Union
from datetime import datetime
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
  'Content-Type': Content_Type
}


def get_app_info(app_id:str)-> Union[dict, bool]:
    app_info = dict()
    stage = 'get app info'

    filter = f"id eq {app_id} and published eq True"
    url = 'https://qs/hdr/qrs/app'
    full_url = f"{url}?xrfkey={xrfkey}&filter={filter}"



    with requests.session() as Session:
        response = requests.get(full_url, headers=headers, verify=False)

        if response.status_code in (200, 201):

            res = json.loads(response.content.decode())

            if len(res) == 0:

                msg = 'not found on QS'
                logger.info(f"app:{app_id:{app_indent}} stage:{stage:{stage_indent}} : {msg}")

                app_info['app_name_qs'] = None
                app_info['app_id_qs'] = None
                app_info['is_published_on_qs'] = None
                app_info['stream_name_qs'] = None
                app_info['stream_id_qs'] = None

                return False

            else:

                app_info['app_name_qs'] = res[0]['name']
                app_info['app_id_qs'] = res[0]['id']
                app_info['stream_name_qs'] = res[0]['stream']['name']
                app_info['stream_id_qs'] = res[0]['stream']['id']
                app_info['is_published_on_qs'] = res[0]['published']

                msg = 'found on QS'
                logger.info(f"app:{app_info['app_name_qs']:{app_indent}} stage:{stage:{stage_indent}} : {msg}")

        else:
            msg = 'request error'
            logger.info(f"app:{app_id:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
            return False

    filter = f"Name eq '{app_info['app_name_qs']}' and published eq True"
    url = 'https://qs2/hdr/qrs/app'
    full_url = f"{url}?xrfkey={xrfkey}&filter={filter}"

    with requests.session() as Session:
        response = requests.get(full_url, headers=headers, verify=False)

        if response.status_code in (200, 201):

            res = json.loads(response.content.decode())

            if len(res) == 0:
                msg = 'not found on QS2'
                logger.info(f"app:{app_info['app_name_qs']:{app_indent}} stage:{stage:{stage_indent}} : {msg}")

                app_info['app_name_qs2'] = None
                app_info['app_id_qs2'] = None
                app_info['is_published_on_qs2'] = None
                # app_info['stream_name_qs2'] = None
                # app_info['stream_id_qs2'] = None

                get_stream_id = get_stream_id_from_qs2_by_name(app_info['stream_name_qs'])
                if get_stream_id:
                    app_info['stream_name_qs2'], app_info['stream_id_qs2'] = get_stream_id_from_qs2_by_name(
                        app_info['stream_name_qs'])

                    return app_info

                else:
                    msg = 'Stream not found on QS2, create the stream with the same name before proceed with the app!'
                    logger.info(f"app:{app_info['app_name_qs']:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
                    return False

            elif len(res) > 1:
                msg = (
                    f"found {len(res)} published apps on QS2!",
                    f"delete unnecessary apps from QS2!",
                    f"the last one published will be updated on QS2!"
                )
                logger.info(f"app:{app_info['app_name_qs']:{app_indent}} stage:{stage:{stage_indent}} : {msg[0]}")
                logger.info(f"app:{app_info['app_name_qs']:{app_indent}} stage:{stage:{stage_indent}} : {msg[1]}")
                logger.info(f"app:{app_info['app_name_qs']:{app_indent}} stage:{stage:{stage_indent}} : {msg[2]}")


                min_inx = max(
                    range(len(res)),
                    key=lambda i: datetime.fromisoformat((res[i]['publishTime'].replace('Z', '+00:00')))
                )

                app_info['app_name_qs2'] = res[min_inx]['name']
                app_info['app_id_qs2'] = res[min_inx]['id']
                app_info['stream_name_qs2'] = res[min_inx]['stream']['name']
                app_info['stream_id_qs2'] = res[min_inx]['stream']['id']
                app_info['is_published_on_qs2'] = res[min_inx]['published']

                return app_info

            else:
                msg = 'found on QS2'
                logger.info(f"app:{app_info['app_name_qs']:{app_indent}} stage:{stage:{stage_indent}} : {msg}")

                app_info['app_name_qs2'] = res[0]['name']
                app_info['app_id_qs2'] = res[0]['id']
                app_info['stream_name_qs2'] = res[0]['stream']['name']
                app_info['stream_id_qs2'] = res[0]['stream']['id']
                app_info['is_published_on_qs2'] = res[0]['published']

                return app_info

        else:
            msg = 'request error'
            logger.info(f"app:{app_info['app_name_qs']:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
            return False




# pprint.pprint(get_app_info('a722ac70-a471-4e19-8092-c04afeca8a0b'))

def get_stream_id_from_qs2_by_name(stream_name):
    stage = 'get stream id by name'

    filter = f"Name eq '{stream_name}'"
    url = 'https://qs2/hdr/qrs/stream'
    full_url = f"{url}?xrfkey={xrfkey}&filter={filter}"



    with requests.session() as Session:
        response = requests.get(full_url, headers=headers, verify=False)

        if response.status_code in (200, 201):

            res = json.loads(response.content.decode())

            stream_id = res[0]['id']
            stream_name = res[0]['name']
            return (stream_name, stream_id)

        else:
            return False