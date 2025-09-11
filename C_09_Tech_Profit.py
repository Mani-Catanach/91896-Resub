import pandas
from tabulate import tabulate


#functions go here
def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)


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


def not_blank(question):
    """Checks user response is not blank"""
    while True:
        response = input(question)

        if response != "":
            return response
        else:
            print("Sorry, this can't be blank.")


def tech_prof_calc():
    # Tech list for panda
    all_tech = []
    all_tech_cost = []
    all_tech_sell = []
    all_profit_per_tech = []

    profit_dict = {
        "Name": all_tech,
        "Material cost": all_tech_cost,
        "Sell price": all_tech_sell,
        "Profit / Tech": all_profit_per_tech
    }

    # loop to get expenses
    while True:
        tech_name = not_blank("Technology Name: ")

        if tech_name.lower() == "xxx":
            if len(all_tech) == 0:
                print("Oops - you have not entered anything.  "
                      "You need at least one item.")
                continue
            else:
                break

        cost_tech = num_check("$ / Pizza? ", "float")
        mat_cost = num_check("Material Cost?", "float")
        tech_prof = cost_tech - mat_cost
        if tech_prof <= 0:
            print("You cannot have a profit of <=$0 per piece of technology. "
                  "Make a new technology product")
            print()
            continue

        all_tech.append(tech_name)
        all_tech_cost.append(mat_cost)
        all_tech_sell.append(cost_tech)
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


# main routine goes here
print("Getting Technology Profit")

# get tech numbers
tech_panda, tech_subtotal, average_prof, maximum_prof, minimum_prof = tech_prof_calc()

# print results
print(tech_panda)
print(tech_subtotal)
print(average_prof)
print(maximum_prof)
print(minimum_prof)