from django import forms
from .models import Kunde, Mitarbeiter, Schadensfall, Versicherungsvertrag


class MitarbeiterForm(forms.ModelForm):
    class Meta:
        model = Mitarbeiter
        fields = "__all__"


class SchadensfallForm(forms.ModelForm):
    class Meta:
        model = Schadensfall
        fields = "__all__"


class VersicherungsvertragForm(forms.ModelForm):
    class Meta:
        model = Versicherungsvertrag
        fields = "__all__"


class KundeForm(forms.ModelForm):
    class Meta:
        model = Kunde
        fields = "__all__"
