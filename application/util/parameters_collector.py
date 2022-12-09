'''
Файл с методами получения параметров из моделей Django и страниц отчетов.
Методы используются в handler.py файлах в папках отчетов.
'''
from server.models import AssignmentsSources, CuratorsKid, Person


def collect_parameter(model, query, parameter_name=None) -> dict:
    '''
    Собирает указанный параметр из всех объектов модели.

    Обрабатывает только простые запросы (получение параметра напрямую из модели).

    ### Параметры
    - model: Модель из server.models
    - query: Запрос к модели
    - parameter_name: Название заголовка для упаковки в словарь
    '''
    output = {}

    if parameter_name:
        model_data = model.objects.all().values_list(query)

        data = []
        for parameter in model_data:
            data.insert(0, parameter[0])

        output[parameter_name] = tuple(data)
    else:
        output = model.objects.all().values_list(query, flat=True)

    return output


def getAssignmentsSources() -> dict:
    '''
    Собирает словарь источников поручений с учетов их коэффициента значимости.
    '''
    output = {}

    assignments_sources_data = AssignmentsSources.objects.all(
    ).values_list('assignment_source', 'coefficient')

    assignments_sources_1 = []
    assignments_sources_2 = []
    assignments_sources_3 = []

    for source in assignments_sources_data:
        if source[1] == 1:
            assignments_sources_1.append(source[0])
        elif source[1] == 2:
            assignments_sources_2.append(source[0])
        elif source[1] == 3:
            assignments_sources_3.append(source[0])

    output['assignments_sources_1'] = tuple(assignments_sources_1)
    output['assignments_sources_2'] = tuple(assignments_sources_2)
    output['assignments_sources_3'] = tuple(assignments_sources_3)

    return output


def getCurators() -> dict:
    '''
    Собирает словарь кураторов со списками их подчиненных

    ### Возвращает
    - Dict(UUID куратора: [UUID подчиненного, UUID подчиненного,..])
    '''
    output = {}

    curators_uuid = collect_parameter(CuratorsKid, 'curator__uuid')

    for curator_uuid in curators_uuid:
        if curator_uuid not in output:
            output[curator_uuid] = []

        dependants_uuid = CuratorsKid.objects.filter(
            curator=Person.objects.get(uuid=curator_uuid)).values_list('dependants__uuid', flat=True)

        for dependant_uuid in dependants_uuid:
            output[curator_uuid].append(dependant_uuid)

    return output


def init(request) -> dict:
    '''Создает словарь и заполняет параметрами из GET запроса.'''
    parameters = {}

    for parameter in request.GET:
        if parameter != 'name':
            parameters[parameter] = request.GET[parameter]

    return parameters
