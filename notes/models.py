import datetime

from django.db import models


class Entry(models.Model):
    """
    Object Representing a Note or blog entry.
    """
    id = models.AutoField(primary_key=True)
    category = models.TextField(null=False)
    entry_content = models.TextField(null=False)
    entry_title = models.TextField()
    entry_description = models.TextField(blank=True)
    date_created = models.DateField(default=datetime.date)
