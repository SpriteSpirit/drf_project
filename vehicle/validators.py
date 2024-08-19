import re

from rest_framework.serializers import ValidationError


class TitleValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('^[a-zA-Z0-9\.\-\ ]+$')
        tmp_value = dict(value).get(self.field)

        if not bool(reg.match(tmp_value)):
            raise ValidationError('В названии недопустимые символы')
