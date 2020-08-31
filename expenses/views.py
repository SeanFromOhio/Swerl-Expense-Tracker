from django.shortcuts import render, redirect
from .models import Expense
from expenses.forms import ExpenseForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import Sum
from datetime import datetime, date, timedelta
from plotly.graph_objs import Pie, Scatter, Figure, Bar
from plotly.offline import plot
from budget.forms import BudgetForm
from budget.models import Budget
import pandas as pd


def index(request):
    current_date = datetime.now().date()
    return render(request, "expenses/index.html", {"current_date": current_date})


def expenses_page(request):
    if request.user.username:
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
        # colors = ["#C0ECCC", "#F6A8A6", "#F9F0C1", "#A5C8E4", "#F4CDA6"]  # Pastel colors
        colors = ["#5cb85c", "#d9534f", "#f5e83b", "#0275d8", "#f0ad4e"]  # Bootstrap colors

        # Custom '$'
        text = ["$", "$", "$", "$", "$"]

        # The plot creator
        pie_plot = Figure(Pie(
                        labels=groups, values=amounts,
                        hoverinfo="label+percent", text=text, textinfo="text+value",
                        textfont=dict(size=15),
                        hole=.3,
                        marker=dict(colors=colors,
                                    line=dict(color="#000000", width=3)
                                    ),
        ))

        pie_plot.update_layout(
            legend=dict(
                orientation="v",
            ),
            title={
                'text': "Overall Expenses per Type",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            },
            # showlegend=False,
        )

        # This is needed to view the plot in a localized setting (not online)
        plot_div = plot(pie_plot, output_type="div")

    # Line Plot
        # Pandas dataframe of expense model
        expense_user_data = Expense.objects.filter(author=author_id).all().values()
        data = pd.DataFrame(expense_user_data)
        # Converting my dates to accepted Pandas datetime
        data["expense_date"] = pd.to_datetime(data["expense_date"])
        # Indexing via date
        data.set_index("expense_date", inplace=True)
        # Sorting by date
        data = data.sort_values(by=["expense_date"])
        # Converting data from daily to weekly and summing the amounts per week
        scatter_plot_data = data.resample("W-MON").agg({"amount": "sum", "expense_type": " - ".join})

        if Budget.objects.filter(author=author_id).last():
            budget_data = Budget.objects.filter(author=author_id).last()
            budget_line = budget_data.weekly_spending_total
        else:
            budget_line = None

        trace_wk_tot = Scatter(
            x=scatter_plot_data.index,
            y=scatter_plot_data.amount,
            mode="lines+markers",
            name="lines+markers",
            line=dict(
                color="#5cb85c",
                width=4,
            ),
            marker=dict(
                size=12,
            )
        )

        expense_weekly_data = [trace_wk_tot]  # This format in case adding additional traces

        line_plot = Figure(expense_weekly_data)  # Line plot instance

        # Total Budget per week line for comparison
        if budget_line:
            line_plot.add_shape(
                type="line",
                x0=scatter_plot_data.index.min(),
                y0=budget_line,
                x1=scatter_plot_data.index.max(),
                y1=budget_line,
                line=dict(
                    color="#d9534f",
                    width=2,
                    dash="dash",
                ),
            )

        line_plot.update_layout(
            xaxis_title="Time (Weeks)",
            yaxis_title="Total Spent ($)",
            font=dict(
                size=14,
            ),
            yaxis_tickformat="$",
            title={
                'text': "Total Expenses per Week",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            },
            yaxis={"rangemode": "tozero"},
        )
        plot_div_line = plot(line_plot, output_type="div")

    # Bar Chart
        # Gather data: each expense type and associated budget limit via Pandas
        # expense_type filters
        food_filter = (data["expense_type"] == "food")
        personal_filter = (data["expense_type"] == "personal")
        transportation_filter = (data["expense_type"] == "transportation")
        housing_filter = (data["expense_type"] == "housing")
        other_filter = (data["expense_type"] == "other")

        # expense_date (Current Week) filter
        previous_monday = date.today() - timedelta(days=date.today().weekday())
        next_monday = previous_monday + timedelta(weeks=1)

        week_filter = ((data.index >= pd.to_datetime(previous_monday)) & (data.index < pd.to_datetime(next_monday)))

        # Split Current Week data up into expense_type
        # Pulls the "amount" data based on the above filters and then sums them for the week
        week_food_amt = data["amount"].loc[week_filter & food_filter].sum()
        week_personal_amt = data["amount"].loc[week_filter & personal_filter].sum()
        week_transportation_amt = data["amount"].loc[week_filter & transportation_filter].sum()
        week_housing_amt = data["amount"].loc[week_filter & housing_filter].sum()
        week_other_amt = data["amount"].loc[week_filter & other_filter].sum()

        spending_array = [week_food_amt, week_personal_amt, week_transportation_amt,
                          week_housing_amt, week_other_amt]

        # Budget Type Limits
        if Budget.objects.filter(author=author_id).last():
            budget_data = Budget.objects.filter(author=author_id).last()

            budget_food = budget_data.weekly_food
            budget_personal = budget_data.weekly_personal
            budget_transportation = budget_data.weekly_transportation
            budget_housing = budget_data.weekly_housing
            budget_other = budget_data.weekly_other
        else:
            budget_food = None
            budget_personal = None
            budget_transportation = None
            budget_housing = None
            budget_other = None

        budget_array = [budget_food, budget_personal, budget_transportation, budget_housing, budget_other]

        # Graph the bar chart
        types = ["Food", "Personal", "Transport", "Housing", "Other"]

        bar_trace = [Bar(name="Expense Totals", x=types, y=spending_array, marker_color=colors,
                         text=spending_array, textposition="auto", showlegend=False),
                     Bar(name="Budget Limits", x=types, y=budget_array, marker_color="#cfb3ff")
                     ]

        bar_chart = Figure(bar_trace)
        bar_chart.update_layout(
            barmode="group",
            yaxis_title="Total Spent ($)",
            yaxis_tickformat="$",
            title={
                'text': "Total Expenses vs Budget Limits per Week",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            },
            legend=dict(
                orientation="h",
            ),
            # showlegend=False,
        )

        # Add the chart to the context and plot in html
        plot_div_bar = plot(bar_chart, output_type="div")

# Budget Form Instance
        if Budget.objects.last():
            budget_info = Budget.objects.last()
            budgetform = BudgetForm(instance=budget_info)
        else:
            budgetform = BudgetForm()

# Update Expense Form
        if Expense.objects.last():
            # expense_info = Expense.objects.get(id=pk)
            # expenseform = ExpenseForm(instance=expense_info)
            expenseform = ExpenseForm()
        else:
            expenseform = ExpenseForm()

        context = {
            "user_expenses": user_expenses,
            "user_name": user_name,
            "plot_div": plot_div,
            "plot_div_line": plot_div_line,
            "plot_div_bar": plot_div_bar,
            "budgetform": budgetform,
            "expenseform": expenseform,
            "current_date": datetime.now().date(),
        }
        return render(request, "expenses/expenses.html", context)

    else:
        return HttpResponseRedirect("/signup")


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

    else:
        return HttpResponseRedirect("/signup")


def post_budget(request):
    if Budget.objects.last():
        budget_info = Budget.objects.last()
    else:
        budgetform = BudgetForm()

    if request.user.username:
        if request.method == "POST":
            author = Budget(author=request.user)
            budgetform = BudgetForm(request.POST, instance=author)
            if budgetform.is_valid():
                author.save()
                return redirect("/profile/")

            else:
                budgetform = BudgetForm(instance=budget_info)

            return render(request, 'expenses.html', {'budgetform': budgetform})


def update_expense(request, pk):
    expense_info = Expense.objects.get(id=pk)
    expenseform = ExpenseForm(instance=expense_info)

    if request.user.username:
        if request.method == "POST":
            expenseform = ExpenseForm(request.POST, instance=expense_info)
            if expenseform.is_valid():
                expenseform.save()
                return redirect("/profile/")

        else:
            context = {
                "expenseform": expenseform,
                "current_date": datetime.now().date(),
                "expense_info": expense_info,
            }
            return render(request, "expenses/update_expense.html", context)


def delete_expense(request, pk):
    expense_info = Expense.objects.get(id=pk)
    print(expense_info)
    if request.method == "POST":
        expense_info.delete()
        return redirect("/profile/")
    context = {
        "current_date": datetime.now().date(),
        "expense_info": expense_info,
    }
    return render(request, "expenses/update_expense.html", context)
