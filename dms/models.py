from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    docfile = models.FileField(upload_to="dms/documents/%Y/%m/%d/%H/%M/%S")
