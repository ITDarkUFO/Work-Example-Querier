from server.models import AssignmentsInitiators, Person
from util.data_manager import (get_subreport_by_position, pack_to_json,
                               remove_not_executors, remove_uuid)
from util.parameters_collector import (collect_parameter,
                                       getAssignmentsSources, init)
from util.queries import execute_sql


def get_data(request):
    parameters = init(request)
    parameters.update(collect_parameter(Person, 'uuid', 'kid_executors'))
    parameters.update(collect_parameter(AssignmentsInitiators,
                      'person__uuid', 'initiators_list'))
    parameters.update(getAssignmentsSources())

    app_name = 'debug'
    report_name = request.GET['name']

    data = execute_sql(app_name, report_name, parameters)
    data = remove_not_executors(data)
    data = get_subreport_by_position(data, request)
    data = remove_uuid(data)

    output_json = pack_to_json(data, app_name, report_name)

    return output_json
