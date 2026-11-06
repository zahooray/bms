import csv
import random

from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from django.db import transaction as db_transaction

from bms.accounts.constants import AccountType, TransactionType
from bms.accounts.models import Account, Transaction
from bms.banks.models import Bank, Branch
from bms.users.models import User


DATA_DIR = Path(__file__).resolve().parent / "data"

SEED = 42
PASSWORD = "test1234"

START_DATE = date(2024, 1, 1)
END_DATE = date(2025, 12, 31)

MIN_TRANSACTIONS = 30
MAX_TRANSACTIONS = 50
WITHDRAWAL_CHANCE = 0.4
MAX_WITHDRAWAL = 100_000
MIN_DEPOSIT = 500
MAX_DEPOSIT = 200_000


def read_csv(name):
    with open(DATA_DIR / name, encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def parse_bool(value, source):
    if value in ("true", "false"):
        return value == "true"

    raise ValueError(f"{source}: expected true or false, got {value!r}")


def lookup(items, key, source):
    if key in items:
        return items[key]

    raise ValueError(f"{source}: unknown reference {key!r}")


def random_date():
    days = (END_DATE - START_DATE).days

    return START_DATE + timedelta(days=random.randint(0, days))


def random_amount(low, high):
    cents = random.randint(low * 100, high * 100)

    return Decimal(cents) / 100


def seed_banks():
    banks = {}
    for row in read_csv("banks.csv"):
        banks[row["swift_code"]], _ = Bank.objects.update_or_create(
            swift_code=row["swift_code"],
            defaults={
                "name": row["name"],
                "is_islamic": parse_bool(row["is_islamic"], f"banks.csv {row['swift_code']}"),
                "established_date": date.fromisoformat(row["established_date"]),
            },
        )

    return banks


def seed_branches(banks):
    branches = {}
    for line, row in enumerate(read_csv("branches.csv"), start=2):
        bank = lookup(banks, row["bank_swift_code"], f"branches.csv line {line}")
        key = (row["bank_swift_code"], row["branch_code"])
        branches[key], _ = Branch.objects.update_or_create(
            bank=bank,
            branch_code=row["branch_code"],
            defaults={"name": row["name"], "address": row["address"]},
        )

    return branches


def seed_users():
    users = {}
    for row in read_csv("users.csv"):
        user, created = User.objects.update_or_create(
            username=row["username"],
            defaults={
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
            },
        )
        if created:
            user.set_password(PASSWORD)
            user.save(update_fields=["password"])
        users[row["username"]] = user

    return users


def seed_accounts(users, branches):
    rows = read_csv("accounts.csv")
    account_numbers = [row["account_number"] for row in rows]

    Account.objects.filter(user__in=users.values()).exclude(
        account_number__in=account_numbers
    ).delete()

    for line, row in enumerate(rows, start=2):
        source = f"accounts.csv line {line}"
        if row["account_type"] not in AccountType.values:
            raise ValueError(f"{source}: unknown account type {row['account_type']!r}")

        Account.objects.update_or_create(
            account_number=row["account_number"],
            defaults={
                "user": lookup(users, row["username"], source),
                "bank_branch": lookup(
                    branches, (row["bank_swift_code"], row["branch_code"]), source
                ),
                "account_type": row["account_type"],
            },
        )


def check_accounts(users):
    for user in users.values():
        bank_count = (
            Account.objects.filter(user=user).values("bank_branch__bank").distinct().count()
        )
        if bank_count != 2:
            raise ValueError(f"{user.username} must have accounts in 2 different banks")


def build_transactions(account):
    count = random.randint(MIN_TRANSACTIONS, MAX_TRANSACTIONS)
    dates = sorted(random_date() for _ in range(count))

    running_total = Decimal("0")
    rows = []
    for day in dates:
        if running_total >= 1 and random.random() < WITHDRAWAL_CHANCE:
            amount = random_amount(1, min(int(running_total), MAX_WITHDRAWAL))
            running_total -= amount
            transaction_type = TransactionType.WITHDRAWAL
        else:
            amount = random_amount(MIN_DEPOSIT, MAX_DEPOSIT)
            running_total += amount
            transaction_type = TransactionType.DEPOSIT

        rows.append(Transaction(account=account, date=day, amount=amount, type=transaction_type))

    return rows


def seed_transactions():
    random.seed(SEED)
    Transaction.objects.all().delete()
    rows = []
    for account in Account.objects.order_by("id"):
        rows.extend(build_transactions(account))

    return Transaction.objects.bulk_create(rows)


def run():
    with db_transaction.atomic():
        banks = seed_banks()
        branches = seed_branches(banks)
        users = seed_users()
        seed_accounts(users, branches)
        check_accounts(users)
        transactions = seed_transactions()

    print(
        f"Seeded {len(banks)} banks, {len(branches)} branches, {len(users)} users, "
        f"{Account.objects.count()} accounts and {len(transactions)} transactions.\n"
        f"User password: {PASSWORD}"
    )
