import os
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_apps.settings")
setup()

from versicherung.factories import (
    MitarbeiterFactory,
    UserFactory,
    KundeFactory,
    VersicherungsvertragFactory,
    SchadensfallFactory,
)

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from decimal import Decimal
import datetime
from versicherung.models import Kunde, Mitarbeiter, Versicherungsvertrag, Schadensfall
from versicherung.forms import (
    MitarbeiterForm,
    KundeForm,
    VersicherungsvertragForm,
    SchadensfallForm,
)
from .views.mitarbeiter_views import (
    mitarbeiter_list,
    mitarbeiter_create,
    mitarbeiter_delete,
    mitarbeiter_detail,
    mitarbeiter_update,
)

from .views.kunde_views import (
    kunde_list,
    kunde_create,
    kunde_delete,
    kunde_detail,
    kunde_update,
)

from .views.versicherungsvertrag_views import (
    versicherungsvertrag_create,
    versicherungsvertrag_delete,
    versicherungsvertrag_detail,
    versicherungsvertrag_list,
    versicherungsvertrag_update,
)

from .views.schadensfall_views import (
    schadensfall_create,
    schadensfall_delete,
    schadensfall_detail,
    schadensfall_list,
    schadensfall_update,
)

# MITARBEITER


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


class MitarbeiterViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.mitarbeiter = MitarbeiterFactory.create(user=self.user)

    # Test für die Views
    def test_mitarbeiter_list_view(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("mitarbeiter_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.mitarbeiter.user.username)

    def test_mitarbeiter_create_view(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("mitarbeiter_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        new_user = UserFactory.create()
        response = self.client.post(
            url,
            {
                "user": new_user.pk,
                "position": "support",
                "geburtsdatum": "1990-01-01",
                "einstellungsdatum": "2020-01-01",
                "telefonnummer": "9876543210",
            },
        )
        self.assertEqual(response.status_code, 302)  # redirect to detail view
        self.assertEqual(Mitarbeiter.objects.filter(user=new_user).count(), 1)

    def test_mitarbeiter_detail_view(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("mitarbeiter_detail", args=[self.mitarbeiter.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.mitarbeiter.user.username)

    def test_mitarbeiter_update_view(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("mitarbeiter_update", args=[self.mitarbeiter.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url,
            {
                "user": self.mitarbeiter.user.pk,
                "position": "manager",
                "geburtsdatum": self.mitarbeiter.geburtsdatum,
                "einstellungsdatum": self.mitarbeiter.einstellungsdatum,
                "telefonnummer": self.mitarbeiter.telefonnummer,
            },
        )
        self.assertEqual(response.status_code, 302)  # redirect to detail view
        self.mitarbeiter.refresh_from_db()
        self.assertEqual(self.mitarbeiter.position, "manager")

    def test_mitarbeiter_delete_view(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("mitarbeiter_delete", args=[self.mitarbeiter.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # redirect to list view
        self.assertEqual(Mitarbeiter.objects.filter(pk=self.mitarbeiter.pk).count(), 0)


class MitarbeiterUrlsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create()
        self.mitarbeiter = MitarbeiterFactory.create(user=self.user)

    def test_mitarbeiter_list_url_resolves(self):
        url = reverse("mitarbeiter_list")
        self.assertEqual(resolve(url).func, mitarbeiter_list)

    def test_mitarbeiter_create_url_resolves(self):
        url = reverse("mitarbeiter_create")
        self.assertEqual(resolve(url).func, mitarbeiter_create)

    def test_mitarbeiter_detail_url_resolves(self):
        url = reverse("mitarbeiter_detail", args=[self.mitarbeiter.pk])
        self.assertEqual(resolve(url).func, mitarbeiter_detail)

    def test_mitarbeiter_update_url_resolves(self):
        url = reverse("mitarbeiter_update", args=[self.mitarbeiter.pk])
        self.assertEqual(resolve(url).func, mitarbeiter_update)

    def test_mitarbeiter_delete_url_resolves(self):
        url = reverse("mitarbeiter_delete", args=[self.mitarbeiter.pk])
        self.assertEqual(resolve(url).func, mitarbeiter_delete)


# KUNDE


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


class KundeViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.kunde = KundeFactory.create()

    # Test für die Views
    def test_kunde_list_view(self):
        url = reverse("kunde_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.kunde.vorname)

    def test_kunde_create_view(self):
        url = reverse("kunde_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url,
            {
                "vorname": "Max",
                "nachname": "Mustermann",
                "email": "max@example.com",
                "telefonnummer": "+49 987654321",
            },
        )
        self.assertEqual(response.status_code, 302)  # redirect to list view
        self.assertEqual(Kunde.objects.filter(email="max@example.com").count(), 1)

    def test_kunde_detail_view(self):
        url = reverse("kunde_detail", args=[self.kunde.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.kunde.vorname)

    def test_kunde_update_view(self):
        url = reverse("kunde_update", args=[self.kunde.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url,
            {
                "vorname": self.kunde.vorname,
                "nachname": "Updated",
                "email": self.kunde.email,
                "telefonnummer": self.kunde.telefonnummer,
            },
        )
        self.assertEqual(response.status_code, 302)  # redirect to list view
        self.kunde.refresh_from_db()
        self.assertEqual(self.kunde.nachname, "Updated")

    def test_kunde_delete_view(self):
        url = reverse("kunde_delete", args=[self.kunde.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # redirect to list view
        self.assertEqual(Kunde.objects.filter(pk=self.kunde.pk).count(), 0)


class KundeUrlsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.kunde = KundeFactory.create()

    def test_kunde_list_url_resolves(self):
        url = reverse("kunde_list")
        self.assertEqual(resolve(url).func, kunde_list)

    def test_kunde_create_url_resolves(self):
        url = reverse("kunde_create")
        self.assertEqual(resolve(url).func, kunde_create)

    def test_kunde_detail_url_resolves(self):
        url = reverse("kunde_detail", args=[self.kunde.pk])
        self.assertEqual(resolve(url).func, kunde_detail)

    def test_kunde_update_url_resolves(self):
        url = reverse("kunde_update", args=[self.kunde.pk])
        self.assertEqual(resolve(url).func, kunde_update)

    def test_kunde_delete_url_resolves(self):
        url = reverse("kunde_delete", args=[self.kunde.pk])
        self.assertEqual(resolve(url).func, kunde_delete)


# VERSICHERUNGSVERTRAG


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


class VersicherungsvertragViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.versicherungsvertrag = VersicherungsvertragFactory.create()

    def test_versicherungsvertrag_list_view(self):
        url = reverse("versicherungsvertrag_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.versicherungsvertrag.vertragsnummer)

    def test_versicherungsvertrag_create_view(self):
        url = reverse("versicherungsvertrag_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        kunde = KundeFactory.create()
        mitarbeiter = MitarbeiterFactory.create()
        response = self.client.post(
            url,
            {
                "vertragsnummer": "12345678",
                "kunde": kunde.id,
                "mitarbeiter": mitarbeiter.id,
                "startdatum": "2023-01-01",
                "enddatum": "2024-01-01",
                "monatlicher_beitrag": "50.00",
            },
        )
        self.assertEqual(response.status_code, 302)  # redirect to list view
        self.assertEqual(
            Versicherungsvertrag.objects.filter(vertragsnummer="12345678").count(), 1
        )

    def test_versicherungsvertrag_detail_view(self):
        url = reverse(
            "versicherungsvertrag_detail", args=[self.versicherungsvertrag.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.versicherungsvertrag.vertragsnummer)

    def test_versicherungsvertrag_update_view(self):
        url = reverse(
            "versicherungsvertrag_update", args=[self.versicherungsvertrag.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url,
            {
                "vertragsnummer": "12345678",
                "kunde": self.versicherungsvertrag.kunde.id,
                "mitarbeiter": self.versicherungsvertrag.mitarbeiter.id,
                "startdatum": self.versicherungsvertrag.startdatum,
                "enddatum": self.versicherungsvertrag.enddatum,
                "monatlicher_beitrag": "60.00",
            },
        )
        self.assertEqual(response.status_code, 302)  # redirect to list view
        self.versicherungsvertrag.refresh_from_db()
        self.assertEqual(
            self.versicherungsvertrag.monatlicher_beitrag, Decimal("60.00")
        )

    def test_versicherungsvertrag_delete_view(self):
        url = reverse(
            "versicherungsvertrag_delete", args=[self.versicherungsvertrag.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # redirect to list view
        self.assertEqual(
            Versicherungsvertrag.objects.filter(
                pk=self.versicherungsvertrag.pk
            ).count(),
            0,
        )


class VersicherungsvertragUrlsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.versicherungsvertrag = VersicherungsvertragFactory.create()

    def test_versicherungsvertrag_list_url_resolves(self):
        url = reverse("versicherungsvertrag_list")
        self.assertEqual(resolve(url).func, versicherungsvertrag_list)

    def test_versicherungsvertrag_create_url_resolves(self):
        url = reverse("versicherungsvertrag_create")
        self.assertEqual(resolve(url).func, versicherungsvertrag_create)

    def test_versicherungsvertrag_detail_url_resolves(self):
        url = reverse(
            "versicherungsvertrag_detail", args=[self.versicherungsvertrag.pk]
        )
        self.assertEqual(resolve(url).func, versicherungsvertrag_detail)

    def test_versicherungsvertrag_update_url_resolves(self):
        url = reverse(
            "versicherungsvertrag_update", args=[self.versicherungsvertrag.pk]
        )
        self.assertEqual(resolve(url).func, versicherungsvertrag_update)

    def test_versicherungsvertrag_delete_url_resolves(self):
        url = reverse(
            "versicherungsvertrag_delete", args=[self.versicherungsvertrag.pk]
        )
        self.assertEqual(resolve(url).func, versicherungsvertrag_delete)


# SCHADENSFALL


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


class SchadensfallViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.schadensfall = SchadensfallFactory.create()

    def test_schadensfall_list_view(self):
        url = reverse("schadensfall_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, str(self.schadensfall.schadenshoehe).replace(".", ",")
        )
        self.assertContains(response, self.schadensfall.status)

    def test_schadensfall_create_view(self):
        url = reverse("schadensfall_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        versicherungsvertrag = VersicherungsvertragFactory.create()
        response = self.client.post(
            url,
            {
                "beschreibung": "Wasserschaden im Keller",
                "versicherungsvertrag": versicherungsvertrag.id,
                "schadenshoehe": "2500.00",
                "status": "offen",
            },
        )
        self.assertEqual(response.status_code, 302)  # redirect to list view
        self.assertEqual(
            Schadensfall.objects.filter(beschreibung="Wasserschaden im Keller").count(),
            1,
        )

    def test_schadensfall_detail_view(self):
        url = reverse("schadensfall_detail", args=[self.schadensfall.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.schadensfall.beschreibung)

    def test_schadensfall_update_view(self):
        url = reverse("schadensfall_update", args=[self.schadensfall.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url,
            {
                "beschreibung": self.schadensfall.beschreibung,
                "versicherungsvertrag": self.schadensfall.versicherungsvertrag.id,
                "schadenshoehe": self.schadensfall.schadenshoehe,
                "status": "bearbeitet",
            },
        )
        self.assertEqual(response.status_code, 302)  # redirect to list view
        self.schadensfall.refresh_from_db()
        self.assertEqual(self.schadensfall.status, "bearbeitet")

    def test_schadensfall_delete_view(self):
        url = reverse("schadensfall_delete", args=[self.schadensfall.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # redirect to list view
        self.assertEqual(
            Schadensfall.objects.filter(pk=self.schadensfall.pk).count(), 0
        )


class SchadensfallUrlsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.schadensfall = SchadensfallFactory.create()

    def test_schadensfall_list_url_resolves(self):
        url = reverse("schadensfall_list")
        self.assertEqual(resolve(url).func, schadensfall_list)

    def test_schadensfall_create_url_resolves(self):
        url = reverse("schadensfall_create")
        self.assertEqual(resolve(url).func, schadensfall_create)

    def test_schadensfall_detail_url_resolves(self):
        url = reverse("schadensfall_detail", args=[self.schadensfall.pk])
        self.assertEqual(resolve(url).func, schadensfall_detail)

    def test_schadensfall_update_url_resolves(self):
        url = reverse("schadensfall_update", args=[self.schadensfall.pk])
        self.assertEqual(resolve(url).func, schadensfall_update)

    def test_schadensfall_delete_url_resolves(self):
        url = reverse("schadensfall_delete", args=[self.schadensfall.pk])
        self.assertEqual(resolve(url).func, schadensfall_delete)
