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
        wk_expenses_tup = Expense.objects.filter(
            author=author_id).filter(
            expense_date__week=current_wk).aggregate(Sum("amount"))
        wk_expenses = wk_expenses_tup["amount__sum"]

        # Calculates the difference between total spent that week and set total budget per week.
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
