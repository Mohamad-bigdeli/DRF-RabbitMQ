from __future__ import annotations

from django.contrib import admin

from .models import AnalysisResult, UploadedFile


# Register your models here.

admin.site.register(AnalysisResult)
admin.site.register(UploadedFile)
