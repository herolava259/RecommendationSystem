import asyncio

import logging

from redis.asyncio import Redis
from fastapi import Request, Response, FastAPI
from typing import Dict
import json

REDIS_TASKS_KEY = "tasks" #TODO: setup redis_task_keys later
REDIS_ITEM_TASKS_KEY = "item_tasks" #TODO: setup later
REDIS_PUBSUB_CHANNEL = "prefix:tasks:command" # TODO: setup later

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

tasks: Dict[str, asyncio.Task] = {}
item_tasks = {}


async def redis_tasks_command_listener(app: FastAPI):
    redis: Redis = app.state.redis

    channel_pubsub = redis.pubsub()

    await channel_pubsub.subscribe(REDIS_PUBSUB_CHANNEL)

    async for message in channel_pubsub.listen():
        if message["type"] != "message":
            continue
        try:
            command = json.loads(message["data"])
            if command.get("action") == "stop":
                task_id = command.get("task_id")
                local_task = tasks.get(task_id)
                if local_task:
                    local_task.cancel()

        except Exception as e:
            log.exception(f"Error handling distributed task command: {e}")



