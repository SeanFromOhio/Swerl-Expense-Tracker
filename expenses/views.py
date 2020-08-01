from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "expenses/index.html", {})


def expenses_page(request):
    author_id = request.user.id
    user_expenses = Expense.objects.filter(author=author_id).order_by("-expense_date")
    user_name = request.user.username
    context = {
        "user_expenses": user_expenses,
        "user_name": user_name,
    }
    return render(request, "expenses/expenses.html", context)


def post_expense(request):
    if request.user.username:
        if request.method == "POST":

            expense_amount = request.POST.get("expense_amount")
            # expense_date = request.POST.get("expense_date")
            expense_description = request.POST.get("description")
            expense_type = request.POST.get("expense_type")
            expense_author = request.user.username

            expense_call = Expense()
            expense_call.amount = expense_amount
            # expense_call.expense_date = expense_date
            expense_call.description = expense_description
            expense_call.expense_type = expense_type
            expense_call.author = User.objects.get(username=expense_author)

            expense_call.save()
            return redirect("/")

    else:
        return HttpResponseRedirect("/signup")
