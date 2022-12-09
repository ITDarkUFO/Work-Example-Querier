from django import template
from django.conf import settings

register = template.Library()

# Пример шаблона
# @register.tag(name="temp") - если нужно
# @register.simple_tag(takes_context = True)
# def getInfo(context, temp):
# 	Тело функции

# Теги страниц генерации отчетов


@register.simple_tag()
def meta():
    static = settings.STATIC_URL

    return f'''
    <meta charset="utf-8">
    <title>ТЕЗИС - Генератор отчетов</title>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <meta name="sputnik-verification" content="sputnik_key"/>
    <link rel="shortcut icon" type="image/x-icon" href="{static}images/favicon.ico">
    <link rel="stylesheet" type="text/css" href="{static}css/main.css?modiifed=19102022">
    '''


@register.simple_tag()
def form_buttons():
    return f'''
    <div class="col-md-2">
        <button onclick="getReport()" class="mt-3 form-control">Получить отчет
            <div id="loading-icon" class="d-none spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Загрузка отчета...</span>
            </div>
        </button>
    </div>
    <div id="print-button" class="d-none col-md-2">
        <button onclick="saveReport()" class="mt-2 form-control">Сохранить отчет</button>
    </div>
    '''

@register.simple_tag()
def libs():
    static = settings.STATIC_URL

    return f'''
    <script src="{static}js/alert-system.js" charset="utf-8"></script>
    <script src="{static}js/page-rendering.js" charset="utf-8"></script>
    <script src="{static}js/report-printing.js" charset="utf-8"></script>
    <script src="{static}js/core.js" charset="utf-8"></script>

    <script src="{static}libs/cdnjs-xlsx/xlsx.extendscript.js" charset="utf-8"></script>
    <link href="{static}libs/bootstrap-5.2.0-dist/css/bootstrap.min.css?modiifed=05092022" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    <script src="{static}libs/bootstrap-5.2.0-dist/js/bootstrap.bundle.min.js?modiifed=05092022" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
    '''
