import uuid

from spb.core.manager import BaseManager
from spb.projects.project import Project

from .asset import Asset
from .query import Query
from .session import Session


class AssetManager(BaseManager):
    def __init__(self, team_name=None, access_key=None):
        self.session = Session(team_name=team_name, access_key=access_key)
        self.query = Query()

    def get_asset_by_id(self, id: uuid.UUID):
        self.query.query_id = "assetV2"
        asset = Asset(id=id)
        query_attrs = asset.get_attributes_map(include=["id"])

        self.query.attrs.update(query_attrs)
        self.query.response_attrs.extend(
            asset.get_property_names(exclude=["project_id", "cursor"])
        )
        self.query.required_attrs.extend(asset.get_property_names(include=["id"]))
        query, values = self.query.build_query()
        response = self.session.execute(query, values)
        asset = self.session.get_data_from_response(response)
        return asset

    def get_assets(self, cursor: bytes = None, page_size: int = 10):
        self.query.query_id = "assetsV2"
        self.query.page_size = page_size
        init_cursor = False
        if not cursor:
            init_cursor = True
        if init_cursor:
            asset = Asset(init_cursor=init_cursor)
            query_attrs = asset.get_attributes_map(include=[])
            self.query.response_attrs.extend(
                asset.get_property_names(exclude=["cursor", "project_id"])
            )
            self.query.required_attrs.extend(asset.get_property_names(include=[]))
        else:
            asset = Asset(cursor=cursor)
            query_attrs = asset.get_attributes_map(include=["cursor"])
            self.query.response_attrs.extend(
                asset.get_property_names(exclude=["cursor", "project_id"])
            )
            self.query.required_attrs.extend(
                asset.get_property_names(include=["cursor", "project_id"])
            )
        self.query.attrs.update(query_attrs)

        if init_cursor:
            query, values = self.query.build_query(init_cursor=init_cursor)
        else:
            query, values = self.query.build_query(cursor=cursor)
        response = self.session.execute(query, values)
        (
            count,
            prev,
            nxt,
            histories,
        ) = self.session.get_cursor_based_data_from_response(response)
        return count, prev, nxt, histories

    def get_download_url(self, asset: Asset):
        query = f"query ($id:String!) {{getAssetUrl(id: $id){{presignedURL}}}}"
        values = {"id": str(asset.id)}
        response = self.session.execute(query, values)
        url = self.session.get_url_from_response(response)
        return url

    def assign_asset(self, asset: Asset, project: Project):
        self.query.query_id = "assignAsset"
        asset.project_id = project.id
        query_attrs = asset.get_attributes_map(include=["id", "project_id"])
        self.query.attrs.update(query_attrs)
        self.query.required_attrs.extend(
            asset.get_property_names(include=["id", "project_id"])
        )
        self.query.response_attrs.extend(
            asset.get_property_names(
                exclude=[
                    "id",
                    "cursor",
                    "project_id",
                    "data_key",
                    "dataset",
                    "projects",
                ]
            )
        )

        query, values = self.query.build_mutation_query()
        response = self.session.execute(query, values)
        result = self.session.get_assign_result_from_response(response)
        return result
