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

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None

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
        self.cleaned_data["position"]
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

    """ def clean_code(self):
        code = self.cleaned_data.get("code")
        if code != 000:  # Ersetzen Sie 000 durch den erwarteten Code
            raise forms.ValidationError("Ungültiger Code")
        return code """
