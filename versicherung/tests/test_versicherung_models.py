import os
from django import setup
from django.test.utils import setup_test_environment, teardown_test_environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_apps.settings")
setup()
teardown_test_environment()
setup_test_environment()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
import datetime
from versicherung.models import Kunde, Mitarbeiter, Versicherungsvertrag, Schadensfall


class MitarbeiterModelTest(TestCase):
    def setUp(self):
        # Erstelle einen Client
        self.client = Client()
        # Erstelle einen User
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )
        # Erstelle einen Mitarbeiter
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
