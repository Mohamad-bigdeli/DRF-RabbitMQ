from __future__ import annotations

import json
import os
import threading
import time

from utils.analyze_csv import analyze_csv
from utils.rabbitmq_client import RabbitMQClient

from .models import AnalysisResult, UploadedFile


class AnalyzerConsumer(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)
        self.rabbitmq_client = RabbitMQClient()

    def callback(self, ch, method, properties, body):
        print(f"[Callback] Received raw message: {body}")

        try:
            message = json.loads(body)
            print(f"[Callback] Parsed message: {message}")

            file_id = message.get("file_id")
            file_path = message.get("file_path")

            if not file_id or not file_path:
                print("[Callback] Invalid message: missing file_id or file_path")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            try:
                uploadedfile = UploadedFile.objects.get(id=file_id)
            except UploadedFile.DoesNotExist:
                print(f"[Callback] UploadedFile with ID {file_id} does not exist.")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            print(f"[Callback] File found: ID={file_id}, updating status to 'processing'")
            uploadedfile.status = "processing"
            uploadedfile.save()

            if not os.path.exists(file_path):
                print(f"[Callback] File does NOT exist on disk at: {file_path}")
                uploadedfile.status = "failed"
                uploadedfile.save()
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            print(f"[Callback] File exists, starting analysis for: {file_path}")
            results = analyze_csv(file_path)
            time.sleep(7)

            if results:
                print("[Callback] Analysis completed successfully.")
                uploadedfile.status = "completed"
                AnalysisResult.objects.create(file=uploadedfile, results=results)
            else:
                print("[Callback] Analysis failed or returned empty.")
                uploadedfile.status = "failed"

            uploadedfile.save()
            print("[Callback] Processing complete and message acknowledged.")

        except Exception as e:
            print(f"[Callback] Exception occurred: {e}")

    def run(self):
        print("consumer running in thread...")
        self.rabbitmq_client.consume_message(queue="analyzer_queue", callback=self.callback)


