from django.db import models

# Create your models here.
class AgentData(models.Model):
    hostname = models.CharField(max_length=200)
    data = models.JSONField()   # requires Django 3.1+, stores system+process info
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hostname} @ {self.created_at}"