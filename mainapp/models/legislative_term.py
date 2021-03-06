from django.db import models

from .default_fields import DefaultFields, ShortableNameFields


class LegislativeTerm(DefaultFields, ShortableNameFields):
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.short_name
