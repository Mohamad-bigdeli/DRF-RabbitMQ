from rest_framework import serializers
from .models import AnalysisResult, UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'status', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at', 'status']

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("File must be a CSV file.")
        max_size = 10 * 1024 * 1024  
        if value.size > max_size:
            raise serializers.ValidationError("File size cannot exceed 10MB.")
        return value


class AnalysisResultSerializer(serializers.ModelSerializer):
    file_id = serializers.PrimaryKeyRelatedField(source='file', queryset=UploadedFile.objects.all(), write_only=True)
    file_info = UploadedFileSerializer(source='file', read_only=True)

    class Meta:
        model = AnalysisResult
        fields = ['id', 'file_id', 'file_info', 'results', 'created_at']
        read_only_fields = ['id', 'file_info', 'results', 'created_at']

    def validate_results(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Results must be a valid JSON object.")
        return value