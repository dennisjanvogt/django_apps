import os
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_apps.settings")
setup()


from django.test import TestCase
from versicherung.forms import (
    MitarbeiterForm,
    KundeForm,
    VersicherungsvertragForm,
    SchadensfallForm,
)
from versicherung.models import Kunde, Mitarbeiter, Versicherungsvertrag
from django.contrib.auth.models import User


class KundeFormTest(TestCase):
    def test_form_has_fields(self):
        form = KundeForm()
        expected = ["vorname", "nachname", "email", "telefonnummer"]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_valid_form(self):
        data = {
            "vorname": "John",
            "nachname": "Doe",
            "email": "john@example.com",
            "telefonnummer": "1234567890",
        }
        form = KundeForm(data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        data = {
            "vorname": "John",
            "nachname": "Doe",
            "email": "john@example.com",
            "telefonnummer": "1234567890",
        }
        form = KundeForm(data)
        kunde = form.save()
        self.assertEqual(kunde.vorname, "John")


class MitarbeiterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_superuser("myuser", "myemail@test.com", "mypassword")

    def test_mitarbeiter_content(self):
        Mitarbeiter.objects.create(
            user=User.objects.get(username="myuser"),
            position="agent",
            geburtsdatum="1990-01-01",
            einstellungsdatum="2020-01-01",
            telefonnummer="1234567890",
        )
        mitarbeiter = Mitarbeiter.objects.get(id=1)
        self.assertEqual(f"{mitarbeiter.user.username}", "myuser")

    def test_form_has_fields(self):
        form = MitarbeiterForm()
        expected = [
            "user",
            "position",
            "geburtsdatum",
            "einstellungsdatum",
            "telefonnummer",
        ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_valid_form(self):
        # Sie müssen einen gültigen Benutzer erstellen und dessen ID hier verwenden
        data = {
            "user": 1,
            "position": "agent",
            "geburtsdatum": "2000-01-01",
            "einstellungsdatum": "2022-01-01",
            "telefonnummer": "1234567890",
        }
        form = MitarbeiterForm(data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        data = {
            "user": 1,
            "position": "agent",
            "geburtsdatum": "2000-01-01",
            "einstellungsdatum": "2022-01-01",
            "telefonnummer": "1234567890",
        }
        form = MitarbeiterForm(data)
        mitarbeiter = form.save()
        self.assertEqual(mitarbeiter.position, "agent")


class VersicherungsvertragFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser("myuser", "myemail@test.com", "mypassword")
        Mitarbeiter.objects.create(
            user=User.objects.first(),
            position="agent",
            geburtsdatum="1990-01-01",
            einstellungsdatum="2020-01-01",
            telefonnummer="1234567890",
        )
        Kunde.objects.create(
            vorname="Max",
            nachname="Muster",
            email="max@muster.com",
            telefonnummer="0987654321",
        )
        Versicherungsvertrag.objects.create(
            vertragsnummer="12345",
            kunde=Kunde.objects.first(),
            mitarbeiter=Mitarbeiter.objects.first(),
            startdatum="2022-01-01",
            enddatum="2023-01-01",
            monatlicher_beitrag=50.00,
        )

    def test_versicherungsvertrag_content(self):
        versicherungsvertrag = Versicherungsvertrag.objects.get(id=1)
        self.assertEqual(f"{versicherungsvertrag.vertragsnummer}", "12345")

    def test_form_has_fields(self):
        form = VersicherungsvertragForm()
        expected = [
            "vertragsnummer",
            "kunde",
            "mitarbeiter",
            "startdatum",
            "enddatum",
            "monatlicher_beitrag",
        ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_valid_form(self):
        # Sie müssen gültige Kunden- und Mitarbeiterobjekte erstellen und deren IDs hier verwenden
        data = {
            "vertragsnummer": "123456",
            "kunde": 1,
            "mitarbeiter": 1,
            "startdatum": "01.01.2022",
            "enddatum": "01.01.2023",
            "monatlicher_beitrag": 100.00,
        }
        form = VersicherungsvertragForm(data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        data = {
            "vertragsnummer": "123456",
            "kunde": 1,
            "mitarbeiter": 1,
            "startdatum": "01.01.2022",
            "enddatum": "01.01.2023",
            "monatlicher_beitrag": 100.00,
        }
        form = VersicherungsvertragForm(data)
        vertrag = form.save()
        self.assertEqual(vertrag.vertragsnummer, "123456")


class SchadensfallFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.mitarbeiter = Mitarbeiter.objects.create(
            user=self.user,
            position="agent",
            geburtsdatum="2000-01-01",
            einstellungsdatum="2022-01-01",
            telefonnummer="1234567890",
        )
        self.kunde = Kunde.objects.create(
            vorname="John",
            nachname="Doe",
            email="john@example.com",
            telefonnummer="1234567890",
        )
        self.versicherungsvertrag = Versicherungsvertrag.objects.create(
            vertragsnummer="123456",
            kunde=self.kunde,
            mitarbeiter=self.mitarbeiter,
            startdatum="2022-01-01",
            enddatum="2023-01-01",
            monatlicher_beitrag=100.00,
        )

    def test_form_has_fields(self):
        form = SchadensfallForm()
        expected = ["beschreibung", "versicherungsvertrag", "schadenshoehe", "status"]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_valid_form(self):
        # Sie müssen ein gültiges Versicherungsvertrag-Objekt erstellen und dessen ID hier verwenden
        data = {
            "beschreibung": "Schaden an der Frontseite",
            "versicherungsvertrag": 1,
            "schadenshoehe": 5000.00,
            "status": "offen",
        }
        form = SchadensfallForm(data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        data = {
            "beschreibung": "Schaden an der Frontseite",
            "versicherungsvertrag": 1,
            "schadenshoehe": 5000.00,
            "status": "offen",
        }
        form = SchadensfallForm(data)
        schadensfall = form.save()
        self.assertEqual(schadensfall.beschreibung, "Schaden an der Frontseite")
