import random

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker

from ...models import Category, Transaction

User = get_user_model()


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        fake = Faker()

        # create categories
        category_list = [
            "Bills",
            "Food",
            "Clothes",
            "Medical",
            "Housing",
            "Salary",
            "Social",
            "Transport",
            "Vacation",
        ]

        if Category.objects.exists() or Transaction.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    '1 or more record(s) found - clear existing db records from "categories" & "transactions" tables and re-run this command\n'
                )
            )
            return

        raw_users = [
            {"username": "a", "email": "a@a.com", "password": "1234"},
            {"username": "b", "email": "b@b.com", "password": "1234"},
            {"username": "c", "email": "c@c.com", "password": "1234"},
            {"username": "d", "email": "d@d.com", "password": "1234"},
        ]

        user_list = [
            User(
                username=data["username"],
                email=data["email"],
                password=make_password(data["password"]),
            )
            for data in raw_users
        ]

        User.objects.bulk_create(user_list, ignore_conflicts=True)
        users = list(
            User.objects.filter(username__in=[user["username"] for user in raw_users])
        )

        saved_users = User.objects.filter(
            username__in=[user["username"] for user in raw_users]
        )

        email_list = [
            EmailAddress(
                user=user,
                email=user.email,
                primary=True,
                verified=True,
            )
            for user in saved_users
        ]
        EmailAddress.objects.bulk_create(email_list, ignore_conflicts=True)

        # allauth_users = list(
        #     EmailAddress.objects.filter(
        #         user__username__in=[user["username"] for user in raw_users]
        #     )
        # )

        Category.objects.bulk_create(
            [Category(name=category) for category in category_list],
            ignore_conflicts=True,
        )

        categories = list(Category.objects.filter(name__in=category_list))

        types = [x for x in Transaction.TransactionType]

        for i in range(20):
            Transaction.objects.create(
                category=random.choice(categories),
                # user=random.choice(allauth_users),
                user=random.choice(users),
                amount=random.uniform(1, 2500),
                date=fake.date_between(start_date="-1y", end_date="today"),
                type=random.choice(types),
            )

        self.stdout.write(self.style.SUCCESS("Transactions created...\n"))
