from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import Sum
from datetime import datetime
from plotly.graph_objs import Pie, Scatter, Figure
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
        # colors = ["#C0ECCC", "#F6A8A6", "#F9F0C1", "#A5C8E4", "#F4CDA6"]
        colors = ["#5cb85c", "#d9534f", "#f5e83b", "#0275d8", "#f0ad4e"]

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

    # Expense / Budget Line Plot
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


        # # Query the date & weeks in the model
        # date_set = Expense.objects.filter(author=author_id).order_by("expense_date")
        # yr_wks = []
        # date_lst = []  # Scatter plot x-axis
        # for date in date_set:
        #     yr_wks.append(date.expense_date.isocalendar()[:2])
        #     date_lst.append(date.expense_date.strftime("(%Y, 'Week: %W')"))
        #
        # # KNOWN ISSUE: The begging and end of year weeks for isocalendar causes issues when extracting data from the
        # # model, so a workaround could be to have a conditional statement to test the week and then use strftime
        # # to format the weeks that need it in order to directly extract the dates needed. strftime is -1 for isoweek.
        #
        # yr_wks = list(set(yr_wks))  # Removes the duplicates
        # yr_wks = sorted(yr_wks, key=lambda x: x[0])  # Sorts the years from lesser to greater iso value
        # date_lst = list(set(date_lst))
        # date_lst = map(literal_eval, date_lst)
        # date_lst = sorted(date_lst, key=lambda x: x[0])
        # print(date_lst)
        #
        # # Must use for loops to iterate over the years/weeks from the DB in order to accurately show all data per week
        # # Then append those values to corresponding list
        # wk_total = []
        # wk_food = []
        # wk_personal = []
        # wk_transpo = []
        # wk_housing = []
        # wk_other = []
        #
        # for yr_wk in yr_wks:
        #     wk_expenses = Expense.objects.filter(
        #         author=author_id).filter(expense_date__year=yr_wk[0]).filter(expense_date__week=yr_wk[1]). \
        #         aggregate(Sum("amount"))
        #     wk_expenses = wk_expenses["amount__sum"]
        #     wk_total.append(wk_expenses)
        #
        #     food_amount_wk = Expense.objects.filter(expense_type="food"). \
        #         filter(author=author_id).filter(expense_date__year=yr_wk[0]).filter(expense_date__week=yr_wk[1]). \
        #         aggregate(Sum("amount"))
        #     food_amount_wk = food_amount_wk["amount__sum"]
        #
        #     personal_amount_wk = Expense.objects.filter(expense_type="personal"). \
        #         filter(author=author_id).filter(expense_date__year=yr_wk[0]).filter(expense_date__week=yr_wk[1]). \
        #         aggregate(Sum("amount"))
        #     personal_amount_wk = personal_amount_wk["amount__sum"]
        #
        #     transportation_amount_wk = Expense.objects.filter(expense_type="transportation"). \
        #         filter(author=author_id).filter(expense_date__year=yr_wk[0]).filter(expense_date__week=yr_wk[1]). \
        #         aggregate(Sum("amount"))
        #     transportation_amount_wk = transportation_amount_wk["amount__sum"]
        #
        #     housing_amount_wk = Expense.objects.filter(expense_type="housing"). \
        #         filter(author=author_id).filter(expense_date__year=yr_wk[0]).filter(expense_date__week=yr_wk[1]). \
        #         aggregate(Sum("amount"))
        #     housing_amount_wk = housing_amount_wk["amount__sum"]
        #
        #     other_amount_wk = Expense.objects.filter(expense_type="other"). \
        #         filter(author=author_id).filter(expense_date__year=yr_wk[0]).filter(expense_date__week=yr_wk[1]). \
        #         aggregate(Sum("amount"))
        #     other_amount_wk = other_amount_wk["amount__sum"]
        # print(wk_total)


        budget_line = Budget.objects.filter(author=author_id).last()
        budget_line = float(budget_line.weekly_spending_total)

        print(budget_line)
        print(scatter_plot_data.index.max())

        trace_wk_tot = Scatter(
            x=scatter_plot_data.index,
            y=scatter_plot_data.amount,
            mode="lines+markers",
            name="lines+markers",
            line=dict(
                color="#5cb85c",
                width=4,
            ),
        )

        # For possible lines per expense type
        trace_wk_fd = None
        trace_wk_pr = None
        trace_wk_tp = None
        trace_wk_hs = None
        trace_wk_ot = None

        expense_weekly_data = [trace_wk_tot]

        line_plot = Figure(expense_weekly_data)

        # Total Budget per week line for comparison
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
            title_text="Total Expenses per Week"
        )
        plot_div_line = plot(line_plot, output_type="div")

    # ----------- BUDGET PAGE ------------

        context = {
            "user_expenses": user_expenses,
            "user_name": user_name,
            "plot_div": plot_div,
            "plot_div_line": plot_div_line,
            "BudgetForm": BudgetForm,
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
    if request.user.username:
        if request.method == "POST":
            form = BudgetForm(request.POST)
            if form.is_valid():

                weekly_spending_total = request.POST.get("weekly_spending_total")
                weekly_food = request.POST.get("weekly_food")
                weekly_personal = request.POST.get("weekly_personal")
                weekly_transportation = request.POST.get("weekly_transportation")
                weekly_housing = request.POST.get("weekly_housing")
                weekly_other = request.POST.get("weekly_other")
                budget_author = request.user.username

                print(weekly_spending_total)

                budget_instance = Budget()

                budget_instance.weekly_spending_total = weekly_spending_total
                budget_instance.weekly_food = weekly_food
                budget_instance.weekly_personal = weekly_personal
                budget_instance.weekly_transportation = weekly_transportation
                budget_instance.weekly_housing = weekly_housing
                budget_instance.weekly_other = weekly_other
                budget_instance.author = User.objects.get(username=budget_author)

                budget_instance.save()
                return redirect("/profile/")

            else:
                form = BudgetForm()

            return render(request, 'expenses.html', {'form': form})


def update_expense(request, pk):
    print(pk)

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
