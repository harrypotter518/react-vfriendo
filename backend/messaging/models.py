from django.db import models


class Message(models.Model):
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contents
