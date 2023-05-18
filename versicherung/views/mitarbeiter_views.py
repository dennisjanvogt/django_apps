from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group, User

from versicherung.forms import MitarbeiterForm
from versicherung.models import Mitarbeiter

from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def mitarbeiter_list(request: HttpRequest):
    mitarbeiter = Mitarbeiter.objects.all()
    context = {"mitarbeiter_list": mitarbeiter}
    return render(request, "mitarbeiter/mitarbeiter_list.html", context)


@login_required(login_url="login")
def mitarbeiter_create(request: HttpRequest):
    if request.method == "POST":
        form = MitarbeiterForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Mitarbeiter wurde erfolgreich erstellt.")
            return redirect("mitarbeiter_list")
    else:
        form = MitarbeiterForm()
    context = {"form": form}
    return render(request, "mitarbeiter/mitarbeiter_form.html", context)


@login_required(login_url="login")
def mitarbeiter_detail(request: HttpRequest, pk: int):
    mitarbeiter = get_object_or_404(Mitarbeiter, pk=pk)
    context = {"mitarbeiter": mitarbeiter}
    return render(request, "mitarbeiter/mitarbeiter_detail.html", context)


@login_required(login_url="login")
def mitarbeiter_update(request: HttpRequest, pk: int):
    mitarbeiter = get_object_or_404(Mitarbeiter, pk=pk)
    if request.method == "POST":
        form = MitarbeiterForm(request.POST, instance=mitarbeiter)
        if form.is_valid():
            form.save()
            messages.success(request, "Mitarbeiter wurde erfolgreich aktualisiert.")
            return redirect("mitarbeiter_list")
    else:
        form = MitarbeiterForm(instance=mitarbeiter)
    context = {"form": form, "mitarbeiter": mitarbeiter}
    return render(request, "mitarbeiter/mitarbeiter_form.html", context)


@login_required(login_url="login")
def mitarbeiter_delete(request: HttpRequest, pk: int):
    mitarbeiter = get_object_or_404(Mitarbeiter, pk=pk)
    if request.method == "POST":
        mitarbeiter.delete()
        messages.success(request, "Mitarbeiter wurde erfolgreich gelöscht.")
        return redirect("mitarbeiter_list")
    context = {"mitarbeiter": mitarbeiter}
    return render(request, "mitarbeiter/mitarbeiter_confirm_delete.html", context)
