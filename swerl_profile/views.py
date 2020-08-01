from django.shortcuts import render
from expenses.models import Expense


def profile_page(request):
    author_id = request.user.id
    user_expenses = Expense.objects.filter(author=author_id).order_by("-expense_date")[:10]
    user_name = request.user.username
    context = {
        "user_expenses": user_expenses,
        "user_name": user_name,
    }
    return render(request, "swerl_profile/swerl_profile.html", context)
