from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import Sum
from datetime import datetime
from plotly.graph_objs import Pie, Scatter, Figure
from plotly.offline import plot


def index(request):
    current_date = datetime.now().date()
    return render(request, "expenses/index.html", {"current_date": current_date})


def expenses_page(request):
    author_id = request.user.id
    user_expenses = Expense.objects.filter(author=author_id).order_by("-expense_date")
    user_name = request.user.username

    # ----------- CHARTS ------------

    # Expense pie chart
    food_amount = Expense.objects.filter(expense_type="food").\
        filter(author=author_id).aggregate(Sum("amount"))
    personal_amount = Expense.objects.filter(expense_type="personal").\
        filter(author=author_id).aggregate(Sum("amount"))
    transportation_amount = Expense.objects.filter(expense_type="transportation").\
        filter(author=author_id).aggregate(Sum("amount"))
    housing_amount = Expense.objects.filter(expense_type="housing").\
        filter(author=author_id).aggregate(Sum("amount"))
    other_amount = Expense.objects.filter(expense_type="other").\
        filter(author=author_id).aggregate(Sum("amount"))

    # Names of the pie chart segments
    groups = ["Food", "Personal", "Transportation", "Housing", "Other"]

    # Amounts of the pie chart segments
    amounts = [food_amount["amount__sum"], personal_amount["amount__sum"], transportation_amount["amount__sum"],
               housing_amount["amount__sum"], other_amount["amount__sum"]]

    # Segment colors
    colors = ["#C0ECCC", "#F6A8A6", "#F9F0C1", "#A5C8E4", "#F4CDA6"]

    # Custom '$'
    text = ["$", "$", "$", "$", "$"]

    # The plot creator
    pie_plot = Figure(Pie(
                    labels=groups, values=amounts,
                    hoverinfo="label+percent", text=text, textinfo="text+value",
                    textfont=dict(size=15), title="Mouseover %",
                    hole=.3,
                    marker=dict(colors=colors,
                                line=dict(color="#000000", width=3)
                                )))

    # This is needed to view the plot in a localized setting (not online)
    plot_div = plot(pie_plot, output_type="div")

    context = {
        "user_expenses": user_expenses,
        "user_name": user_name,
        "plot_div": plot_div,
    }
    return render(request, "expenses/expenses.html", context)


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
            return redirect("/")

    else:
        return HttpResponseRedirect("/signup")

