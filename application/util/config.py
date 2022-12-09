from enum import Enum
from django.conf import settings


class Status(Enum):
    BETA = 1
    PRODUCTION = 2


stage = Status.BETA


sql_config = None

if stage == Status.BETA:
    sql_config = settings.DATABASES['preproduction']
if stage == Status.PRODUCTION:
    sql_config = settings.DATABASES['production']
