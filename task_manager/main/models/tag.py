from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return f"Tag(title={self.title})"
