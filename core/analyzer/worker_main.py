from __future__ import annotations

import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from analyzer.worker import AnalyzerConsumer


if __name__ == "__main__":
    max_retries = 5
    retry = 0
    while retry < max_retries:
        try:
            consumer = AnalyzerConsumer()
            consumer.start()
            consumer.join()
            break
        except Exception as e:
            print(f"Worker error: {e}, retrying...")
            retry += 1
