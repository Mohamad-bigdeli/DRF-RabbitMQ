from __future__ import annotations

from django.urls import path

from .views import AnalysisResultView, UploadFileView


app_name = "analyzer"

urlpatterns = [
    path('upload/', UploadFileView.as_view(), name='upload-file'),
    path('results/<int:file_id>/', AnalysisResultView.as_view(), name='analysis-result'),
]
