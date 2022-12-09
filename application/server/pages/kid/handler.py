from server.models import AssignmentsInitiators, Person
from util.data_manager import (add_kid_data, calculate_kid, get_subreport_by_position,
                               pack_to_json, recalculate_curators_data,
                               remove_not_executors, remove_uuid)
from util.parameters_collector import (collect_parameter,
                                       getAssignmentsSources, init)
from util.queries import execute_sql


def get_data(request):
    parameters = init(request)

    parameters.update(collect_parameter(
        Person, 'uuid', 'kid_executors'))
    parameters.update(collect_parameter(AssignmentsInitiators,
                      'person__uuid', 'initiators_list'))
    parameters.update(getAssignmentsSources())

    app_name = 'server'
    report_name = request.GET['name']

    executors_data = execute_sql(app_name, report_name, parameters)
    pns_data = execute_sql('debug', 'd_overdue_assignments', parameters)

    kid_data = calculate_kid(executors_data, pns_data)
    executors_data = add_kid_data(executors_data, kid_data, False, True)
    executors_data = recalculate_curators_data(executors_data, False)
    executors_data = remove_not_executors(executors_data)
    executors_data = get_subreport_by_position(executors_data, request)
    executors_data = remove_uuid(executors_data)

    output_json = pack_to_json(executors_data, app_name, report_name)

    return output_json
