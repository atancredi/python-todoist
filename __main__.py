import logging

from dotenv import load_dotenv
from os import environ as env

load_dotenv()

from api import get_client
from filters import FilteredTasks

# logger
logger = logging.getLogger("todoist")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

token = env.get("TODOIST_API_KEY")
client = get_client(token,logger)

filtered_tasks = FilteredTasks(client,"daily",logger)
filtered_tasks.pull_tasks()
tasks = filtered_tasks._tasks

print([[_.content for _ in _filtered_tasks["tasks"]] for _filtered_tasks in filtered_tasks])
