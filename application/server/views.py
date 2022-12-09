import importlib
import json
import logging
from importlib.util import find_spec

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render


def api_data(request):
    '''Отправляет запрос в БД и формирует ответ'''
    report_name = request.GET['name']

    # Загрузка обработчика
    module = f'server.pages.{report_name}.handler'
    if not find_spec(module):
        module = 'server.pages.handler'

    script = importlib.import_module(module)

    # Запрос данных
    output_json = script.get_data(request)
    # try:
    #     output_json = script.get_data(request)
    # except Exception as error:
    #     logging.error(error)
    #     return HttpResponseBadRequest()

    return HttpResponse(json.dumps(output_json, ensure_ascii=False))


def api_page(request):
    '''Отправляет требуемую html-страницу получения отчета'''
    report_name = request.GET['name']

    # Загрузка обработчика
    if find_spec(f'server.pages.{report_name}.handler'):
        script = importlib.import_module(f'server.pages.{report_name}.handler')
    else:
        script = importlib.import_module(f'server.pages.handler')

    # Запрос контекста
    try:
        context = script.get_context()
    except:
        context = {}

    try:
        return render(request, f'{request.GET["name"]}/index.html', context=context)
    except:
        return HttpResponseBadRequest()
