import logging

from fastapi import FastAPI
from starlette.types import ASGIApp

# config
from config import Config
from typing import Literal

# base tracing
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# span, exporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterGRPC,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterHTTP
)

# instrumentation for fast-api, logging
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# inject, provider, batch-span
from opentelemetry.propagate import inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# import prometheus
from prometheus_fastapi_instrumentator import Instrumentator as PrometheusInstrumentor

# import loki for logging
from logging_loki import LokiHandler

# setup tracer

def setting_jaeger(app: ASGIApp, mode: Literal["otlp-grpc", "otlp-http"] = "otlp-grpc", log_correlation: bool = True) -> None:
    tracer = TracerProvider()
    trace.set_tracer_provider(tracer)

    if mode == "otlp-grpc":
        tracer.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporterGRPC(endpoint=Config.JAEGER_GRPC_ADDR, insecure=True)
            )
        )
    elif mode == "otlp-http":
        tracer.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporterHTTP(endpoint=Config.JAEGER_HTTP_ADDR)
            )
        )
    else:
        raise ValueError("Agrument 'mode' is not supported.")

    if log_correlation:
        LoggingInstrumentor().instrument(set_logging_format=True)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)


def setting_prometheus(app: FastAPI):
    # resigter endpoint for prometheus scrape metrics data
    # the endpoint: http://localhost:8000/metrics
    PrometheusInstrumentor().instrument(app).expose(app)


def setup_loki_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = LokiHandler(url=Config.LOKI_ENDPOINT,
                          tags={"application": "rec-fastapi-app"},
                          version="1")
    logger.addHandler(handler)

    return logger
