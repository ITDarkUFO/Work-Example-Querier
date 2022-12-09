from server.models import ReportKid
from util.data_manager import pack_to_json
from util.parameters_collector import collect_parameter, init
from util.queries import execute_sql


def get_data(request):
    parameters = init(request)
    parameters.update(collect_parameter(
        ReportKid, 'person__uuid', 'kid_executors'))

    app_name = 'debug'
    report_name = request.GET['name']

    data = execute_sql(app_name, report_name, parameters)

    output_json = pack_to_json(data, app_name, report_name)

    return output_json
