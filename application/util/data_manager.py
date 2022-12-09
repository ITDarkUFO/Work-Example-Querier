import datetime
import decimal
import json
import logging
import os
from types import NoneType
from uuid import UUID

from server.models import DeputyGovernor, Minister, ReportKid
from util.parameters_collector import collect_parameter, getCurators

from application.settings import BASE_DIR


def pack_to_json(data: list, app_name: str, report_name: str) -> dict:
    '''
    Форматирует данные таблицы и упаковывает вместе с заголовками в json.

    ## Параметры
    - data: Данные для упаковывания
    - app_name: Название приложения
    - report_name: Название отчета

    app_name и report_name используются только для получения заголовков при построении отчета.
    '''
    output_json = {}

    # Упаковка заголовков
    if app_name and report_name:
        headings_path = f'{BASE_DIR}/{app_name}/pages/{report_name}/headings.json'

        if os.path.exists(headings_path):
            with open(headings_path, 'r', encoding='utf-8') as f:
                column_data = json.load(f)
                output_json['columns'] = column_data['columns']
        else:
            logging.warning(
                f'Список заголовков для таблицы {app_name}/{report_name} не был найден.')
    else:
        logging.warning('Путь до заголовков таблицы не был задан.')

    # Форматирование данных
    data_list = []

    for entity_data in data:
        entity = []

        for property_data in entity_data:
            property = {}
            property_type = type(property_data)

            if property_type is NoneType:
                property['value'] = '-'

            elif property_type in (str, UUID):
                if property_data:
                    property['value'] = str(property_data)
                else:
                    property['value'] = '-'

            elif property_type in (decimal.Decimal, float, int):
                if property_data == 0:
                    property['value'] = 0
                elif property_data - int(property_data) == 0:
                    property['value'] = int(property_data)
                else:
                    property['value'] = float(property_data)

            elif property_type is datetime.datetime:
                property['value'] = property_data.strftime('%d.%m.%y %H:%M:%S')

            elif property_type is datetime.date:
                property['value'] = property_data.strftime('%d.%m.%y')

            elif property_type is datetime.time:
                property['value'] = property_data.strftime('%H:%M:%S')

            elif property_type is datetime.timedelta:
                days = property_data.days
                hours, rem = divmod(property_data.seconds, 3600)
                minutes, seconds = divmod(rem, 60)
                property['value'] = f'{(days * 24) + hours}:{minutes}:{seconds}'

            elif property_type is list:
                if property_data:
                    property['value'] = [
                        ', '.join(item for item in property_data)]
                else:
                    property['value'] = '-'

            elif property_type is dict:
                if property_data:
                    output_str = ''

                    for item in property_data:
                        output_str += f'{item}: {property_data.get(item)};\n'

                    property['value'] = output_str
                else:
                    property['value'] = '-'

            entity.append(property)
        data_list.append(entity)
    output_json['data'] = data_list

    return output_json


def get_subreport_by_position(data: list, request) -> dict:
    '''
    Отсеивает сотрудников, не соответствующих выбранной в отчете должности.
    '''
    report_type = request.GET['position_input']

    if report_type != 'Все':
        if report_type == 'Заместители Губернатора':
            persons_uuid = collect_parameter(
                DeputyGovernor, 'person__uuid')

        elif report_type == 'Министры':
            persons_uuid = collect_parameter(Minister, 'person__uuid')

        output_data = []
        for person in data:
            person_uuid = person[0]
            if person_uuid in persons_uuid:
                output_data.append(person)

        return output_data

    return data


def recalculate_curators_data(executors_data: list, add_curators_assignments: bool = False) -> list:
    '''
    Пересчитывает КИД и количество поручений у кураторов.
    
    ## Параметры
    - executors_data: Список исполнителей
    - add_curators_assignments: Указатель, добавлять ли поручения подчиненного куратору
    '''
    # Словарь для уменьшения количества прохождений
    executors_dict = {}

    for executor in executors_data:
        executor_uuid = executor[0]
        executors_dict[executor_uuid] = executor

    # Получение словаря кураторов со списками их подчиненных
    curators_data = getCurators()

    while curators_data:
        only_dependants = True

        for curator_uuid in curators_data.copy():
            dependant_curators = set(
                curators_data[curator_uuid]).intersection(curators_data)

            # Если ни один из подчиненных сам не является куратором
            if not dependant_curators:
                only_dependants = False

                for dependant_uuid in curators_data[curator_uuid]:
                    __recalculate_curator_data(
                        executors_dict, curator_uuid, dependant_uuid, add_curators_assignments)

                curators_data.pop(curator_uuid)

        if only_dependants:
            logging.warning(
                'В таблице "Кураторы КИД" (CuratorsKid) был обнаружен цикл, количество поручений кураторов из цикла не было изменено.')
            break

    return executors_data


def __recalculate_curator_data(executors_dict: dict, curator_uuid, dependant_uuid, add_curators_assignments):
    '''
    Служебная функция для пересчета данных куратора.
    
    ## Параметры
    - executors_dict: Словарь исполнителей
    - curator_uuid: UUID куратора
    - dependant_uuid: UUID подчиненного
    - add_curators_assignments: Указатель, добавлять ли поручения подчиненного куратору
    '''
    if add_curators_assignments:
        # Добавление куратору поручений подчиненного
        for i in range(2, len(executors_dict[curator_uuid]) - 1):
            if type(executors_dict[curator_uuid][i]) in (NoneType, int, float, decimal.Decimal):
                curator_field = executors_dict[curator_uuid][i] or 0
                dependant_field = executors_dict[dependant_uuid][i] or 0
                executors_dict[curator_uuid][i] = (
                    curator_field + dependant_field) or None

            elif type(executors_dict[curator_uuid][i]) is dict:
                curator_field = executors_dict[curator_uuid][i] or {}
                dependant_field = executors_dict[dependant_uuid][i] or {}

                for coefficient in dependant_field:
                    if coefficient not in curator_field:
                        curator_field[coefficient] = []

                    curator_field[coefficient].extend(
                        dependant_field[coefficient])

                executors_dict[curator_uuid][i] = curator_field

    # Замена значения КИД куратора на минимальное из значений куратора и подчиненного
    if executors_dict[curator_uuid][-1] is None:
        curator_kid = 1
    else:
        curator_kid = executors_dict[curator_uuid][-1]
    dependant_kid = executors_dict[dependant_uuid][-1]

    if dependant_kid and curator_kid >= dependant_kid:
        executors_dict[curator_uuid][-1] = dependant_kid


def remove_not_executors(data: list) -> list:
    '''Убирает из отчета сотрудников, не являющихся исполнителями.'''
    executors_uuid = collect_parameter(ReportKid, 'person__uuid')
    output_data = []

    for person in data:
        person_uuid = person[0]

        if person_uuid in executors_uuid:
            output_data.append(person)

    return output_data


def remove_uuid(data: list) -> list:
    '''Убирает все поля с типом UUID из отчета.'''
    for i in range(len(data)):
        entity = []
        entity_data = data[i]

        for j in range(len(entity_data)):
            if type(entity_data[j]) is not UUID:
                entity.append(entity_data[j])

        data[i] = entity

    return data


def calculate_kid(executors_data: list, pns_data: list) -> dict:
    '''Рассчитывает ПНС и КИД сотрудников.'''
    output_data = dict()

    # Рассчитываем пнс
    for person_data in pns_data:
        person_uuid = person_data[0]
        overdue_assignments_list = person_data[2]
        coefficient = person_data[3] or 1

        if person_uuid not in output_data:
            output_data[person_uuid] = {'pns': 0, 'kid': 0}

        if (overdue_assignments_list):
            for assignment in overdue_assignments_list:
                # Парсим "число поручений/количество дней" в две переменные
                assignments_count = int(assignment[:assignment.find('/')])
                days_count = int(assignment[assignment.find('/')+1:])

                old_pns = output_data.get(person_uuid).get('pns') or 0
                pns = pow(pow(0.5, days_count), coefficient) * \
                    assignments_count
                output_data[person_uuid]['pns'] = old_pns + pns

        if output_data[person_uuid]['pns'] == 0:
            output_data[person_uuid]['pns'] = None
        elif output_data[person_uuid]['pns'] is not None:
            output_data[person_uuid]['pns'] = round(
                output_data[person_uuid]['pns'], 3)

    # Рассчитываем КИД
    for i in range(len(executors_data)):
        person_data = list(executors_data[i])

        person_uuid = person_data[0]
        assignments_count = int(person_data[2] or 0)
        done_assignments_count = int(person_data[3] or 0)
        pns = output_data[person_uuid].get('pns') or 0

        kid = round((done_assignments_count + pns) /
                    assignments_count, 2) if assignments_count else None

        output_data[person_uuid]['kid'] = kid

    return output_data


def add_kid_data(executors_data: list, kid_data: dict, add_pns: bool, add_kid: bool) -> list:
    '''Добавляет данные ПНС и КИД в отчет.'''
    output_data = []

    for person in executors_data:
        person = list(person)
        person_uuid = person[0]

        if add_pns:
            pns = kid_data.get(person_uuid).get('pns')
            person.append(pns)

        if add_kid:
            kid = kid_data.get(person_uuid).get('kid')
            person.append(kid)

        output_data.append(person)

    return output_data


def add_overdue_assignment(executors_data: list, pns_data: list, insert_position: int = 5) -> list:
    '''Добавляет список просроченных поручений отчет.'''
    overdue_assignments_dict = {}

    for person in pns_data:
        person_uuid = person[0]
        overdue_assignments = person[2]
        coefficient = person[3] or 1

        if person_uuid not in overdue_assignments_dict:
            overdue_assignments_dict[person_uuid] = dict()

        if overdue_assignments:
            if coefficient not in overdue_assignments_dict.get(person_uuid):
                overdue_assignments_dict.get(person_uuid)[coefficient] = []

            overdue_assignments_dict.get(person_uuid).get(
                coefficient).extend(overdue_assignments)

    output_data = []

    for executor in executors_data:
        executor_uuid = executor[0]
        assignment_dict = overdue_assignments_dict.get(executor_uuid) or {}

        executor.insert(insert_position, assignment_dict)
        output_data.append(executor)

    return output_data


def concat_overdue_assignments(executors_data: list, dict_position: int = 5) -> list:
    '''Заменяет словарь просроченных поручений на строку.'''
    output_data = []

    for executor in executors_data:
        concat_string = ''
        for coefficient in executor[dict_position]:
            concat_string += f'{coefficient}: ' + ', '.join(
                x for x in executor[dict_position][coefficient]) + ';\n'

        executor[dict_position] = concat_string

        output_data.append(executor)

    return output_data


def make_links(cards_data, cards_type, uuid_position: int, name_position: int):
    '''Создает HTML ссылки на карточки.'''
    for i in range(len(cards_data)):
        card = list(cards_data[i])

        create_link = True
        if cards_type == 'assignment':
            link = 'https://application_url_example.com/app/open?screen=task.edit&item=task-'
        elif cards_type == 'document':
            create_link = False
        else:
            create_link = False
            logging.warning(
                'Указан неподдерживаемый тип документа. Ссылка не была создана.')

        if create_link:
            card[name_position] = f'<a href="{link + str(card[uuid_position])}" target=_blank>{card[name_position]}</a>'
            cards_data[i] = card

    return cards_data
