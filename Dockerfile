FROM python:3

ENV PYTHONBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR /

COPY ./application /

COPY  ./www/static /www/static

RUN pip install -r ./requirements.txt

CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000"]