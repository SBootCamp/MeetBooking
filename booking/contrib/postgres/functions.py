from django.contrib.postgres.fields import DateTimeRangeField
from django.db import models


class TsTzRange(models.Func):
    function = 'TSTZRANGE'
    output_field = DateTimeRangeField()
