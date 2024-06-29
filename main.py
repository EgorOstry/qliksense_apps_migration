import os
from dotenv import load_dotenv
from procedure.app_single_procedure import run_app_procedure

if __name__ == "__main__":

    app_id='ce8401ab-4e9c-4557-a171-f83ed7e57a9d'
    load_dotenv(override=True)
    # app_id = os.getenv("app_id")
    run_procedure = run_app_procedure(app_id) #начало обработки