from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Mitarbeiter(models.Model):
    POSITION_CHOICES = [
        ("agent", "Agent"),
        ("manager", "Manager"),
        ("support", "Support"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    position = models.CharField(
        max_length=100,
        choices=POSITION_CHOICES,
        null=True,
    )
    geburtsdatum = models.DateField(null=True)
    einstellungsdatum = models.DateField(null=True)
    telefonnummer = models.CharField(max_length=15, unique=True, null=True)

    def __str__(self):
        return self.user.username


class Kunde(models.Model):
    vorname = models.CharField(max_length=50)
    nachname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefonnummer = models.CharField(max_length=15, unique=True)
    erstellt_am = models.DateTimeField(auto_now_add=True)
    aktualisiert_am = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vorname} {self.nachname}"


class Versicherungsvertrag(models.Model):
    vertragsnummer = models.CharField(max_length=20, unique=True)
    kunde = models.ForeignKey(Kunde, on_delete=models.CASCADE)
    mitarbeiter = models.ForeignKey(Mitarbeiter, on_delete=models.SET_NULL, null=True)
    startdatum = models.DateField()
    enddatum = models.DateField()
    monatlicher_beitrag = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    abgeschlossen_am = models.DateTimeField(auto_now_add=True)
    aktualisiert_am = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vertragsnummer


class Schadensfall(models.Model):
    STATUS_CHOICES = [
        ("offen", "Offen"),
        ("bearbeitet", "Bearbeitet"),
        ("abgeschlossen", "Abgeschlossen"),
    ]

    beschreibung = models.TextField()
    versicherungsvertrag = models.ForeignKey(
        Versicherungsvertrag, on_delete=models.CASCADE
    )
    schadenshoehe = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    erstellt_am = models.DateTimeField(auto_now_add=True)
    aktualisiert_am = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.versicherungsvertrag} - {self.beschreibung}"
