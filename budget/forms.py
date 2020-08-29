from django import forms
from .models import Budget


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = "__all__"
        exclude = ("author",)

        widgets = {
            "weekly_spending_total": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0.01",
                "placeholder": "0",
                "step": "0.01",
            }),
            "weekly_food": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0.01",
                "placeholder": "0",
                "step": "0.01",
            }),
            "weekly_personal": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0.01",
                "placeholder": "0",
                "step": "0.01",
            }),
            "weekly_transportation": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0.01",
                "placeholder": "0",
                "step": "0.01",
            }),
            "weekly_housing": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0.01",
                "placeholder": "0",
                "step": "0.01",
            }),
            "weekly_other": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0.01",
                "placeholder": "0",
                "step": "0.01",
            })
        }
