import os
from django import setup
from django.test.utils import setup_test_environment, teardown_test_environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_apps.settings")
setup()


from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
import datetime
from versicherung.models import Kunde, Mitarbeiter, Versicherungsvertrag, Schadensfall
from versicherung.forms import (
    MitarbeiterForm,
    KundeForm,
    VersicherungsvertragForm,
    SchadensfallForm,
)


class MitarbeiterModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )
        self.mitarbeiter = Mitarbeiter.objects.create(
            user=self.user,
            position="Agent",
            geburtsdatum="2000-01-01",
            einstellungsdatum="2022-01-01",
            telefonnummer="1234567890",
        )

    def test_user_content(self):
        self.assertEqual(f"{self.mitarbeiter.user.username}", "testuser")

    def test_mitarbeiter_content(self):
        self.assertEqual(f"{self.mitarbeiter.user}", "testuser")
        self.assertEqual(f"{self.mitarbeiter.position}", "Agent")
        self.assertEqual(f"{self.mitarbeiter.geburtsdatum}", "2000-01-01")
        self.assertEqual(f"{self.mitarbeiter.einstellungsdatum}", "2022-01-01")
        self.assertEqual(f"{self.mitarbeiter.telefonnummer}", "1234567890")

    def test_mitarbeiter_str(self):
        self.assertEqual(str(self.mitarbeiter), "testuser")

    def test_mitarbeiter_view(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse("mitarbeiter_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertTemplateUsed(response, "mitarbeiter/mitarbeiter_list.html")


class KundeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Erstelle einen Kunden
        Kunde.objects.create(
            vorname="Test",
            nachname="Kunde",
            email="test@kunde.de",
            telefonnummer="0123456789",
        )

    def test_kunde_content(self):
        kunde = Kunde.objects.get(id=1)
        self.assertEqual(f"{kunde.vorname}", "Test")
        self.assertEqual(f"{kunde.nachname}", "Kunde")
        self.assertEqual(f"{kunde.email}", "test@kunde.de")
        self.assertEqual(f"{kunde.telefonnummer}", "0123456789")

    def test_kunde_str(self):
        kunde = Kunde.objects.get(id=1)
        self.assertEqual(str(kunde), "Test Kunde")


class VersicherungsvertragModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Erstelle einen Kunden, User, Mitarbeiter und Versicherungsvertrag
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()
        mitarbeiter = Mitarbeiter.objects.create(
            user=test_user, position="agent", telefonnummer="0123456789"
        )
        kunde = Kunde.objects.create(
            vorname="Test",
            nachname="Kunde",
            email="test@kunde.de",
            telefonnummer="0123456789",
        )
        Versicherungsvertrag.objects.create(
            vertragsnummer="123456789",
            kunde=kunde,
            mitarbeiter=mitarbeiter,
            startdatum=datetime.date.today(),
            enddatum=datetime.date.today() + datetime.timedelta(days=365),
            monatlicher_beitrag=Decimal("100.00"),
        )

    def test_versicherungsvertrag_content(self):
        versicherungsvertrag = Versicherungsvertrag.objects.get(id=1)
        self.assertEqual(f"{versicherungsvertrag.vertragsnummer}", "123456789")
        self.assertEqual(f"{versicherungsvertrag.kunde}", "Test Kunde")
        self.assertEqual(f"{versicherungsvertrag.mitarbeiter}", "testuser")
        self.assertEqual(versicherungsvertrag.monatlicher_beitrag, Decimal("100.00"))

    def test_versicherungsvertrag_str(self):
        versicherungsvertrag = Versicherungsvertrag.objects.get(id=1)
        self.assertEqual(str(versicherungsvertrag), "123456789")


class SchadensfallModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Erstelle einen Kunden, User, Mitarbeiter, Versicherungsvertrag und Schadensfall
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()
        mitarbeiter = Mitarbeiter.objects.create(
            user=test_user, position="agent", telefonnummer="0123456789"
        )
        kunde = Kunde.objects.create(
            vorname="Test",
            nachname="Kunde",
            email="test@kunde.de",
            telefonnummer="0123456789",
        )
        versicherungsvertrag = Versicherungsvertrag.objects.create(
            vertragsnummer="123456789",
            kunde=kunde,
            mitarbeiter=mitarbeiter,
            startdatum=datetime.date.today(),
            enddatum=datetime.date.today() + datetime.timedelta(days=365),
            monatlicher_beitrag=Decimal("100.00"),
        )
        Schadensfall.objects.create(
            beschreibung="Test Beschreibung",
            versicherungsvertrag=versicherungsvertrag,
            schadenshoehe=Decimal("500.00"),
            status="offen",
        )

    def test_schadensfall_content(self):
        schadensfall = Schadensfall.objects.get(id=1)
        self.assertEqual(f"{schadensfall.beschreibung}", "Test Beschreibung")
        self.assertEqual(f"{schadensfall.versicherungsvertrag}", "123456789")
        self.assertEqual(schadensfall.schadenshoehe, Decimal("500.00"))
        self.assertEqual(f"{schadensfall.status}", "offen")

    def test_schadensfall_str(self):
        schadensfall = Schadensfall.objects.get(id=1)
        self.assertEqual(str(schadensfall), "123456789 - Test Beschreibung")


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
