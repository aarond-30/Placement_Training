
from decimal import Decimal


def to_paise(amount):
    return int(Decimal(str(amount)) * 100)


def calculate_balances(group):

    balances = {}

    for member in group["members"]:
        balances[member] = {
            "total_paid": 0,
            "total_share": 0,
            "net_balance": 0
        }

    for expense in group["expenses"]:

        payer = expense["paid_by"]

        balances[payer]["total_paid"] += to_paise(
            expense["amount"]
        )

        for member, share in expense["shares"].items():
            balances[member]["total_share"] += to_paise(share)

    for member in balances:

        paid = balances[member]["total_paid"]
        share = balances[member]["total_share"]

        balances[member]["net_balance"] = paid - share

    return balances


def show_balances(group):

    print("\n========== MEMBER BALANCES ==========")

    if not group["expenses"]:
        print("No expenses recorded yet.")
        return

    balances = calculate_balances(group)

    print("\nGroup:", group["group_name"])
    print("-" * 75)

    print(f"{'Member':<15}{'Paid':>15}{'Share':>15}{'Balance':>15}  Status")

    print("-" * 75)

    for member, details in balances.items():

        paid = details["total_paid"] / 100
        share = details["total_share"] / 100
        balance = details["net_balance"] / 100

        if balance > 0:
            status = "Gets Back"
        elif balance < 0:
            status = "Owes"
        else:
            status = "Settled"

        print(
            f"{member:<15}"
            f"{paid:>15.2f}"
            f"{share:>15.2f}"
            f"{balance:>15.2f}  "
            f"{status}"
        )

    print("-" * 75)


def generate_settlement(group):

    print("\n========== SETTLEMENT PLAN ==========")

    if not group["expenses"]:
        print("No expenses available.")
        return

    balances = calculate_balances(group)

    creditors = []
    debtors = []

    for member, details in balances.items():

        balance = details["net_balance"]

        if balance > 0:
            creditors.append([member, balance])

        elif balance < 0:
            debtors.append([member, abs(balance)])

    if not creditors and not debtors:
        print("All members are already settled.")
        return

    print("\nCreditors:")

    for member, amount in creditors:
        print(f"{member} should receive Rs. {amount / 100:.2f}")

    print("\nDebtors:")

    for member, amount in debtors:
        print(f"{member} owes Rs. {amount / 100:.2f}")

    print("\nPayment Transactions:")

    i = 0
    j = 0
    count = 1

    while i < len(debtors) and j < len(creditors):

        debtor = debtors[i][0]
        creditor = creditors[j][0]

        payment = min(debtors[i][1], creditors[j][1])

        print(
            f"{count}. {debtor} pays {creditor} "
            f"Rs. {payment / 100:.2f}"
        )

        debtors[i][1] -= payment
        creditors[j][1] -= payment

        if debtors[i][1] == 0:
            i += 1

        if creditors[j][1] == 0:
            j += 1

        count += 1

    print("\nSettlement completed.")
    print("Total transactions:", count - 1)


def check_consistency(group):

    print("\n========== CONSISTENCY CHECK ==========")

    total_paid = 0
    total_shares = 0

    for expense in group["expenses"]:

        total_paid += to_paise(expense["amount"])

        for share in expense["shares"].values():
            total_shares += to_paise(share)

    balances = calculate_balances(group)

    balance_sum = 0

    for details in balances.values():
        balance_sum += details["net_balance"]

    print(f"Total paid: Rs. {total_paid / 100:.2f}")
    print(f"Total shares: Rs. {total_shares / 100:.2f}")
    print(f"Sum of balances: Rs. {balance_sum / 100:.2f}")

    if total_paid == total_shares and balance_sum == 0:
        print("\nRecords are consistent.")
        return True

    else:
        print("\nRecords are not consistent.")
        return False
