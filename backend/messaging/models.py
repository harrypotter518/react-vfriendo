from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    contents = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contents
