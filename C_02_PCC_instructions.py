# Functions go here...
def yes_no(question):
    """Checks that users enter yes / y or no / n to a question"""

    while True:
        response = input(question).lower()

        if response == "yes" or response == "y":
            return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("Please enter yes (y) or no (n).\n")

def make_statement(statement, decoration):
    """Emphasises headings by adding decoration at the start and end"""

    print(f"{decoration * 3} {statement} {decoration * 3}")

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

# Main Routine goes here
print(make_statement("Pizza Cost Calculator", "[]"))

print()
want_instructions =yes_no("Do you want to see the instructions?")
print()

if want_instructions == "yes":
    instructions()

print()
print(" program continues")

