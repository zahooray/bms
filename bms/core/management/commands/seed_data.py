from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from bms.accounts.constants import AccountType
from bms.accounts.models import Account
from bms.banks.models import Bank, Branch
from bms.users.models import User


PASSWORD = "test1234"

USERS = [
    # username, first name, last name, phone, date of birth
    ("ali", "Ali", "Khan", "03001234567", date(1995, 4, 12)),
    ("sara", "Sara", "Ahmed", "03011234567", date(1998, 9, 3)),
    ("usman", "Usman", "Raza", "03021234567", date(1990, 1, 27)),
    ("ayesha", "Ayesha", "Malik", "03031234567", date(2000, 6, 18)),
    ("bilal", "Bilal", "Hussain", "03041234567", date(1988, 11, 5)),
]

BANKS = [
    # swift code, name, is islamic, established date
    ("HABBPKKA", "Habib Bank Limited", False, date(1941, 8, 25)),
    ("MUCBPKKA", "MCB Bank Limited", False, date(1947, 7, 9)),
    ("UNILPKKA", "United Bank Limited", False, date(1959, 11, 7)),
    ("MEZNPKKA", "Meezan Bank Limited", True, date(1997, 1, 27)),
    ("BKIPPKKA", "BankIslami Pakistan Limited", True, date(2004, 10, 18)),
]

BRANCHES = [
    # bank swift code, branch code, name, address, is active
    ("HABBPKKA", "0001", "Main Branch", "Habib Bank Plaza, I.I. Chundrigar Road, Karachi", True),
    ("HABBPKKA", "0042", "Gulberg Branch", "Main Boulevard, Gulberg III, Lahore", True),
    ("HABBPKKA", "0108", "Blue Area Branch", "Jinnah Avenue, Blue Area, Islamabad", False),
    ("MUCBPKKA", "0010", "Mall Road Branch", "The Mall, Lahore", True),
    ("MUCBPKKA", "0215", "Saddar Branch", "Bank Road, Saddar, Rawalpindi", True),
    ("UNILPKKA", "0003", "Clifton Branch", "Block 5, Clifton, Karachi", True),
    ("UNILPKKA", "0077", "University Road Branch", "University Road, Peshawar", True),
    ("MEZNPKKA", "0101", "Shahrah-e-Faisal Branch", "Shahrah-e-Faisal, Karachi", True),
    ("MEZNPKKA", "0233", "F-7 Markaz Branch", "Jinnah Super Market, F-7, Islamabad", True),
    ("BKIPPKKA", "0005", "DHA Branch", "Phase 6, DHA, Lahore", True),
]

ACCOUNTS = [
    # account number, username, bank swift code, branch code, account type, balance
    ("PK36HABB0000001123456702", "ali", "HABBPKKA", "0001", AccountType.SAVINGS, "25000.00"),
    ("PK36HABB0000042123456703", "ali", "HABBPKKA", "0042", AccountType.CURRENT, "1200.50"),
    ("PK24MUCB0000010987654301", "sara", "MUCBPKKA", "0010", AccountType.SAVINGS, "78000.00"),
    ("PK11MEZN0000101555666701", "sara", "MEZNPKKA", "0101", AccountType.CURRENT, "0.00"),
    ("PK54UNIL0000003111222301", "usman", "UNILPKKA", "0003", AccountType.SAVINGS, "5400.75"),
    ("PK54UNIL0000077111222302", "usman", "UNILPKKA", "0077", AccountType.CURRENT, "150000.00"),
    ("PK11MEZN0000233777888901", "ayesha", "MEZNPKKA", "0233", AccountType.SAVINGS, "500.00"),
    ("PK79BKIP0000005444333201", "bilal", "BKIPPKKA", "0005", AccountType.SAVINGS, "92000.00"),
    ("PK24MUCB0000215987654302", "bilal", "MUCBPKKA", "0215", AccountType.CURRENT, "3300.00"),
]


class Command(BaseCommand):
    help = "Seed dummy users, banks, branches and accounts for testing"

    @transaction.atomic
    def handle(self, *args, **options):
        users = {}
        for username, first_name, last_name, phone, date_of_birth in USERS:
            user, created = User.objects.update_or_create(
                username=username,
                defaults={
                    "email": f"{username}@test.com",
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                    "date_of_birth": date_of_birth,
                },
            )
            if created:
                user.set_password(PASSWORD)
                user.save(update_fields=["password"])
            users[username] = user

        banks = {}
        for swift_code, name, is_islamic, established_date in BANKS:
            banks[swift_code], _ = Bank.objects.update_or_create(
                swift_code=swift_code,
                defaults={
                    "name": name,
                    "is_islamic": is_islamic,
                    "established_date": established_date,
                },
            )

        branches = {}
        for swift_code, branch_code, name, address, is_active in BRANCHES:
            branches[(swift_code, branch_code)], _ = Branch.objects.update_or_create(
                bank=banks[swift_code],
                branch_code=branch_code,
                defaults={"name": name, "address": address, "is_active": is_active},
            )

        for account_number, username, swift_code, branch_code, account_type, balance in ACCOUNTS:
            Account.objects.update_or_create(
                account_number=account_number,
                defaults={
                    "user": users[username],
                    "bank_branch": branches[(swift_code, branch_code)],
                    "account_type": account_type,
                    "balance": Decimal(balance),
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Seeded {len(USERS)} users, {len(BANKS)} banks, "
                f"{len(BRANCHES)} branches and {len(ACCOUNTS)} accounts.\n"
                f"   User password: {PASSWORD}"
            )
        )
