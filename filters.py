from collections.abc import Iterator
from logging import Logger
from typing import List, Any, Optional
from yaml import safe_load

# Only for typing, doesnt raise circular dep error
from todoist_api_python.api import TodoistAPI

# FILTERS
def get_filters(filtered_view: Optional[str] = None, path: str = "filters.yml") -> List[str] | str:
    config = safe_load(open(path,"r"))
    try:
        if filtered_view:
            return config[filtered_view]["filters"]
        else: return config
    except KeyError:
        print(f"Filters '{filtered_view}' not found.")

class FilteredTasks(list):

    client: TodoistAPI
    filters: List[str] | str
    logger: Logger
    _tasks: List[dict]

    def __init__(self, client: TodoistAPI, filtered_view: str, logger: Optional[Logger] = None) -> None:
        self.client = client
        self.logger = logger
        self.filters = get_filters(filtered_view=filtered_view)
        self._tasks = []
    
    def pull_tasks(self):
        if isinstance(self.filters,list):
            for _filter in self.filters:
                self.logger.info(f"Filter: {_filter}")
                tasks = self.client.get_tasks(filter=_filter)
                self._tasks.append({
                    "filter": _filter,
                    "tasks": tasks
                })
        elif isinstance(self.filters,str):
            tasks = self.client.get_tasks(filter=self.filters)
            self._tasks.append({
                    "filter": self.filters,
                    "tasks": tasks
                })
            
    def __iter__(self) -> Iterator:
        return self._tasks.__iter__()