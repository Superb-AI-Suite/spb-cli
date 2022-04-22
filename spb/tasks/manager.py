from uuid import UUID

from spb.projects.project import Project
from .session import Session
from .query import Query
from .task import Task
from spb.core.manager import BaseManager

class TaskManager(BaseManager):
    
    def __init__(self):
        self.session = Session()
        self.query = Query()


    def get_task_list(self, project_id, status_in, page: int = 1, page_size: int = 10):
        QUERY_ID = 'getTaskList'
        self.query.query_id = QUERY_ID

        try:
            query, values = self.query.build_task_list_query(
                project_id = project_id, 
                status_in = status_in,
                page = page,
                page_size = page_size
            )
            response = self.session.execute(query, values)
            result = self.session.extract_task_list(response, QUERY_ID)
            return result

        except Exception as e:
            raise e



    def get_task_by_id(self, task_id: str):
        QUERY_ID = 'getTaskById'
        self.query.query_id = QUERY_ID
        task = Task(id=task_id)

        query_attrs = task.get_attributes_map(include=['id'])
        self.query.attrs.update(query_attrs)

        self.query.required_attrs.extend(task.get_property_names(include=['id']))
        self.query.response_attrs.extend(task.get_property_names())

        try:
            query, values = self.query.build_query()
            response = self.session.execute(query, values)
            result = self.session.extract_task(response, QUERY_ID)
            return result

        except Exception as e:
            raise e


    def get_task_progress_by_id(self, task_id: str):
        QUERY_ID = 'getTaskProgressById'
        self.query.query_id = QUERY_ID
        task = Task(id=task_id)

        query_attrs = task.get_attributes_map(include=['id'])
        self.query.attrs.update(query_attrs)

        self.query.required_attrs.extend(task.get_property_names(include=['id']))
        self.query.response_attrs.extend(
            task.get_property_names(include=['id','progress','total_count', 'status'])
        )

        try:
            query, values = self.query.build_query()
            response = self.session.execute(query, values)
            result = self.session.extract_task_progress(response, QUERY_ID)
            return result

        except Exception as e:
            raise e


    def request_auto_label_task(self, project_id, tags=[]):
        QUERY_ID = 'requestAutoLabelTask'
        self.query.query_id = QUERY_ID
        task = Task()

        self.query.response_attrs.extend(task.get_property_names(include=['id']))

        try:
            query, values = self.query.build_request_autolabel_query(
                project_id = project_id, 
                tags= tags
            )
            response = self.session.execute(query, values)
            result = self.session.extract_autolabel_task(response, QUERY_ID)
            return result

        except Exception as e:
            raise e
