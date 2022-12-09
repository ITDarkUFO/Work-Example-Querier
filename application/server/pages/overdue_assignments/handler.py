from server.models import AssignmentsInitiators, ReportKid
from util.data_manager import make_links, pack_to_json, remove_uuid
from util.parameters_collector import (collect_parameter,
                                       getAssignmentsSources, init)
from util.queries import execute_sql


def get_data(request):
    parameters = init(request)
    parameters.update(collect_parameter(AssignmentsInitiators,
                      'person__uuid', 'initiators_list'))
    parameters.update(getAssignmentsSources())

    app_name = 'server'
    report_name = request.GET['name']

    data = execute_sql(app_name, report_name, parameters)
    data = make_links(data, 'assignment', 0, 1)
    data = remove_uuid(data)
    
    output_json = pack_to_json(data, app_name, report_name)

    return output_json


def get_context():
    context = {}
    executors = ReportKid.objects.all()
    context.update({'executors': executors})

    return context