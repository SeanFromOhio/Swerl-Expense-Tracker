from django.shortcuts import render


def index(request):
    return render(request, "expenses/index.html", {})


def post_expenses(request):
    return render(request, "expenses/expenses.html", {})
