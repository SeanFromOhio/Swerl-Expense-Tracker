from django.urls import path
from .views import index, expenses_page, post_expense, post_budget, update_expense

app_name = "expenses_paths"
urlpatterns = [
    path("", index, name="landing_page"),
    path("expenses/", expenses_page, name="expenses_page"),
    path("write-expense/", post_expense, name="post_expenses"),
    path("write-budgets/", post_budget, name="post_budgets"),
    path("update-expense/", update_expense, name="update_expense"),
]
