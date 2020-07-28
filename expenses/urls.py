from django.urls import path
from .views import index, expenses_page, post_expense

app_name = "expenses_paths"
urlpatterns = [
    path("", index, name="landing_page"),
    path("expenses/", expenses_page, name="expenses_page"),
    path("write-expense/", post_expense, name="post_function"),
]
