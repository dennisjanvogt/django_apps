from decimal import Decimal
import random
import factory
from django.contrib.auth.models import User
from .models import Mitarbeiter, Kunde, Schadensfall, Versicherungsvertrag


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.LazyAttribute(lambda a: f"{a.username}@example.com")


class MitarbeiterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mitarbeiter

    user = factory.SubFactory(UserFactory)
    position = factory.Iterator(["agent", "manager", "support"])
    geburtsdatum = factory.Faker("past_date", start_date="-30y", tzinfo=None)
    einstellungsdatum = factory.Faker("past_date", start_date="-5y", tzinfo=None)
    telefonnummer = factory.Sequence(lambda n: "123456789%d" % n)


class KundeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Kunde

    vorname = factory.Faker("first_name")
    nachname = factory.Faker("last_name")
    email = factory.Sequence(lambda n: "kunde%d@example.com" % n)
    telefonnummer = factory.Sequence(lambda n: "+49 12345678%d" % n)


class VersicherungsvertragFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Versicherungsvertrag

    vertragsnummer = factory.Faker("bothify", text="????-####-????")
    kunde = factory.SubFactory(KundeFactory)
    mitarbeiter = factory.SubFactory(MitarbeiterFactory)
    startdatum = factory.Faker("past_date")
    enddatum = factory.Faker("future_date")
    monatlicher_beitrag = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )


class SchadensfallFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schadensfall

    beschreibung = factory.Faker("text")
    versicherungsvertrag = factory.SubFactory(VersicherungsvertragFactory)
    schadenshoehe = factory.LazyFunction(
        lambda: Decimal(random.uniform(0.01, 9999999.99)).quantize(Decimal(".01"))
    )
    status = factory.Iterator(["offen", "bearbeitet", "abgeschlossen"])
