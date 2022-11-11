from .session import Session
from .query import Query
from .task import Task
from spb.core.manager import BaseManager

class TaskManager(BaseManager):
    
    def __init__(self, team_name=None, access_key=None):
        self.session = Session(
            team_name = team_name,
            access_key = access_key
        )
        self.query = Query()


    def get_task_list(self, project_id, status_in, page: int = 1, page_size: int = 10):
        QUERY_ID = 'getTaskList'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_task_list_query(
            project_id = project_id, 
            status_in = status_in,
            page = page,
            page_size = page_size
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task_list(response, QUERY_ID)
        return result



    def get_task_by_id(self, task_id: str):
        QUERY_ID = 'getTaskById'
        self.query.query_id = QUERY_ID
        task = Task(id=task_id)

        query_attrs = task.get_attributes_map(include=['id'])
        self.query.attrs.update(query_attrs)

        self.query.required_attrs.extend(task.get_property_names(include=['id']))
        self.query.response_attrs.extend(task.get_property_names())

        query, values = self.query.build_query()
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result


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

        query, values = self.query.build_query()
        response = self.session.execute(query, values)
        result = self.session.extract_task_progress(response, QUERY_ID)
        return result


    def request_auto_label_task(self, project_id, tags=[]):
        QUERY_ID = 'requestAutoLabelTask'
        self.query.query_id = QUERY_ID
        task = Task()

        self.query.response_attrs.extend(task.get_property_names(include=['id']))

        query, values = self.query.build_request_autolabel_query(
            project_id = project_id, 
            tags= tags
        )
        response = self.session.execute(query, values)
        result = self.session.extract_autolabel_task(response, QUERY_ID)
        return result

    def assign_reviewer(self, project_id: str, tags: list, limit: int, distribution_method: str, work_assignee: list=[]):
        QUERY_ID = 'assignReviewerTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_assign_reviewer_task_query(
            project_id = project_id, 
            tags = tags,
            limit=limit,
            distribution_method=distribution_method,
            work_assignee = work_assignee
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result
            

    def unassign_reviewer(self, project_id: str, tags: list=[]):
        QUERY_ID = 'unassignReviewerTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_unassign_reviewer_task_query(
            project_id = project_id, 
            tags = tags
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result

    def assign_labeler(self, project_id: str, tags: list, limit: int, distribution_method: str, work_assignee: list=[]):
        QUERY_ID = 'assignLabelerTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_assign_labeler_task_query(
            project_id = project_id, 
            tags = tags,
            limit=limit,
            distribution_method=distribution_method,
            work_assignee = work_assignee
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result

    
    def unassign_labeler(self, project_id: str, tags: list=[]):
        QUERY_ID = 'unassignLabelerTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_unassign_labeler_task_query(
            project_id = project_id, 
            tags = tags
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result

    def initialize_label(self, project_id: str, tags: list=[]):
        QUERY_ID = 'initializeLabelTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_initialize_label_task_query(
            project_id = project_id, 
            tags = tags
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result

    def submit_label(self, project_id: str, tags: list=[]):
        QUERY_ID = 'submitLabelTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_submit_label_task_query(
            project_id = project_id, 
            tags = tags
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result


    def skip_label(self, project_id: str, tags: list=[]):
        QUERY_ID = 'skipLabelTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_skip_label_task_query(
            project_id = project_id,
            tags = tags
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result


    # def edit_label_tags(self, project_id: str, label_ids: list=[], add_tags: list=[], remove_tags: list=[]):
    #     QUERY_ID = 'editLabelTagsTask'
    #     self.query.query_id = QUERY_ID

    #     try:
    #         query, values = self.query.build_edit_label_tags_query(
    #             project_id = project_id, 
    #             label_ids = label_ids,
    #             add_tags = add_tags,
    #             remove_tags = remove_tags
    #         )
    #         response = self.session.execute(query, values)
    #         result = self.session.extract_task(response, QUERY_ID)
    #         return result

    #     except Exception as e:
    #         raise e