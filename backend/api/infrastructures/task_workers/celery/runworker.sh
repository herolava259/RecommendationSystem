celery -A api.infrastructures.task_workers.celery.tasks.c_app worker --loglevel=INFO &

celery -A api.infrastructures.task_workers.celery.tasks.c_app flower
