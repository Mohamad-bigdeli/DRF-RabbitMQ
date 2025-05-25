from django.db import models
from django.db import models
from django.db.models import JSONField
from django.contrib.postgres.indexes import GinIndex 

# Create your models here.

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ])

    def __str__(self):
        return f"{self.file} : {self.status}"

class AnalysisResult(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    results = JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            GinIndex(fields=['results'])
        ]

    def __str__(self):
        return f"result for {self.file.id}"