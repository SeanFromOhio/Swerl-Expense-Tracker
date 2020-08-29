from django import forms
from .models import Expense

expense_type_choices = [
    ("food", "Food"), ("personal", "Personal"), ("transportation", "Transportation"),
    ("housing", "Housing"), ("other", "Other")
]


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"
        exclude = ("author",)

        widgets = {
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0.01",
                "placeholder": "0",
                "step": "0.01",
                "id": "update_expense_amount",
                "required": "True",
            }),
            "expense_date": forms.DateInput(attrs={
                "class": "form-control",
                "placeholder": "Ex. Dec. 30, 1995",
                "type": "date",
            }),
            "description": forms.TextInput(attrs={
                "class": "form-control",
                "id": "update_expense_description",
                "placeholder": "Optional description..."
            }),
            "expense_type": forms.Select(
                choices=expense_type_choices,
                attrs={
                    "class": "form-control",
                    "id": "update_expense_type",
                },
            ),
        }
