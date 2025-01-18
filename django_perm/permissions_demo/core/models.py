from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ('toggle_document', 'Can change status document'),
        ]