from django.contrib import admin

from .models import Kunde, Mitarbeiter, Schadensfall, Versicherungsvertrag

# Register your models here.
admin.site.register(Kunde)
admin.site.register(Mitarbeiter)
admin.site.register(Schadensfall)
admin.site.register(Versicherungsvertrag)
