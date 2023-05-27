from django.shortcuts import render


# Create your views here.
def dms_index(request):
    context = {}

    render(request, "dms_index.html", context)
