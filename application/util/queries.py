import psycopg2
from util.config import sql_config

from application.settings import BASE_DIR


def execute_sql(app_name: str, report_name: str, parameters: dict = {}) -> list:
    '''
    Отправляет SQL запрос с подставленными параметрами на сервер.

    :param app_name: Название приложения
    :param report_name: Название отчета
    :param parameters: Параметры, подставляемые в отчет
    '''
    cur = psycopg2.connect(
        host=sql_config['HOST'],
        port=sql_config['PORT'],
        database=sql_config['NAME'],
        user=sql_config['USER'],
        password=sql_config['PASSWORD']
    ).cursor()

    file_path = f'{BASE_DIR}/{app_name}/pages/{report_name}/request.sql'

    sql_query = open(file_path, 'r', encoding='utf-8-sig').read()

    if parameters:
        cur.execute(sql_query, parameters)
    else:
        cur.execute(sql_query)

    data = cur.fetchall()
    cur.close()

    return data
