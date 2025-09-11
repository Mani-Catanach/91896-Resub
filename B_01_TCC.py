import pandas
from tabulate import tabulate
from datetime import date
import math


# Functions go here
def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}\n"


def yes_no(question):
    """Checks that users enter yes / no / y / n"""

    while True:

        response = input(question).lower()

        if response == "y" or response == "yes":
            return "yes"
        elif response == "n" or response == "no":
            return "no"

        print(f"Please answer yes / no (y / n)")


def instructions():
    """Displays instructions"""
    print(make_statement("Instructions", "{}"))

    print('''This program will ask you for... 
    - The name of the tech shop you have 
    - The title of your employees
    - The amount of each employee type (must be greater than 0)
    - The amount of hours each employee type works (must be greater than 0) 
    - The wages of that employee type (must be greater than $23.50)
    - Whether or not you have weekly expenses (if you have 
      weekly expenses, it will ask you what they are).
    - The name of your technology product
    - How much you sell each piece technology for
    - How much it costs to make each technology item (must be less than the sell price)
    - Type 'xxx' into the name input when you're done with a section to move on to the next section.
    - You must have at least one entry for each section before moving on to the next 


The program outputs an itemised list of the employee and weekly 
expenses (which includes the subtotals for these expenses). It also
outputs the profit you make per piece of technology sold and how many 
pieces of technology you need to sell on average, minimum, and 
maximum, to break even (rounded up).

The data will then be written to a text file which has the 
same name as your shop name and today's date. (Provided that
the shop name is less than 19 characters long)

    ''')


def not_blank(question):
    """Checks user response is not blank"""
    while True:
        response = input(question)

        if response != "":
            return response
        else:
            print("Sorry, this can't be blank.")


def num_check(question, num_type="float", exit_code=None):
    """Checks that response is a float / integer more than zero"""

    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:

        response = input(question)

        # check for exit code and return it if entered
        if response == exit_code:
            return response

        # check datatype is correct and that number
        # is more than zero
        try:

            if num_type == "float":
                response = float(response)
            else:
                response = int(response)

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)


def get_expenses(exp_type, how_many=10):
    """Gets employee / weekly expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    # Lists for panda
    all_emp = []
    all_hours = []
    all_amount = []
    all_employee_cost = []
    all_weekly_cost = []
    all_weekly = []

    # Expenses dictionary
    wages_dict = {
        "Employee": all_emp,
        "Hours": all_hours,
        "$ / Employee": all_employee_cost,
        "Amount": all_amount
    }

    weekly_dict = {
        "Weekly": all_weekly,
        "Weekly Cost": all_weekly_cost
    }

    if exp_type == "weekly":
        # loop to get weekly expenses
        while True:

            # get weekly name and check it's not blank
            util_name = not_blank("Weekly Expense Name: ")

            # check users enter at least one weekly expense
            if util_name == "xxx" and len(all_weekly) == 0:
                print("Oops - you have not entered any weekly expenses.  "
                      "You need at least one item.")
                continue

            # end loop when users enter exit code
            elif util_name == "xxx":
                break

            util_cost = num_check("Weekly Expense Cost: ", "float")

            all_weekly.append(util_name)
            all_weekly_cost.append(util_cost)

    elif exp_type == "wages":
        # loop to get wages
        while True:

            # Get item name and check it's not blank
            employee_title = not_blank("Employee Title: ")

            # check users enter at least one employee
            if employee_title == "xxx" and len(all_emp) == 0:
                print("Oops - you have not entered any employee types.  "
                      "You need at least one employee type.")
                continue

            # end loop when users enter exit code
            elif employee_title == "xxx":
                break

            quantity_employee = num_check("Employees of this type: ", "integer")

            hours = num_check(f"Hours per week? <enter for {how_many}>: ",
                              "integer", "")

            # Allow users to push <enter> to default to number of items being made
            if hours == "":
                hours = how_many

            how_much_question = "Wages of title? $"

            # Get price for item (question customised depending on expense type).
            employee_wage = num_check(how_much_question, "float")
            print()

            # loop restarts for illegal/unethical inputs
            if employee_wage < 23.50 or employee_wage > 100000:
                print("You cannot pay employees less than minimum wage ($23.50) or more than a completely "
                      "ludicrous amount ($10000). Make a new employee type")
                print()
                continue

            elif quantity_employee > 10000:
                print("You should not be employing more than 10000 employees of a certain type."
                      "Make a new employee type")

            elif hours > 70:
                print("You cannot have an employee work over 70 hours a week. Make a new employee type")
                print()
                continue

            all_emp.append(employee_title)
            all_amount.append(quantity_employee)
            all_hours.append(hours)
            all_employee_cost.append(employee_wage)

    # make util panda
    util_frame = pandas.DataFrame(weekly_dict)
    util_subtotal = util_frame['Weekly Cost'].sum()
    util_frame['Weekly Cost'] = util_frame['Weekly Cost'].apply(currency)
    weekly_string = tabulate(util_frame[['Weekly', 'Weekly Cost']], headers='keys',
                              tablefmt='psql', showindex=False)

    # make panda
    wage_frame = pandas.DataFrame(wages_dict)

    # Calculate wage Column
    wage_frame['Cost'] = wage_frame['Hours'] * wage_frame['$ / Employee'] * wage_frame['Amount']

    # calculate subtotal
    subtotal = wage_frame['Cost'].sum()

    # Apply currency formatting to currency columns.
    add_dollars = ['$ / Employee', 'Cost']
    for var_item in add_dollars:
        wage_frame[var_item] = wage_frame[var_item].apply(currency)

    # make expense frame into a string with the desired columns

    expense_string = tabulate(wage_frame, headers='keys',
                              tablefmt='psql', showindex=False)

    # return the expenses panda and subtotal
    return expense_string, subtotal, weekly_string, util_subtotal


def technology_prof_calc():
    # technology list for panda
    all_technology = []
    all_technology_cost = []
    all_technology_sell = []
    all_profit_per_tech = []

    profit_dict = {
        "Name": all_technology,
        "Material cost": all_technology_cost,
        "Sell price": all_technology_sell,
        "Profit / Tech": all_profit_per_tech
    }

    # loop to get expenses
    while True:
        tech_name = not_blank("Technology Name: ")

        if tech_name.lower() == "xxx":
            if len(all_technology) == 0:
                print("Oops - you have not entered anything.  "
                      "You need at least one item.")
                continue
            else:
                break

        cost_tech = num_check("$ / Piece of Technology? ", "float")
        mat_cost = num_check("Material Cost?", "float")
        tech_prof = cost_tech - mat_cost
        if tech_prof <= 0:
            print("You cannot have a profit of <=$0 per piece of technology. Make a new technology product")
            print()
            continue

        all_technology.append(tech_name)
        all_technology_cost.append(mat_cost)
        all_technology_sell.append(cost_tech)
        all_profit_per_tech.append(tech_prof)

    # make panda
    tech_frame = pandas.DataFrame(profit_dict)

    # Calculate Cost Column
    tech_frame['Profit / Tech'] = tech_frame['Sell price'] - tech_frame['Material cost']

    # calculate subtotal
    tech_sub = tech_frame['Profit / Tech'].sum()
    max_prof = tech_frame['Profit / Tech'].max()
    min_prof = tech_frame['Profit / Tech'].min()
    avg_prof = tech_frame['Profit / Tech'].mean()

    # Apply currency formatting to currency columns.
    add_tech = ['Sell price', 'Material cost', 'Profit / Tech']
    for var_item in add_tech:
        tech_frame[var_item] = tech_frame[var_item].apply(currency)

    # make expense frame into a string with the desired columns
    tech_string = tabulate(tech_frame[['Name', 'Profit / Tech']], headers='keys',
                            tablefmt='psql', showindex=False)

    # return the expenses panda and subtotal
    return tech_string, tech_sub, avg_prof, max_prof, min_prof


def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)


def round_up(amount, round_val):
    """Rounds amount to desired hole number"""
    return int(math.ceil(amount / round_val)) * round_val


def clean_filename(raw_filename):
    """Check filename has not illegal characters and is not too long"""

    # assume filename is OK
    valid_filename = True
    error = ""

    while True:

        # replace spaces with underscores
        raw_filename = raw_filename.replace(" ", "_")

        # check for valid length
        if len(raw_filename) >= 20:
            valid_filename = False
            error = ("Oops - your product name / filename is too long.  \n"
                     "Please provide an alternate filename (<= 19 characters) \n"
                     "or press <enter> to default to PCC_yyyy_mm_ddd")

        # iterate through filename and check for invalid characters
        for letter in raw_filename:
            if letter.isalnum() is False and letter != "_":
                valid_filename = False
                error = ("I can't use the product name / proposed filename \n"
                         "as it has illegal characters.  Please \n"
                         "enter an alternate name for the first part \n"
                         "of the file or press <enter> to default to PCC_yyyy_mm_dd")
                break

        if valid_filename is False:
            print(error)
            raw_filename = input("\nPlease enter an alternate name for the start of the file: ")

            # reset valid_filename so that it's new name can be checked.
            valid_filename = True

            # put in default filename if users press <enter>
            if raw_filename == "":
                raw_filename = "BCC"

        else:
            return raw_filename


# Main routine goes here

# initialise variables...

# assume we have no weekly expenses for now
weekly_subtotal = 0
weekly_panda_string = ""

print(make_statement("Technology Cost Calculator", "[]"))

print()
want_instructions = yes_no("Do you want to see the instructions? ")
print()

if want_instructions == "yes":
    instructions()

print()

# Get product details...
shop_name = not_blank("Shop Name: ")

# Get variable expenses...
print("Let's get the employee wages....")
employee_wages = get_expenses("wages")
print()

employee_panda_string = employee_wages[0]
employee_subtotal = employee_wages[1]

# ask user if they have weekly expenses and retrieve them
print()
has_weekly = yes_no("Do you have weekly expenses? ")

if has_weekly == "yes":
    weekly_expenses = get_expenses("weekly")

    weekly_panda_string = weekly_expenses[2]
    weekly_subtotal = weekly_expenses[3]

    # If the user has not entered any weekly expenses,
    # # Set empty panda to "" so that it does not display!
    if weekly_subtotal == 0:
        has_weekly = "no"
        weekly_panda_string = ""

total_expenses = employee_subtotal + weekly_subtotal
total_expenses_string = f"Total Expenses: ${total_expenses:.2f}"

print()
print("Let's get your profit per piece of technology...")
tech_profit_string, technology_subtotal, prof_avg, prof_max, prof_min = technology_prof_calc()
tech_panda_string = tech_profit_string

# calc amounts to sell
avg_amount = total_expenses / prof_avg
min_amount = total_expenses / prof_max
max_amount = total_expenses / prof_min
avg_num = math.ceil(avg_amount)
min_num = math.ceil(min_amount)
max_num = math.ceil(max_amount)

min_amount = []
max_amount = []
ave_amount = []

# Final dictionary
final_dict = {
    "Minimum Amount": min_amount,
    "Maximum Amount": max_amount,
    "Average Amount": ave_amount
}


min_amount.append(min_num)
max_amount.append(max_num)
ave_amount.append(avg_num)

# make panda
final_frame = pandas.DataFrame(final_dict)
final_panda_string = tabulate(final_frame, headers='keys',
                            tablefmt='psql', showindex=False)

# strings / output area

# **** Get current date for heading and filename ****
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

# Headings / Strings...
main_heading_string = make_statement(f"Technology Cost Calculator "
                                     f"({shop_name}, {day}/{month}/{year})", "=")

employee_heading_string = make_statement("Employee Wages", "-")
employee_subtotal_string = f"Wage Expense Subtotal: ${employee_subtotal:.2f}"

# set up strings if we have weekly costs
if has_weekly == "yes":
    weekly_heading_string = make_statement("Weekly Expenses", "-")
    weekly_subtotal_string = f"Weekly Expenses Subtotal: {weekly_subtotal:.2f}"

# set weekly cost strings to blank if we don't have weekly costs
else:
    weekly_heading_string = make_statement("You have no Weekly Expenses", "-")
    weekly_subtotal_string = "Weekly Expenses Subtotal: $0.00"

tech_profit_heading = make_statement("Profit Per Piece of Tech", "-")
avg_amount_heading = make_statement("Selling Amount Calculations", "-")

print(final_frame)
suggest_amount_string = make_statement(f"We suggest you should sell {avg_num} pieces of technology per week to break even.", "*")

# List of strings to be outputted / written to file
to_write = [
            main_heading_string,
            "\n", employee_heading_string, employee_panda_string,
            employee_subtotal_string,
            "\n", weekly_heading_string, weekly_panda_string,
            weekly_subtotal_string, "\n",
            tech_panda_string, "\n",
            total_expenses_string,
            avg_amount_heading, final_panda_string,
            "\n", suggest_amount_string]

# Print area
print()
for item in to_write:
    print(item)

# create file to hold data (add .txt extension)

# check product name is suitable for a filename
# and ask for an alternate file name if necessary
clean_shop_name = clean_filename(shop_name)

file_name = f"{clean_shop_name}_{year}_{month}_{day}"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w+")

# write item to file
for item in to_write:
    text_file.write(item)
    text_file.write("\n")