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
    date_created = models.DateField(null=False)

    def __str__(self):
        return self.entry_title


class Tag(models.Model):
    """
    Tags that can be used for more subtle Filtering than category.
    """
    entry_id = models.ForeignKey(Entry, on_delete=models.CASCADE)
    tag = models.TextField()

    def __str__(self):
        """
        Updated magic method to show the entries id, and tag.
        """
        return f'{self.entry_id}__{self.tag}'
