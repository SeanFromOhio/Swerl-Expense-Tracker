from django import forms


class BudgetForm(forms.Form):
    weekly_spending_total = forms.DecimalField(
        label="Weekly Spending Budget:", max_digits=11, min_value=0, decimal_places=2)
    weekly_food = forms.DecimalField(
        label="Food Expense Budget:", max_digits=11, min_value=0, decimal_places=2)
    weekly_personal = forms.DecimalField(
        label="Personal Expense Budget:", max_digits=11, min_value=0, decimal_places=2)
    weekly_transportation = forms.DecimalField(
        label="Transportation Expense Budget:", max_digits=11, min_value=0, decimal_places=2)
    weekly_housing = forms.DecimalField(
        label="Housing Expense Budget:", max_digits=11, min_value=0, decimal_places=2)
    weekly_other = forms.DecimalField(
        label="Other Expense Budget:", max_digits=11, min_value=0, decimal_places=2)

