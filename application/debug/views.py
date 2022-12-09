import importlib
import json
import logging
from importlib.util import find_spec

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render


def api_data(request):
    '''Отправляет запрос в БД и формирует ответ'''
    report_name = request.GET['name']

    # Загрузка обработчика
    if find_spec(f'debug.pages.{report_name}.handler'):
        script = importlib.import_module(f'debug.pages.{report_name}.handler')
    else:
        script = importlib.import_module(f'debug.pages.handler')

    # Запрос данных
    output_json = script.get_data(request)
    # try:
    #     output_json = script.get_data(request)
    # except Exception as error:
    #     logging.error(error)
    #     return HttpResponseBadRequest()

    return HttpResponse(json.dumps(output_json, ensure_ascii=False))


def api_page(request):
    '''Отправляет требуемую html-страницу отладки'''
    report_name = request.GET['name']

    # Загрузка обработчика
    module = f'debug.pages.{report_name}.handler'
    if not find_spec(module):
        module = 'debug.pages.handler'

    script = importlib.import_module(module)

    # Запрос контекста
    try:
        context = script.get_context()
    except:
        context = {}

    try:
        return render(request, f'{request.GET["name"]}/index.html', context=context)
    except:
        return HttpResponseBadRequest()


@login_required
def page_debug(request):
    '''Рендер главной страницы отладки'''
    return render(request, 'debug/index.html')
