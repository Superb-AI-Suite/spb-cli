from typing import Optional, Dict
from datetime import datetime

from .session import Session
from .query import Query
from .task import Task
from spb.core.manager import BaseManager
from spb.labels.manager import LabelManager
from spb.exceptions import ParameterException
from spb.projects.project import Project
from spb.utils import SearchFilter


class TaskManager(BaseManager):
    
    def __init__(self, team_name=None, access_key=None):
        self.session = Session(
            team_name = team_name,
            access_key = access_key
        )
        self.team_name = team_name
        self.access_key = access_key
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

    def request_auto_label_task(self, project_id, tags=[], filter: Optional[SearchFilter] = None):
        if filter is None:
            filter = SearchFilter()
        filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        QUERY_ID = 'requestAutoLabelTask'
        self.query.query_id = QUERY_ID
        task = Task()

        self.query.response_attrs.extend(task.get_property_names(include=['id']))

        query, values = self.query.build_request_autolabel_query(
            project_id=project_id,
            filter=filter
        )
        response = self.session.execute(query, values)
        result = self.session.extract_autolabel_task(response, QUERY_ID)
        return result

    def export_labels_task(
            self,
            project: Project,
            export_name: Optional[str] = None,
            tags: list = [],
            filter: Optional[SearchFilter] = None,
            request_custom_auto_label: bool = False,
            request_transform: bool = False,
            custom_auto_label_configuration: Optional[Dict[str, str]] = None,
            transform_configuration: Optional[Dict[str, str]] = None
    ):
        """Request export labels

        Args:
            project_id (string): project id to request
            export_name (Optional[string]): Export name to be made (default auto generation)
            tags (List[string]): tag names to be exported of labels
            filter (SearchFilter): filter to search labels (working with tags)
            request_custom_auto_label (boolean): Request custom auto label with this export
            request_transform (boolean): Request export transform with this export
            custom_auto_label_configuration (Optional[Dict[str, str]]):
                Custom auto label configuration (format : {"name": "CUSTOM_AUTO_LABEL_NAME"})
            transform_configuration (Optional[Dict[str, str]]):
                Export transform configuration (format : {"type": "COCO" | "YOLO"})
        
        Returns:
            Task: export labels task
        """
        if filter is None:
            filter = SearchFilter()
        filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        if request_transform:
            if not isinstance(transform_configuration, dict):
                raise ParameterException("[ERROR] request transform must be with transform configuration")
            if "type" not in transform_configuration.keys():
                raise ParameterException("[ERROR] transform configuration need to define [type]")
            if transform_configuration["type"] not in ["YOLO", "COCO"]:
                raise ParameterException("[ERROR] transform type must be in ['YOLO', 'COCO']")
        if request_custom_auto_label:
            if custom_auto_label_configuration is None:
                custom_auto_label_configuration = {"name": None}
            elif isinstance(custom_auto_label_configuration, dict):
                custom_auto_label_configuration = {
                    "name": custom_auto_label_configuration.get("name")
                }
            else:
                raise ParameterException("[ERROR] custom_auto_label_configuration must be dict")

        if export_name is None:
            current_time = datetime.now()
            export_name = f"{project.name} {current_time.strftime('%Y-%m-%d %H%M%S')}"
        if request_custom_auto_label and custom_auto_label_configuration["name"] is None:
            custom_auto_label_configuration["name"] = export_name
        QUERY_ID = 'exportLabelsTask'
        self.query.query_id = QUERY_ID
        task = Task()

        label_manager = LabelManager(team_name=self.team_name, access_key=self.access_key)
        label_count = label_manager.search_labels_count(
            project=project,
            filter=filter
        )

        self.query.response_attrs.extend(task.get_property_names(include=['id']))
        query, values = self.query.build_export_labels_task_query(
            project_id=project.id,
            name=export_name,
            filter=filter,
            label_count=label_count,
            custom_auto_label=custom_auto_label_configuration if request_custom_auto_label else None,
            transform=transform_configuration if request_transform else None
        )
        response = self.session.execute(query, values)
        result = self.session.extract_labels_export_task(response, QUERY_ID)
        return result

    def assign_reviewer(
        self,
        project_id: str,
        tags: Optional[list],
        limit: int,
        distribution_method: str,
        work_assignee: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if filter is None:
            filter = SearchFilter()
        filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        QUERY_ID = 'assignReviewerTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_assign_reviewer_task_query(
            project_id=project_id,
            filter=filter,
            limit=limit,
            distribution_method=distribution_method,
            work_assignee=work_assignee
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result
            
    def unassign_reviewer(
        self,
        project_id: str,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if filter is None:
            filter = SearchFilter()
        filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        QUERY_ID = 'unassignReviewerTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_unassign_reviewer_task_query(
            project_id=project_id,
            filter=filter
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result

    def assign_labeler(
        self,
        project_id: str,
        tags: list,
        filter: Optional[SearchFilter],
        limit: int,
        distribution_method: str,
        work_assignee: list=[]
    ):
        if filter is None:
            filter = SearchFilter()
        filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        QUERY_ID = 'assignLabelerTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_assign_labeler_task_query(
            project_id=project_id,
            filter=filter,
            limit=limit,
            distribution_method=distribution_method,
            work_assignee=work_assignee
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result

    def unassign_labeler(
        self,
        project_id: str,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if filter is None:
            filter = SearchFilter()
        filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        QUERY_ID = 'unassignLabelerTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_unassign_labeler_task_query(
            project_id=project_id,
            filter=filter
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result

    def initialize_label(
        self,
        project_id: str,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if filter is None:
            filter = SearchFilter()
        filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        QUERY_ID = 'initializeLabelTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_initialize_label_task_query(
            project_id=project_id,
            filter=filter
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result

    def submit_label(
        self,
        project_id: str,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if filter is None:
            filter = SearchFilter()
        filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        QUERY_ID = 'submitLabelTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_submit_label_task_query(
            project_id=project_id,
            filter=filter,
        )
        response = self.session.execute(query, values)
        result = self.session.extract_task(response, QUERY_ID)
        return result

    def skip_label(
        self,
        project_id: str,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if filter is None:
            filter = SearchFilter()
        filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        QUERY_ID = 'skipLabelTask'
        self.query.query_id = QUERY_ID

        query, values = self.query.build_skip_label_task_query(
            project_id=project_id,
            filter=filter,
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