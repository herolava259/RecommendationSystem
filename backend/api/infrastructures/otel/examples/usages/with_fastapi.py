
#utilities
from typing import Optional
import json

from fastapi import FastAPI
import uvicorn

import logging
import time
import random
import httpx
from fastapi.openapi.models import Response

from opentelemetry import trace
from opentelemetry.propagate import inject
from opentelemetry.metrics import get_meter

from infrastructures.otel.setup import setting_jaeger, setting_prometheus, setup_loki_logger

# with prometheus
from prometheus_client import Counter as PrometheusCounter
from prometheus_fastapi_instrumentator import Instrumentator as PrometheusInstrumentor

app = FastAPI(
    summary="This is some example about using otel with fast-api",
    description="This is some example about using otel with fast-api",
    version="0.0.1",
    openapi_prefix="/openapi/otel-example/",
    root_path="/openapi/otel-example/usage",
)

# setting jaeger
setting_jaeger(app)

@app.get("/")
async def root():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("root_request") as span:
        return {"massage": "Hello, It is the first example of FatAPI with Open-Telemetry"}

@app.get("/user/{user_id}")
async def get_user(user_id: str):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("user_request") as span:
        return {"message": f"Echoing {user_id}"}

# logging examples

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    logging.error("items")
    return {"item_id": item_id, "q": q}

@app.get("io_task")
async def io_task():
    time.sleep(1)
    logging.error("io_task")
    return "IO bound task finished"

@app.get("/cpu_task")
async def cpu_task():
    for i in range(1000):
        _ = i**3
    logging.error("cpu_task")
    return "CPU bound task finished"


@app.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 5))
    logging.error("random_sleep")

    return {"path": "/random_sleep"}


@app.get("chain")
async def chain(response: Response):
    headers = {}
    inject(headers)

    logging.critical(headers)

    async with httpx.AsyncClient() as client:
        await client.get(
            "http://localhost:8000/",
            headers=headers,
        )
    async with httpx.AsyncClient() as client:
        await client.get(
            "http://localhost:8000/io_task",
            headers=headers,
        )
    async with httpx.AsyncClient() as client:
        await client.get(
            "https://localhost:8000/cpu_task",
            headers=headers
        )

    logging.info("Chain finished")

    return {"path": "/chain"}

# example with meter
meter = get_meter(__name__)

request_counter = meter.create_counter(
    "custom_request_counter", description="Trackings custom requests"
)
@app.get("/track/counting_request")
async def track_counting_request():
    request_counter.add(1)

    return {"message": "Request traced"}

# setting up with prometheus

# define metrics
predict_counter = PrometheusCounter("prediction_requests_total",
                                    "Total number of prediction requests",)

@app.get("predict")
async def predict():
    predict_counter.inc()
    return {"message": "Prediction traced"}

setting_prometheus(app)

#########
# - example using loki to logging
########
loki_logger = setup_loki_logger(__name__)
@app.get("/demo/logging-loki")
def logging_loki():
    loki_logger.info("Hello from ")
    loki_logger.info("Hello from FastAPI!", extra={"tags": {"endpoint": "/"}})
    return {"message": "Hello loki"}

@app.get("/demo/logging-loki/with-json-dumps")
def logging_loki_with_json_dumps():
    loki_logger.info(json.dumps({"event": "user_login", "user_id": 123}))

    return {"message": "Try Loki Logger with json dumps use case"}

@app.get("/demo/logging-loki/with-error")
def logging_loki_with_error():
    try:
        1/0
    except ZeroDivisionError as err:
        loki_logger.exception("Error occurred!", extra={"tags": {"endpoint": "/error"}})
    return {"error": "logged"}

if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=80, log_config=log_config)