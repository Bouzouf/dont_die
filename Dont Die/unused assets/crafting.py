
choice = ""
to_append = []
while choice.lower() != 'q':
    item1 = input("Item 1: ")
    amount1 = int(input("Amount 1: "))
    item2 = input("Item 2: ")
    amount2 = int(input("Amount 2: "))
    output = input("Output Item: ")
    amount_output = int(input("Amount of recipe: "))
    recipe_type = input("Type: ")
    choice = input("Confirm Your Choice. ")
    if choice.lower() == 'y':
        to_append.append([[item1,amount1],[item2,amount2],output,amount_output,recipe_type])
print(to_append)