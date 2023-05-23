# myapp/management/commands/generate_data.py
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from versicherung.models import Mitarbeiter, Kunde, Versicherungsvertrag, Schadensfall
from faker import Faker
import random


class Command(BaseCommand):
    help = "Create random users"

    def add_arguments(self, parser):
        parser.add_argument(
            "total", type=int, help="Indicates the number of users to be created"
        )

    def handle(self, *args, **kwargs):
        total = kwargs["total"]
        fake = Faker()
        for i in range(total):
            user = User.objects.create(username=fake.first_name(), email=fake.email())
            Mitarbeiter.objects.create(
                user=user,
                position=random.choice(Mitarbeiter.POSITION_CHOICES)[0],
                geburtsdatum=fake.date_of_birth(minimum_age=22, maximum_age=55),
                einstellungsdatum=fake.date_this_century(),
                telefonnummer=fake.phone_number(),
            )
            Kunde.objects.create(
                vorname=fake.first_name(),
                nachname=fake.last_name(),
                email=fake.email(),
                telefonnummer=fake.phone_number(),
            )
            Versicherungsvertrag.objects.create(
                vertragsnummer=get_random_string(length=20),
                kunde=Kunde.objects.order_by("?").first(),
                mitarbeiter=Mitarbeiter.objects.order_by("?").first(),
                startdatum=fake.date_this_century(),
                enddatum=fake.date_this_century(),
                monatlicher_beitrag=random.uniform(0, 10000),
            )
            Schadensfall.objects.create(
                beschreibung=fake.text(),
                versicherungsvertrag=Versicherungsvertrag.objects.order_by("?").first(),
                schadenshoehe=random.uniform(0, 10000),
                status=random.choice(Schadensfall.STATUS_CHOICES)[0],
            )
