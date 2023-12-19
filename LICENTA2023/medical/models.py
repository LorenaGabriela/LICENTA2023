from django.contrib.auth.models import User
from django.db import models


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
