import os
import time
import pandas as pd
from dotenv import load_dotenv

from procedure.logger import logger
from procedure.app_migration import migrate
from procedure.get_app_info import get_app_info
from procedure.app_export import app_export_step1, app_export_step_2
from procedure.app_import import initial_app_import, initial_app_publish, regular_app_import_replace


load_dotenv(override=True)

app_indent = int(os.getenv('app_indent'))
stage_indent = int(os.getenv('stage_indent'))

def run_app_procedure(app_id):

    procedure_start_time = time.time()

    results = dict()

    token = '060dcbca-4782-4f99-a7c4-767190e85355'  # рандомный uuid для отмены экспорта на 2 этапе, если отмена потребуется

    app_info = get_app_info(app_id)  # получение всей необходимой информации о приложении

    if not app_info:
        return False

    else:

        app_name = app_info['app_name_qs']
        app_id = app_info['app_id_qs']
        new_app_id = app_info['app_id_qs2']
        stream_name = app_info['stream_name_qs2']
        stream_id = app_info['stream_id_qs2']

        # Этап 1: Экспорт

        # Этап 1.1: Экспорт_1
        export_1_res = app_export_step1(app_name, app_id, token)
        if not export_1_res:
            return False
        results[f'{app_name}'] = {'1_Export_1': round(export_1_res[-1], 2)}

        # Этап 1.2: Экспорт_2
        export_2_res = app_export_step_2(*export_1_res[:-1])  # не берем последний элемент, это duration
        if not export_2_res:
            return False
        results[f'{app_name}']['2_Export_2'] = round(export_2_res[1], 2)

        # Этап 2: Копирование
        migrate_res = migrate(app_name, export_2_res[0])
        if not migrate_res:
            return False
        results[f'{app_name}']['3_Migration'] = round(migrate_res, 2)

        # Этап 3
        if new_app_id is None:
            # Этап 3.1: Импорт
            initial_app_import_res = initial_app_import(app_name, app_id)
            if not initial_app_import_res:
                return False
            results[f'{app_name}']['4_Import'] = round(initial_app_import_res[1], 2)

            # Этап 3.2: Публикация
            initial_app_publish_res = initial_app_publish(app_name, initial_app_import_res[0]['id'], stream_id)
            if not initial_app_publish_res:
                return False
            results[f'{app_name}']['5_Publish'] = round(initial_app_publish_res[1], 2)

        else:
            # Этап 3.1: Замена
            app_replace_res = regular_app_import_replace(app_name, app_id, new_app_id)
            if not app_replace_res:
                return False
            results[f'{app_name}']['6_Replace'] = round(app_replace_res[1], 2)




    procedure_end_time = time.time()
    duration = procedure_end_time - procedure_start_time

    stage = 'total'
    msg = f'completed successfully in {duration:.2f} sec'
    logger.info(f"app:{app_name:{app_indent}} stage:{stage:{stage_indent}} : {msg}")
    results[f'{app_name}']['7_Total'] = round(duration, 2)

    all_keys = set()

    for app_data in results.values():
        all_keys.update(app_data.keys())

    all_keys = list(all_keys)
    all_keys = sorted(all_keys)

    df = pd.DataFrame.from_dict(results, orient='index', columns=all_keys)
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Приложение'}, inplace=True)
    df.to_csv('results.csv', index=False, encoding='utf-8', sep=';')
    return True