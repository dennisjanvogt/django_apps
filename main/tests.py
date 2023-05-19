import os
from django import setup
from django.test.utils import setup_test_environment, teardown_test_environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_apps.settings")
setup()
setup_test_environment()


from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import MitarbeiterRegisterForm
from .views import index, login_view, logout_view, register_view


class MainViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        print(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["apps"])

    def test_authenticated_user_redirect(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("login"))
        self.assertRedirects(response, reverse("index"))

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], AuthenticationForm)

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], MitarbeiterRegisterForm)

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("index"))
        response = self.client.get(reverse("index"))
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

    def test_index_view_with_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_login_view_with_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("login"))
        self.assertRedirects(response, reverse("index"))

    def test_register_view_with_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("register"))
        self.assertRedirects(response, reverse("index"))

    def test_logout_view_with_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("index"))

    def test_register_view_with_mismatched_passwords(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "abcdef123456",
                "password2": "abcdef654321",
                "position": "manager",
                "geburtsdatum": "01.01.2002",
                "einstellungsdatum": "01.01.2022",
                "telefonnummer": "123456789",
                "code": 000,
            },
        )
        self.assertFormError(
            response,
            "form",
            "password2",
            "Die beiden Passwörter sind nicht identisch.",
        )


class URLTest(TestCase):
    def test_root_url_resolves_to_index_view(self):
        view = resolve("/")
        self.assertEqual(view.func, index)

    def test_login_url_resolves_to_login_view(self):
        view = resolve("/login/")
        self.assertEqual(view.func, login_view)

    def test_register_url_resolves_to_register_view(self):
        view = resolve("/register/")
        self.assertEqual(view.func, register_view)

    def test_logout_url_resolves_to_logout_view(self):
        view = resolve("/logout/")
        self.assertEqual(view.func, logout_view)


class MitarbeiterRegisterFormTest(TestCase):
    def test_form_with_valid_data(self):
        form = MitarbeiterRegisterForm(
            {
                "username": "testuser",
                "password1": "testpassword123",
                "password2": "testpassword123",
                "position": "manager",
                "geburtsdatum": "01.01.2002",
                "einstellungsdatum": "01.01.2022",
                "telefonnummer": "123456789",
                "code": 000,
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_with_missing_data(self):
        form = MitarbeiterRegisterForm({})
        self.assertFalse(form.is_valid())

    def test_form_creates_user_and_mitarbeiter_on_save(self):
        form = MitarbeiterRegisterForm(
            {
                "username": "testuser",
                "password1": "testpassword123",
                "password2": "testpassword123",
                "position": "Position_Wert",
                "geburtsdatum": "01.01.2002",
                "einstellungsdatum": "01.01.2022",
                "telefonnummer": "123456789",
                "code": 000,
            }
        )
        if form.is_valid():
            user = form.save()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testuser")
            mitarbeiter = user.mitarbeiter
            self.assertIsNotNone(mitarbeiter)
            self.assertEqual(mitarbeiter.position, "manager")

    def test_form_with_incorrect_code(self):
        form = MitarbeiterRegisterForm(
            {
                "username": "testuser",
                "password1": "testpassword123",
                "password2": "testpassword123",
                "position": "manager",
                "geburtsdatum": "01.01.2002",
                "einstellungsdatum": "01.01.2022",
                "telefonnummer": "123456789",
                "code": 123,
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_with_mismatched_passwords(self):
        form = MitarbeiterRegisterForm(
            {
                "username": "testuser",
                "password1": "testpassword123",
                "password2": "testpassword456",
                "position": "manager",
                "geburtsdatum": "01.01.2002",
                "einstellungsdatum": "01.01.2022",
                "telefonnummer": "123456789",
                "code": 000,
            }
        )
        self.assertFalse(form.is_valid())
