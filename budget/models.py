from django.db import models
from django.conf import settings


class Budget(models.Model):
    weekly_spending_total = models.DecimalField(max_digits=11, decimal_places=2)
    weekly_food = models.DecimalField(max_digits=11, decimal_places=2)
    weekly_personal = models.DecimalField(max_digits=11, decimal_places=2)
    weekly_transportation = models.DecimalField(max_digits=11, decimal_places=2)
    weekly_housing = models.DecimalField(max_digits=11, decimal_places=2)
    weekly_other = models.DecimalField(max_digits=11, decimal_places=2)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - Spending Total: ${}".format(self.author, self.weekly_spending_total)
