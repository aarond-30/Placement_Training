
from expense_manager import (
    create_group,
    add_member,
    add_expense,
    show_expense_history
)

from balance_settlement import (
    calculate_balances,
    show_balances,
    generate_settlement,
    check_consistency
)


def main():

    group = None

    while True:

        print("\n========== EVENSPLIT ==========")
        print("1. Create Group")
        print("2. Add Member")
        print("3. Add Expense")
        print("4. View Expense History")
        print("5. View Member Balances")
        print("6. Generate Settlement Plan")
        print("7. Check Total Consistency")
        print("8. Exit")
        print("================================")

        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:

            if group is not None:

                confirm = input(
                    "A group already exists. Replace it? (yes/no): "
                ).strip().lower()

                if confirm not in ["yes", "y"]:
                    continue

            group = create_group()

        elif choice == 8:

            print("\nThank you for using EvenSplit!")
            break

        elif choice in [2, 3, 4, 5, 6, 7]:

            if group is None:
                print("\nPlease create a group first.")
                continue

            if choice == 2:
                add_member(group)

            elif choice == 3:
                add_expense(group)

            elif choice == 4:
                show_expense_history(group)

            elif choice == 5:
                show_balances(group)

            elif choice == 6:
                generate_settlement(group)

            elif choice == 7:
                check_consistency(group)

        else:
            print("Invalid choice. Select between 1 and 8.")


if __name__ == "__main__":
    main()
