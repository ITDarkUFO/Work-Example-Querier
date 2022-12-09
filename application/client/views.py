import os

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render


def page_home(request):
    '''Рендер основной страницы приложения'''
    return render(request, 'home/index.html')


def page_login(request):
    '''Рендер страницы входа в систему'''
    if request.GET.get('next'):
        next = request.GET.get('next')
    else:
        next = '/'

    if request.user.is_authenticated:
        return redirect(next)

    if request:
        if request.POST.get('remember-me') == 'on':
            request.session.set_expiry(2678400)
        else:
            request.session.set_expiry(0)

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if request.POST.get('next'):
            next = request.POST.get('next')

        if user:
            login(request, user)
            if next:
                return redirect(next)

    if next == '/':
        next = ''

    return render(request, 'login/index.html', {'next': next})


def page_logout(request):
    logout(request)
    return redirect('/')


def page_docs(request):
    filename = 'docs_file_name.docx'
    file_path = 'docs/'
    full_path = os.path.join(settings.STATIC_DIR, file_path, filename)
    if os.path.exists(full_path):
        with open(full_path, 'rb') as fh:
            response = HttpResponse(fh.read(
            ), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'inline; filename=' + filename
            return response
    raise Http404
