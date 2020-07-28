from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "expenses/index.html", {})


def expenses_page(request):
    return render(request, "expenses/expenses.html", {})


def post_expense(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            expense_amount = request.POST.get("amount")
            expense_date = request.POST.get("expense_date")
            expense_description = request.POST.get("description")
            expense_type = request.POST.get("expense_type")
            expense_author = request.username.user
            print(expense_type)

            expense_entry = Expense(
                amount=expense_amount,
                expense_date=expense_date,
                description=expense_description,
                expense_type=expense_type,
                author=User.objects.get(username=expense_author)
            )
            expense_entry.save()
        return redirect("/")

    else:
        return HttpResponseRedirect("/signup")
