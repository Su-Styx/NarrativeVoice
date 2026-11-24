from django.db import models
from django.conf import settings
# Create your models here.

class Document(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    pdf = models.FileField(upload_to="pdfs/", null=True, blank=True)
    status = models.CharField(max_length=10, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.JSONField(null=True, blank=True)
    error = models.TextField(blank=True, default="")