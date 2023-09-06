import re
import uuid
from urllib.parse import quote

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from datetime import datetime, timezone
from spb.projects.project import Project
from spb.exceptions import ParameterException


class Status(Enum):
    WORKING = "WORKING"
    SUBMITTED = "SUBMITTED"
    SKIPPED = "SKIPPED"


class ReviewStatus(Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"


@dataclass(unsafe_hash=True)
class SearchFilter:

    def __init__(self, project: Optional[Project] = None):
        self.project = project

    # Label Status Filter
    status_is_any_one_of: Optional[List[Status]] = None

    # Label Review Filter
    review_is_any_one_of: Optional[List[ReviewStatus]] = None
    review_exists: Optional[bool] = None

    # Assignee Filter
    assignee_does_not_exists: Optional[bool] = None
    assignee_is_any_one_of: Optional[List[str]] = None
    assignee_none_of: Optional[List[str]] = None

    # Reviewer Filter
    reviewer_is_any_one_of: Optional[List[str]] = None
    reviewer_none_of: Optional[List[str]] = None
    reviewer_exists: Optional[bool] = None

    # Tag filter
    tag_name_all: Optional[List[str]] = None
    tag_contains_all_of: Optional[List[str]] = None
    tag_contains_any_one_of: Optional[List[str]] = None
    tag_contains_only: Optional[List[str]] = None
    tag_contains_none_of: Optional[List[str]] = None
    tag_is_empty: Optional[bool] = None

    # Dataset filter
    dataset_is_any_one_of: Optional[List[str]] = None

    # Data key filter
    data_key_contains: Optional[str] = None
    data_key_matches: Optional[str] = None
    data_key_starts_with: Optional[str] = None
    data_key_ends_with: Optional[str] = None

    # Data added filter
    data_added_at_lte: Optional[datetime] = None
    data_added_at_gte: Optional[datetime] = None

    # Last labeled at filter
    last_labeled_at_lte: Optional[datetime] = None
    last_labeled_at_gte: Optional[datetime] = None

    def to_filter_string(self):
        filters = self.generate_filter_list()
        search_string = []
        for filter in filters:
            [key, value] = filter.split("=")
            search_string.append(f"{quote(key)}={quote(value)}")
        return "&".join(search_string)

    def to_task_filter_string(self):
        filters = self.generate_filter_list()
        return "&".join(filters)

    def generate_filter_list(self):
        is_consensus_project = self.project.settings.get("allow_advanced_qa", False) if self.project is not None else False
        self.validate_options()

        filters = []
        if self.status_is_any_one_of is not None:
            filters += [f"status_in[]={s}" for s in self.status_is_any_one_of]
        if self.review_is_any_one_of is not None:
            filters += [f"review_in[]={s}" for s in self.review_is_any_one_of]
        if self.review_exists is not None:
            if is_consensus_project:
                filters += ["is_unreviewed=true"] if not self.review_exists else []
            else:
                filters += ["review_exists=true"] if not self.review_exists else []
        if self.assignee_does_not_exists is not None:
            if is_consensus_project:
                filters += ["is_unassigned=true"] if self.assignee_does_not_exists else []
            else:
                filters += ["work_assignee_exists=true"] if self.assignee_does_not_exists else []
        if self.assignee_is_any_one_of is not None:
            filters += [f"work_assignee_in[]={s}" for s in self.assignee_is_any_one_of]
        if self.assignee_none_of is not None:
            filters += [f"work_assignee_none_of[]={s}" for s in self.assignee_none_of]
        if self.reviewer_is_any_one_of is not None:
            filters += [f"reviewer_in[]={s}" for s in self.reviewer_is_any_one_of]
        if self.reviewer_none_of is not None:
            filters += [f"reviewer_none_of[]={s}" for s in self.reviewer_none_of]
        if self.reviewer_exists is not None:
            if is_consensus_project:
                filters += ["is_reviewer_unassigned=true"] if not self.reviewer_exists else []
            else:
                filters += ["reviewer_exists=true"] if not self.reviewer_exists else []
        if self.tag_name_all is not None:
            filters += [f"tags_name_all[]={s}" for s in self.tag_name_all]
        if self.tag_contains_all_of is not None:
            if is_consensus_project:
                filters += [f"tags_all[]={s}" for s in self.tag_contains_all_of]
            else:
                filters += [f"tag_all[]={s}" for s in self.tag_contains_all_of]
        if self.tag_contains_any_one_of is not None:
            if is_consensus_project:
                filters += [f"tags_any[]={s}" for s in self.tag_contains_any_one_of]
            else:
                filters += [f"tag_any[]={s}" for s in self.tag_contains_any_one_of]  
        if self.tag_contains_only is not None:
            if is_consensus_project:
                filters += [f"tags_only[]={s}" for s in self.tag_contains_only]
            else:
                filters += [f"tag_only[]={s}" for s in self.tag_contains_only]
        if self.tag_contains_none_of is not None:
            if is_consensus_project:
                filters += [f"tags_not_any[]={s}" for s in self.tag_contains_none_of]
            else:
                filters += [f"tag_none_of[]={s}" for s in self.tag_contains_none_of]
        if self.tag_is_empty is not None:
            if is_consensus_project:
                filters += [f"tags_exist={'true' if self.tag_is_empty else 'false'}"]
            else:
                filters += [f"tag_exist={'true' if self.tag_is_empty else 'false'}"]
        if self.dataset_is_any_one_of is not None:
            filters += [f"asset_group_in[]={s}" for s in self.dataset_is_any_one_of]
        if self.data_key_contains is not None:
            if is_consensus_project:
                filters += [f"asset_key_icontains={self.data_key_contains}"]
            else:
                filters += [f"asset_key_wildcard=*{self.data_key_contains}*"]
        if self.data_key_matches is not None:
            if is_consensus_project:
                raise ParameterException("[ERROR] Allow advanced QA project does not support [data_key_matches] filter")
            else:
                filters += [f"asset_key_wildcard={self.data_key_matches}"]
        if self.data_key_starts_with is not None:
            if is_consensus_project:
                raise ParameterException("[ERROR] Allow advanced QA project does not support [data_key_starts_with] filter")
            else:
                filters += [f"asset_key_wildcard={self.data_key_starts_with}*"]
        if self.data_key_ends_with is not None:
            if is_consensus_project:
                raise ParameterException("[ERROR] Allow advanced QA project does not support [data_key_ends_with] filter")
            else:
                filters += [f"asset_key_wildcard=*{self.data_key_ends_with}"]
        if self.data_added_at_lte is not None:
            filters += [f"created_at_lte={self.data_added_at_lte.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}"]
        if self.data_added_at_gte is not None:
            filters += [f"created_at_gte={self.data_added_at_gte.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}"]
        if self.last_labeled_at_lte is not None:
            filters += [f"last_labeled_at_lte={self.last_labeled_at_lte.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}"]
        if self.last_labeled_at_gte is not None:
            filters += [f"last_labeled_at_gte={self.last_labeled_at_gte.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}"]
        return filters

    def validate_options(self):
        if self.tag_contains_all_of is not None:
            for tag in self.tag_contains_all_of:
                if not uuid_validator(uuid_string=tag):
                    raise ParameterException("[ERROR] The [tag_contains_all_of] should be composed of a list of UUIDs.")
        if self.tag_contains_any_one_of is not None:
            for tag in self.tag_contains_any_one_of:
                if not uuid_validator(uuid_string=tag):
                    raise ParameterException("[ERROR] The [tag_contains_any_one_of] should be composed of a list of UUIDs.")
        if self.tag_contains_only is not None:
            for tag in self.tag_contains_only:
                if not uuid_validator(uuid_string=tag):
                    raise ParameterException("[ERROR] The [tag_contains_only] should be composed of a list of UUIDs.")
        if self.tag_contains_none_of is not None:
            for tag in self.tag_contains_none_of:
                if not uuid_validator(uuid_string=tag):
                    raise ParameterException("[ERROR] The [tag_contains_none_of] should be composed of a list of UUIDs.")

        if self.data_added_at_lte is not None and not isinstance(self.data_added_at_lte, datetime):
            raise ParameterException("[ERROR] The [data_added_at_lte] must be datetime object")
        if self.data_added_at_gte is not None and not isinstance(self.data_added_at_gte, datetime):
            raise ParameterException("[ERROR] The [data_added_at_gte] must be datetime object")
        if self.last_labeled_at_lte is not None and not isinstance(self.last_labeled_at_lte, datetime):
            raise ParameterException("[ERROR] The [last_labeled_at_lte] must be datetime object")
        if self.last_labeled_at_gte is not None and not isinstance(self.last_labeled_at_gte, datetime):
            raise ParameterException("[ERROR] The [last_labeled_at_gte] must be datetime object")

        if self.status_is_any_one_of is not None:
            for status in self.status_is_any_one_of:
                status = status.value if isinstance(status, Status) else status
                if status not in [e.value for e in Status]:
                    raise ParameterException(f"[ERROR] The [status_is_any_one_of] must be in {[e.value for e in Status]}")

        if self.review_is_any_one_of is not None:
            for status in self.review_is_any_one_of:
                status = status.value if isinstance(status, ReviewStatus) else status
                if status not in [e.value for e in ReviewStatus]:
                    raise ParameterException(f"[ERROR] The [review_is_any_one_of] must be in {[e.value for e in ReviewStatus]}")

        if self.assignee_is_any_one_of is not None:
            try:
                email_validator(emails=self.assignee_is_any_one_of)
            except ParameterException:
                raise ParameterException("[ERROR] Email format error. [assignee_is_any_one_of] needs to be email list")

        if self.assignee_none_of is not None:
            try:
                email_validator(emails=self.assignee_none_of)
            except ParameterException:
                raise ParameterException("[ERROR] Email format error. [assignee_none_of] needs to be email list")

        if self.reviewer_is_any_one_of is not None:
            try:
                email_validator(emails=self.reviewer_is_any_one_of)
            except ParameterException:
                raise ParameterException("[ERROR] Email format error. [reviewer_is_any_one_of] needs to be email list")

        if self.reviewer_none_of is not None:
            try:
                email_validator(emails=self.reviewer_none_of)
            except ParameterException:
                raise ParameterException("[ERROR] Email format error. [reviewer_none_of] needs to be email list")

        asset_key_filter_usage_count = sum(var is not None for var in [
            self.data_key_contains,
            self.data_key_matches,
            self.data_key_starts_with,
            self.data_key_ends_with])
        if asset_key_filter_usage_count > 1:
            raise ParameterException("[ERROR] [data_key_contains, data_key_matches, data_key_starts_with, data_key_ends_with] cannot be used together.")


def email_validator(*, emails: List[str]):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    for email in emails:
        if not re.match(pattern, email):
            raise ParameterException("")


def uuid_validator(*, uuid_string: str):
    try:
        _ = uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False
