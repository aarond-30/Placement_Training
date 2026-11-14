
# ============================================
# EvenSplit: Group Expense Settlement Optimiser
# Module: Expense Management
# File: expense_manager.py
# Developed by: Member 1
# ============================================


# Function 1: Create a new group
def create_group():

    print("\n========== CREATE GROUP ==========")

    group_name = input("Enter group name: ").strip()

    # Validate group name
    while group_name == "":
        print("Group name cannot be empty.")
        group_name = input("Enter group name: ").strip()

    # Create the common group dictionary
    group = {
        "group_name": group_name,
        "members": [],
        "expenses": []
    }

    # Get the number of initial members
    while True:
        try:
            count = int(input("Enter number of members: "))

            if count > 0:
                break
            else:
                print("Please enter at least one member.")

        except ValueError:
            print("Please enter a valid whole number.")

    # Add members to the group
    for i in range(count):
        print("\nEnter details of member", i + 1)
        add_member(group)

    print("\nGroup created successfully!")
    print("Group Name:", group["group_name"])
    print("Total Members:", len(group["members"]))

    return group


# Function 2: Add a member to an existing group
def add_member(group):

    while True:

        name = input("Enter member name: ").strip()

        if name == "":
            print("Member name cannot be empty.")
            continue

        # Check for duplicate names
        duplicate = False

        for member in group["members"]:
            if member.lower() == name.lower():
                duplicate = True
                break

        if duplicate:
            print("This member already exists. Enter another name.")

        else:
            group["members"].append(name)
            print(name, "added successfully!")
            return group


# Function 3: Add a shared expense
def add_expense(group):

    print("\n========== ADD SHARED EXPENSE ==========")

    # Check whether group members exist
    if len(group["members"]) == 0:
        print("No members available. Add members first.")
        return group

    # Display group members
    print("\nGroup Members:")

    for i in range(len(group["members"])):
        print(i + 1, ".", group["members"][i])

    # Select the person who paid
    while True:
        try:
            payer_choice = int(input("\nSelect payer (enter number): "))

            if 1 <= payer_choice <= len(group["members"]):
                paid_by = group["members"][payer_choice - 1]
                break
            else:
                print("Invalid member selection.")

        except ValueError:
            print("Please enter a valid number.")

    # Enter expense description
    description = input("Enter expense description: ").strip()

    while description == "":
        print("Description cannot be empty.")
        description = input("Enter expense description: ").strip()

    # Enter expense amount
    while True:
        try:
            amount = float(input("Enter total expense amount (Rs.): "))

            # Round to two decimal places
            amount = round(amount, 2)

            if amount > 0 and amount != float("inf"):
                break
            else:
                print("Amount must be greater than zero.")

        except ValueError:
            print("Please enter a valid amount.")

    # Display members for expense participation
    print("\nSelect members who participated:")

    for i in range(len(group["members"])):
        print(i + 1, ".", group["members"][i])

    # Select participants
    while True:

        try:
            choices = input(
                "Enter member numbers separated by commas: "
            )

            selected_numbers = choices.split(",")

            participants = []
            valid = True

            for number in selected_numbers:

                number = int(number.strip())

                if number < 1 or number > len(group["members"]):
                    valid = False
                    break

                member = group["members"][number - 1]

                if member in participants:
                    valid = False
                    break

                participants.append(member)

            if valid and len(participants) > 0:
                break
            else:
                print("Invalid selection. Please select valid members without duplicates.")

        except ValueError:
            print("Enter valid member numbers separated by commas.")

    # Calculate equal shares
    # Convert amount into paise to handle decimal rounding correctly
    total_paise = round(amount * 100)

    number_of_participants = len(participants)

    # Divide the total amount equally
    base_share = total_paise // number_of_participants
    remaining_paise = total_paise % number_of_participants

    shares = {}

    for i in range(number_of_participants):

        # Distribute any remaining paise one by one
        member_share = base_share

        if i < remaining_paise:
            member_share = member_share + 1

        shares[participants[i]] = member_share / 100

    # Create the expense dictionary
    expense = {
        "description": description,
        "paid_by": paid_by,
        "amount": amount,
        "participants": participants,
        "shares": shares
    }

    # Store expense in the group's expense list
    group["expenses"].append(expense)

    print("\nExpense added successfully!")
    print("Description:", description)
    print("Paid By:", paid_by)
    print("Total Amount: Rs.", format(amount, ".2f"))

    print("\nIndividual Shares:")

    for member in shares:
        print(member, ": Rs.", format(shares[member], ".2f"))

    return group


# Function 4: Display expense history
def show_expense_history(group):

    print("\n========== EXPENSE HISTORY ==========")

    # Check whether expenses exist
    if len(group["expenses"]) == 0:
        print("No expenses have been recorded yet.")
        return

    print("Group Name:", group["group_name"])

    # Display all expenses in insertion order
    for i in range(len(group["expenses"])):

        expense = group["expenses"][i]

        print("\n------------------------------------")
        print("Expense Number:", i + 1)
        print("Description:", expense["description"])
        print("Paid By:", expense["paid_by"])
        print("Total Amount: Rs.", format(expense["amount"], ".2f"))

        print("Participants:")

        for member in expense["participants"]:
            print("-", member)

        print("Individual Shares:")

        for member in expense["shares"]:
            print(
                member,
                ": Rs.",
                format(expense["shares"][member], ".2f")
            )

    print("\n------------------------------------")
    print("End of Expense History")
