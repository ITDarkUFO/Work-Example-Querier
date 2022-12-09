from server.models import ExcludedOrganizations
from util.data_manager import pack_to_json
from util.parameters_collector import collect_parameter, init
from util.queries import execute_sql


def get_data(request):
    parameters = init(request)
    parameters.update(collect_parameter(ExcludedOrganizations,
                      'name', 'excluded_organizations'))

    app_name = 'server'
    report_name = request.GET['name']

    data = execute_sql(app_name, report_name, parameters)

    output_json = pack_to_json(data, app_name, report_name)

    return output_json
