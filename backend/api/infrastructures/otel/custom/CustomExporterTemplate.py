from typing import List

from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk.trace import ReadableSpan
import json
import httpx

class CustomHttpExporter(SpanExporter):
    def __init__(self, export_enddpoint: str):
        self.url = export_enddpoint

    def export(self, spans: List[ReadableSpan]):

        for span in spans:
            print(f"Exporting span: {span}")

        with httpx.Client() as client:
            client.post(self.url, json=json.dumps(spans))


    def shutdown(self) -> None:
        pass
