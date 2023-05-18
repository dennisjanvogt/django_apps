from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from versicherung.models import Mitarbeiter


class MitarbeiterRegisterForm(UserCreationForm):
    position = forms.ChoiceField(choices=Mitarbeiter.POSITION_CHOICES)
    geburtsdatum = forms.DateField()
    einstellungsdatum = forms.DateField()
    telefonnummer = forms.CharField()
    code = forms.IntegerField()

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "position",
            "geburtsdatum",
            "einstellungsdatum",
            "telefonnummer",
            "code",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.save()

        mitarbeiter = Mitarbeiter(
            user=user,
            position=self.cleaned_data["position"],
            geburtsdatum=self.cleaned_data["geburtsdatum"],
            einstellungsdatum=self.cleaned_data["einstellungsdatum"],
            telefonnummer=self.cleaned_data["telefonnummer"],
        )
        if commit:
            mitarbeiter.save()

        return user
