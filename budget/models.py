from django.db import models
from django.conf import settings


class Budget(models.Model):
    goal = models.DecimalField(max_digits=11, decimal_places=2)
    goal_type = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
