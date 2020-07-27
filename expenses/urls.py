from django.urls import path
from expenses.views import index, post_expenses

app_name = "expenses_paths"
urlpatterns = [
    path("", index, name="landing_page"),
    path("expenses/", post_expenses, name="expenses_page"),
]
