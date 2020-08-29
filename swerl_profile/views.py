from django.shortcuts import render, redirect
from expenses.models import Expense
from budget.models import Budget
from datetime import datetime
from django.http import HttpResponseRedirect
from django.db.models import Sum


def profile_page(request):
    if request.user.username:
        author_id = request.user.id
        user_expenses = Expense.objects.filter(author=author_id).order_by("-expense_date")[:10]
        user_budgets = Budget.objects.filter(author=author_id).last()
        user_name = request.user.username

        # Extracts the date (iso-week) from the DB and calculates the total expenses for that week.
        current_wk = datetime.now().isocalendar()[1]
        current_yr = datetime.now().isocalendar()[0]

        wk_expenses_tuple = Expense.objects.filter(
            author=author_id).filter(expense_date__year=current_yr).filter(
            expense_date__week=current_wk).aggregate(Sum("amount"))
        wk_expenses = wk_expenses_tuple["amount__sum"]

        # wk_expenses = None, if the user hasn't input an expense for that week, causing an error.
        if wk_expenses is None:
            wk_expenses = 0

        # Calculates the difference between total spent that week and set total budget per week.
        # Checks if the user set up spending limits
        if user_budgets is None:
            budget_difference = 0
        else:
            budget_difference = abs(user_budgets.weekly_spending_total - wk_expenses)

        context = {
            "user_expenses": user_expenses,
            "user_name": user_name,
            "current_date": datetime.now().date(),
            "user_budgets": user_budgets,
            "wk_expenses": wk_expenses,
            "budget_difference": budget_difference,
        }
        return render(request, "swerl_profile/swerl_profile.html", context)

    else:
        return HttpResponseRedirect("/signup")


def account_page(request):
    user = request.user.username
    context = {
        "user": user,
    }
    return render(request, "swerl_profile/account.html", context)
