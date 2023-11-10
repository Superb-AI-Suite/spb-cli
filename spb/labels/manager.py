import json
import logging
import uuid
from typing import Optional, Union, List

import requests
from spb.core.manager import BaseManager
from spb.exceptions import APIException, ParameterException, NotSupportedException
from spb.labels.serializer import LabelInfoBuildParams
from spb.utils.utils import requests_retry_session
from spb.utils.search_filter import SearchFilter
from spb.projects.project import Project
from spb.users.user import User

from .label import Label, WorkappType, Tags
from .query import Query
from .session import Session

logger = logging.getLogger()


class LabelManager(BaseManager):
    def __init__(self, team_name=None, access_key=None):
        self.session = Session(team_name=team_name, access_key=access_key)
        self.query = Query()

    def get_labels_count(
        self,
        project_id: uuid.UUID,
        dataset=None,
        data_key=None,
        tags: list = [],
        label_type=None,
    ):
        self.query.query_id = "labels"
        label = Label(
            project_id=project_id,
            dataset=dataset,
            data_key=data_key,
            tags=tags,
            label_type=label_type,
        )
        query_attrs = label.get_attributes_map(include=["project_id"])
        if dataset is not None:
            query_attrs[Label.dataset] = label.dataset
        if data_key is not None:
            query_attrs[Label.data_key] = label.data_key
        if len(tags) != 0:
            query_attrs[Label.tags] = label.tags
        if label_type is not None:
            query_attrs[Label.label_type] = label_type

        self.query.attrs.update(query_attrs)
        self.query.page = 1
        self.query.page_size = 1

        self.query.response_attrs.extend(
            label.get_property_names(include=["id", "project_id"])
        )
        self.query.required_attrs.extend(
            label.get_property_names(include=["project_id"])
        )
        try:
            query, values = self.query.build_label_count_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e

        return response.json()["data"].get("labels", {"count": None})["count"]

    def search_labels_count(
        self,
        project: Project,
        filter: Optional[SearchFilter] = None,
    ):
        count, _, _ = self.search_label_ids(
            project=project,
            filter=filter,
            page_size=1
        )
        return count

    def search_labels(
        self,
        project: Project,
        filter: Optional[SearchFilter] = None,
        cursor: Optional[str] = None,
        page_size: int = 10,
    ):
        if project.settings.get("allow_advanced_qa", False):
            raise ParameterException("[ERROR] search_labels function does not support Allow Advanced QA project.")
        if page_size > 10:
            raise ParameterException("[ERROR] The page_size must be less than 11")

        QUERY_ID = "labelsSearch"
        query_string, search_params = self.query.build_search_labels_query(
            query_id=QUERY_ID,
            project_id=project.id,
            response_attrs=Label().get_property_names(),
            filter=filter,
            cursor=cursor,
            page_size=page_size
        )

        response = self.session.execute(query_string, search_params)
        count, data, next_cursor = self.session.get_count_cursor_data_from_response(QUERY_ID, response)
        labels = []
        for item in data:
            label = Label(**item)
            label = self.session.get_label_info_from_url(label)
            labels.append(label)
        return count, labels, next_cursor

    def search_label_ids(
        self,
        project: Project,
        filter: Optional[SearchFilter] = None,
        cursor: Optional[str] = None,
        page_size: int = 10,
    ):
        if project.settings.get("allow_advanced_qa", False):
            raise ParameterException("[ERROR] search_labels function does not support Allow Advanced QA project.")
        if page_size > 500:
            raise ParameterException("[ERROR] The page_size must be less than 501")

        QUERY_ID = "labelIDSearch"
        query_string, search_params = self.query.build_search_labels_query(
            query_id=QUERY_ID,
            project_id=project.id,
            response_attrs=['id'],
            filter=filter,
            cursor=cursor,
            page_size=page_size
        )

        response = self.session.execute(query_string, search_params)
        count, data, next_cursor = self.session.get_count_cursor_data_from_response(QUERY_ID, response)
        labels = []
        for item in data:
            label = Label(**item)
            labels.append(label)
        return count, labels, next_cursor

    def get_labels(
        self,
        project_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
        dataset=None,
        data_key=None,
        tags: list = [],
        label_type=None,
    ):
        self.query.query_id = "labels"
        label = Label(
            project_id=project_id,
            dataset=dataset,
            data_key=data_key,
            tags=tags,
            label_type=label_type,
        )
        query_attrs = label.get_attributes_map(include=["project_id"])

        if dataset is not None:
            query_attrs[Label.dataset] = dataset
        if data_key is not None:
            query_attrs[Label.data_key] = data_key
        if len(tags) != 0:
            query_attrs[Label.tags] = tags
        if label_type is not None:
            query_attrs[Label.label_type] = label_type

        self.query.attrs.update(query_attrs)
        self.query.page = page
        self.query.page_size = page_size

        self.query.response_attrs.extend(label.get_property_names())
        self.query.required_attrs.extend(
            label.get_property_names(include=["project_id"])
        )
        query, values = self.query.build_query()
        response = self.session.execute(query, values)

        count, data = self.session.get_count_and_data_from_response(response, "labels")
        labels = []
        for item in data:
            label = Label(**item)
            label = self.session.get_label_info_from_url(label)
            labels.append(label)
        return count, labels

    def get_label(self, project_id: uuid.UUID, id: uuid.UUID):
        self.query.query_id = "labels"
        label = Label(project_id=project_id, id=id)
        self.query.attrs.update(label.get_attributes_map(include=["id", "project_id"]))
        self.query.page = 1
        self.query.page_size = 1
        self.query.required_attrs.extend(
            label.get_property_names(include=["project_id"])
        )
        self.query.response_attrs.extend(label.get_property_names())
        try:
            query, values = self.query.build_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e

        count, data = self.session.get_count_and_data_from_response(response, "labels")
        label = None
        if count > 0:
            item = data[0]
            label = Label(**item)
            label = self.session.get_label_info_from_url(label)

        return label

    def set_info_with_url(self, label_info: dict, label: Label = None):
        if label.info_write_presigned_url is None:
            return label
        with requests_retry_session() as session:
            request_result = session.put(
                label.info_write_presigned_url, data=json.dumps(label_info)
            )
            request_result.raise_for_status()

    def get_related_labels_by_label(
        self,
        project_id: uuid.UUID,
        label_id: uuid.UUID,
        page: int = 1,
        page_size: int = 10,
    ):
        self.query.query_id = "relatedLabels"
        label = Label(project_id=project_id, id=label_id)

        self.query.attrs.update(label.get_attributes_map(include=["id", "project_id"]))
        self.query.page = page
        self.query.page_size = page_size

        self.query.response_attrs.extend(label.get_property_names())
        self.query.required_attrs.extend(
            label.get_property_names(include=["project_id"])
        )
        try:
            query, values = self.query.build_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e
        count, data = self.session.get_count_and_data_from_response(
            response, "relatedLabels"
        )
        labels = []
        for item in data:
            label = Label(**item)
            label = self.session.get_label_info_from_url(label)
            labels.append(label)
        return count, labels

    def create_label(self):
        # Request export to civet
        # boto3
        pass

    def update_label(
        self, label: Label, info_build_params: LabelInfoBuildParams = None
    ):
        query_id = "updateLabels"
        self.query.query_id = query_id

        attribute_maps = label.get_attributes_map(
            include=["id", "project_id", "tags", "workapp"]
        )
        if label.workapp == WorkappType.IMAGE_SIESTA.value:
            if info_build_params is not None:
                label_info = info_build_params.build_info()
            else:
                label_info = label.result
            result = {
                "tags": label_info.get("tags")
            } if "tags" in label_info.keys() else None
            attribute_maps.update({label.get_attribute_type("result"): result})
        elif label.workapp == WorkappType.POINTCLOUDS_SIESTA.value:
            pass
        else:
            result = label.result
            attribute_maps.update({label.get_attribute_type("result"): result})
        
        self.query.attrs.update(attribute_maps)
        self.query.required_attrs.extend(
            label.get_property_names(include=["id", "project_id", "workapp"])
        )
        self.query.response_attrs.extend(label.get_property_names())
        try:
            query, values = self.query.build_mutation_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e

        data = self.session.get_data_from_mutation(response, query_id)
        updated_label = Label(**data)

        if label.workapp in [WorkappType.IMAGE_SIESTA.value]:
            label.info_write_presigned_url = updated_label.info_write_presigned_url
            self.set_info_with_url(label_info=label_info, label=label)
            updated_label.result = label_info.get("result", None)

        return updated_label

    def delete_label(self):
        pass

    def update_info(
            self,
            label: Label,
            info_build_params: LabelInfoBuildParams = None
    ):
        QUERY_ID = "updateLabelInfo"
        self.query.query_id = QUERY_ID
        self.query.response_attrs.extend(label.get_property_names())

        if label.workapp in [
            WorkappType.IMAGE_SIESTA.value,
            WorkappType.VIDEO_SIESTA.value
        ]:
            if info_build_params is not None:
                label_info = info_build_params.build_info()
            else:
                label_info = label.result
            result = {
                "tags": label_info["tags"]
            } if "tags" in label_info.keys() else None
        else:
            raise NotSupportedException(
                "This project does not support [label info update]."
            )
        try:
            query, values = self.query.build_update_info_query(
                project_id=str(label.project_id),
                id=str(label.id),
                result=result
            )
            response = self.session.execute(query, values)
            data = self.session.get_data_from_mutation(response, QUERY_ID)
            updated_label = Label(**data)
            self.set_info_with_url(
                label_info=label_info,
                label=updated_label
            )
            updated_label = self.session.get_label_info_from_url(updated_label)
        except Exception as e:
            raise e
        return updated_label

    def update_tags(self, label: Label, tags: List[Union[str, Tags]]):
        QUERY_ID = "updateLabelTags"
        self.query.query_id = QUERY_ID
        generated_tags = []
        for tag in tags:
            if isinstance(tag, str):
                generated_tags.append(Tags(name=tag))
            else:
                generated_tags.append(tag)
        self.query.response_attrs.extend(label.get_property_names())
        try:
            query, values = self.query.build_update_tags_query(
                project_id=str(label.project_id),
                id=str(label.id),
                tags=generated_tags
            )
            response = self.session.execute(query, values)
        except Exception as e:
            raise e
        return self.session.build_label_from_response(QUERY_ID, response)

    def update_status(self, label: Label, status: str):
        QUERY_ID = "updateLabelStatus"
        self.query.query_id = QUERY_ID
        if status not in ["WORKING", "SUBMITTED", "SKIPPED"]:
            raise ParameterException((
                f"The status {status} is not supported."
                " The status can only be changed to ['WORKING', 'SUBMITTED', 'SKIPPED']."
            ))
        self.query.response_attrs.extend(label.get_property_names())
        query, values = self.query.build_update_status_query(
            project_id=str(label.project_id),
            id=str(label.id),
            status=status
        )
        response = self.session.execute(
            query, values
        )
        return self.session.build_label_from_response(QUERY_ID, response)

    def update_review_status(self, label: Label, status: str):
        QUERY_ID = "updateLabelReviewStatus"
        self.query.query_id = QUERY_ID
        if status not in ["APPROVE", "REJECT"]:
            raise ParameterException((
                f"The status {status} is not supported."
                " The status can only be changed to ['APPROVE', 'REJECT']."
            ))
        self.query.response_attrs.extend(label.get_property_names())
        query, values = self.query.build_update_status_query(
            project_id=str(label.project_id),
            id=str(label.id),
            status=status
        )
        response = self.session.execute(
            query, values
        )
        return self.session.build_label_from_response(QUERY_ID, response)

    def update_assignee(
        self,
        label: Label,
        assignee: Optional[Union[User, str]] = None
    ):
        QUERY_ID = "updateLabelAssignee"
        self.query.query_id = QUERY_ID

        if isinstance(assignee, str):
            assignee = User(email=assignee)
        self.query.response_attrs.extend(label.get_property_names())
        query, values = self.query.build_update_assignee_query(
            project_id=str(label.project_id),
            id=str(label.id),
            assignee=assignee.email if assignee is not None else None
        )
        response = self.session.execute(
            query, values
        )
        return self.session.build_label_from_response(QUERY_ID, response)

    def update_reviewer(
        self,
        label: Label,
        reviewer: Optional[Union[User, str]] = None
    ):
        QUERY_ID = "updateLabelReviewer"
        self.query.query_id = QUERY_ID

        if isinstance(reviewer, str):
            reviewer = User(email=reviewer)
        self.query.response_attrs.extend(label.get_property_names())
        query, values = self.query.build_update_reviewer_query(
            project_id=str(label.project_id),
            id=str(label.id),
            reviewer=reviewer.email if reviewer is not None else None
        )
        response = self.session.execute(
            query, values
        )
        return self.session.build_label_from_response(QUERY_ID, response)
