from util.data_manager import pack_to_json, remove_uuid
from util.parameters_collector import init
from util.queries import execute_sql


def get_data(request):
    parameters = init(request)

    app_name = 'server'
    report_name = request.GET['name']

    data = execute_sql(app_name, report_name, parameters)
    
    output_json = pack_to_json(data, app_name, report_name)

    return output_json
