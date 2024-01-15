# tasks.py

from huey.contrib.djhuey import task

@task()
def my_task():
    # Logica della tua attività
    print(f"Task eseguito")
