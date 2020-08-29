from django.db import models
from datetime import datetime
from django.conf import settings


class Expense(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    expense_date = models.DateField(default=datetime.now, blank=True)
    description = models.CharField(max_length=100, blank=True)
    expense_type = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "Amount: ${} | Type: {} | Date: {}".format(self.amount, self.expense_type.title(), self.expense_date)
