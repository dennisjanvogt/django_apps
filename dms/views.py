from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def dms_index(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            newdoc = Document(title=title, docfile=request.FILES["docfile"])
            newdoc.save()

            return redirect("dms_index")

    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request, "dms_index.html", {"documents": documents, "form": form})
