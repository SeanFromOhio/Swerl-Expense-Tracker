from django.shortcuts import render, redirect
from expenses.models import Expense
from budget.models import Budget
from django.contrib.auth.models import User
from datetime import datetime


def profile_page(request):
    author_id = request.user.id
    user_expenses = Expense.objects.filter(author=author_id).order_by("-expense_date")[:10]
    user_budgets = Budget.objects.filter(author=author_id).last()
    print(user_budgets)
    user_name = request.user.username
    context = {
        "user_expenses": user_expenses,
        "user_name": user_name,
        "current_date": datetime.now().date(),
        "user_budgets": user_budgets,
    }
    return render(request, "swerl_profile/swerl_profile.html", context)


def post_expense(request):
    if request.user.username:
        if request.method == "POST":

            expense_amount = request.POST.get("expense_amount")
            expense_date = request.POST.get("custom_date")
            expense_description = request.POST.get("description")
            expense_type = request.POST.get("expense_type")
            expense_author = request.user.username

            expense_call = Expense()
            expense_call.amount = expense_amount
            if expense_date:
                expense_call.expense_date = expense_date
            expense_call.description = expense_description
            expense_call.expense_type = expense_type
            expense_call.author = User.objects.get(username=expense_author)

            expense_call.save()
            return redirect("/profile/")
