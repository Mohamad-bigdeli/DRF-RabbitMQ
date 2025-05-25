from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import AnalysisResult
from .serializers import UploadedFileSerializer, AnalysisResultSerializer
from utils.rabbitmq_client import RabbitMQClient

class UploadFileView(GenericAPIView):
    serializer_class = UploadedFileSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save(status='pending')

            client = RabbitMQClient()
            message = {
                'file_id': uploaded_file.id,
                'file_path': uploaded_file.file.path
            }
            try:
                client.publish_message(queue='analyzer_queue', message=message, routing_key="analyze_queue")
                return Response({'message': 'File uploaded and queued for processing', 'file_id': uploaded_file.id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                uploaded_file.status = 'failed'
                uploaded_file.save()
                return Response({'error': f'Failed to queue file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnalysisResultView(GenericAPIView):
    serializer_class = AnalysisResultSerializer

    def get(self, request, file_id, *args, **kwargs):
        try:
            result = AnalysisResult.objects.get(file_id=file_id)
            serializer = self.get_serializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AnalysisResult.DoesNotExist:
            return Response({'error': 'Analysis result not found'}, status=status.HTTP_404_NOT_FOUND)