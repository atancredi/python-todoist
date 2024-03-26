from logging import Logger
from todoist_api_python.api import TodoistAPI

def get_client(token: str, logger: Logger):
    logger.info("Starting Todoist API")
    return TodoistAPI(token)