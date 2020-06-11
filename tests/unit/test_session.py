import requests_mock

import spb
from spb.session import Session
from spb.models.data import Data
import pytest
from spb.models.project import Project
from spb.exceptions.exceptions import APIException

query = """
query does not matter
"""

def test_session_can_execute_create_asset_command():
    with requests_mock.Mocker() as m:
        m.post(requests_mock.ANY, json={
            "data": {
                "createAsset": {
                    "id": "929c9802-4bce-4040-acb4-d5dd398de29b",
                    "file": None,
                    "fileName": "img-4.jpg",
                    "fileSize": 26097,
                    "dataset": "12",
                    "dataKey": "img-11-28.jpg"
                }
            }
        })
        session = Session(access_key='access_key', account_name='account_name')
        res = session.execute(query)

    assert res is not None

def test_session_can_execute_describe_projects_command():
    with requests_mock.Mocker() as m:
        m.post(requests_mock.ANY, json={
            "data": {
                "projects": [
                    {
                        "id": "08f8662b-e297-4e39-b2eb-b2a12f5ed690",
                        "name": "0318 test",
                        "labelCount": 18,
                        "progress": 18,
                        "configure": "{\"dataType\":\"image\",\"objectDetection\":{\"annotationTypes\":[\"box\"],\"objectClasses\":[{\"name\":\"test\",\"color\":\"#FF625A\",\"annotationType\":\"box\"}],\"objectGroups\":[],\"keypointInterfaces\":[]},\"imageCategorization\":[]}"
                    },
                    {
                        "id": "8331c61b-ff4b-4446-8f02-a984b7ade47b",
                        "name": "a-1",
                        "labelCount": 0,
                        "progress": 18,
                        "configure": "{\"dataType\":\"image\",\"objectDetection\":{\"annotationTypes\":[\"box\",\"polyline\",\"polygon\"],\"objectClasses\":[{\"name\":\"pedestrians\",\"color\":\"#FF625A\",\"annotationType\":\"box\"},{\"name\":\"seated pedestrians\",\"color\":\"#F89400\",\"annotationType\":\"box\"},{\"name\":\"bike rider\",\"color\":\"#FFCC00\",\"annotationType\":\"box\"},{\"name\":\"motorcycle rider\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"sedan\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"van\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"box trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"bus\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"a bike without driver\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"motocycle without driver\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"tricycle\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"pickup truck\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"agitators\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"excavator\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"forklifts\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"ladder trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"other trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"other cars\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"speed limit\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"speed limit remove\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"minimum speed limit\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"minimum speed limit remove\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"no passing\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"no passing remove\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"sub-traffic sign\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"traffic light\",\"color\":\"#FFCC00\",\"annotationType\":\"box\"},{\"name\":\"traffic light lamp\",\"color\":\"#6648FF\",\"annotationType\":\"box\"},{\"name\":\"solid line\",\"color\":\"#4AE2B9\",\"annotationType\":\"polyline\"},{\"name\":\"dotted line\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"botts dots\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"other line\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"unknown road edge\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"traffic cone group\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"guardrail\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"curb\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"solid delimiter\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"vegetation\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"free space\",\"color\":\"#A6A6A6\",\"annotationType\":\"polygon\"}],\"objectGroups\":[{\"name\":\"pd\",\"objectClasses\":[\"pedestrians\",\"seated pedestrians\",\"bike rider\",\"motorcycle rider\"]},{\"name\":\"vd\",\"objectClasses\":[\"sedan\",\"van\",\"trucks\",\"box trucks\",\"bus\",\"a bike without driver\",\"motocycle without driver\",\"tricycle\",\"pickup truck\",\"agitators\",\"excavator\",\"forklifts\",\"ladder trucks\",\"other trucks\",\"other cars\"]},{\"name\":\"traffic sign\",\"objectClasses\":[\"speed limit\",\"speed limit remove\",\"minimum speed limit\",\"minimum speed limit remove\",\"no passing\",\"no passing remove\",\"sub-traffic sign\"]},{\"name\":\"traffic light\",\"objectClasses\":[\"traffic light\",\"traffic light lamp\"]},{\"name\":\"lane\",\"objectClasses\":[\"solid line\",\"dotted line\",\"botts dots\",\"other line\"]},{\"name\":\"road edge\",\"objectClasses\":[\"unknown road edge\",\"traffic cone group\",\"guardrail\",null,\"solid delimiter\",\"vegetation\"]},{\"name\":\"free space\",\"objectClasses\":[\"free space\"]}],\"keypointInterfaces\":[]},\"imageCategorization\":[]}"
                    },
                    {
                        "id": "d0607406-161b-4bed-adf9-65da917a862e",
                        "name": "a-1-test",
                        "labelCount": 2,
                        "progress": 18,
                        "configure": "{\"dataType\":\"image\",\"objectDetection\":{\"annotationTypes\":[\"box\",\"polyline\",\"polygon\"],\"objectClasses\":[{\"name\":\"pedestrians\",\"color\":\"#FF625A\",\"annotationType\":\"box\"},{\"name\":\"seated pedestrians\",\"color\":\"#F89400\",\"annotationType\":\"box\"},{\"name\":\"bike rider\",\"color\":\"#FFCC00\",\"annotationType\":\"box\"},{\"name\":\"motorcycle rider\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"sedan\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"van\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"box trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"bus\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"a bike without driver\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"motocycle without driver\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"tricycle\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"pickup truck\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"agitators\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"excavator\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"forklifts\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"ladder trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"other trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"other cars\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"speed limit\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"speed limit remove\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"minimum speed limit\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"minimum speed limit remove\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"no passing\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"no passing remove\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"sub-traffic sign\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"traffic light\",\"color\":\"#FFCC00\",\"annotationType\":\"box\"},{\"name\":\"traffic light lamp\",\"color\":\"#6648FF\",\"annotationType\":\"box\"},{\"name\":\"solid line\",\"color\":\"#4AE2B9\",\"annotationType\":\"polyline\"},{\"name\":\"dotted line\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"botts dots\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"other line\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"unknown road edge\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"traffic cone group\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"guardrail\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"curb\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"solid delimiter\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"vegetation\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"free space\",\"color\":\"#A6A6A6\",\"annotationType\":\"polygon\"}],\"objectGroups\":[{\"name\":\"pd\",\"objectClasses\":[\"pedestrians\",\"seated pedestrians\",\"bike rider\",\"motorcycle rider\"]},{\"name\":\"vd\",\"objectClasses\":[\"sedan\",\"van\",\"trucks\",\"box trucks\",\"bus\",\"a bike without driver\",\"motocycle without driver\",\"tricycle\",\"pickup truck\",\"agitators\",\"excavator\",\"forklifts\",\"ladder trucks\",\"other trucks\",\"other cars\"]},{\"name\":\"traffic sign\",\"objectClasses\":[\"speed limit\",\"speed limit remove\",\"minimum speed limit\",\"minimum speed limit remove\",\"no passing\",\"no passing remove\",\"sub-traffic sign\"]},{\"name\":\"traffic light\",\"objectClasses\":[\"traffic light\",\"traffic light lamp\"]},{\"name\":\"lane\",\"objectClasses\":[\"solid line\",\"dotted line\",\"botts dots\",\"other line\"]},{\"name\":\"road edge\",\"objectClasses\":[\"unknown road edge\",\"traffic cone group\",\"guardrail\",null,\"solid delimiter\",\"vegetation\"]},{\"name\":\"free space\",\"objectClasses\":[\"free space\"]}],\"keypointInterfaces\":[]},\"imageCategorization\":[]}"
                    },
                    {
                        "id": "b3cf1699-381d-4fd0-a6bc-65e27820ff23",
                        "name": "a-1-test2",
                        "labelCount": 1,
                        "progress": 18,
                        "configure": "{\"dataType\":\"image\",\"objectDetection\":{\"annotationTypes\":[\"box\",\"polyline\",\"polygon\"],\"objectClasses\":[{\"name\":\"pedestrians\",\"color\":\"#FF625A\",\"annotationType\":\"box\"},{\"name\":\"seated pedestrians\",\"color\":\"#F89400\",\"annotationType\":\"box\"},{\"name\":\"bike rider\",\"color\":\"#FFCC00\",\"annotationType\":\"box\"},{\"name\":\"motorcycle rider\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"sedan\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"van\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"box trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"bus\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"a bike without driver\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"motocycle without driver\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"tricycle\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"pickup truck\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"agitators\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"excavator\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"forklifts\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"ladder trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"other trucks\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"other cars\",\"color\":\"#4AE2B9\",\"annotationType\":\"box\"},{\"name\":\"speed limit\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"speed limit remove\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"minimum speed limit\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"minimum speed limit remove\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"no passing\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"no passing remove\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"sub-traffic sign\",\"color\":\"#A3EB57\",\"annotationType\":\"box\"},{\"name\":\"traffic light\",\"color\":\"#FFCC00\",\"annotationType\":\"box\"},{\"name\":\"traffic light lamp\",\"color\":\"#6648FF\",\"annotationType\":\"box\"},{\"name\":\"solid line\",\"color\":\"#4AE2B9\",\"annotationType\":\"polyline\"},{\"name\":\"dotted line\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"botts dots\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"other line\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"unknown road edge\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"traffic cone group\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"guardrail\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"curb\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"solid delimiter\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"vegetation\",\"color\":\"#A6A6A6\",\"annotationType\":\"polyline\"},{\"name\":\"free space\",\"color\":\"#A6A6A6\",\"annotationType\":\"polygon\"}],\"objectGroups\":[{\"name\":\"pd\",\"objectClasses\":[\"pedestrians\",\"seated pedestrians\",\"bike rider\",\"motorcycle rider\"]},{\"name\":\"vd\",\"objectClasses\":[\"sedan\",\"van\",\"trucks\",\"box trucks\",\"bus\",\"a bike without driver\",\"motocycle without driver\",\"tricycle\",\"pickup truck\",\"agitators\",\"excavator\",\"forklifts\",\"ladder trucks\",\"other trucks\",\"other cars\"]},{\"name\":\"traffic sign\",\"objectClasses\":[\"speed limit\",\"speed limit remove\",\"minimum speed limit\",\"minimum speed limit remove\",\"no passing\",\"no passing remove\",\"sub-traffic sign\"]},{\"name\":\"traffic light\",\"objectClasses\":[\"traffic light\",\"traffic light lamp\"]},{\"name\":\"lane\",\"objectClasses\":[\"solid line\",\"dotted line\",\"botts dots\",\"other line\"]},{\"name\":\"road edge\",\"objectClasses\":[\"unknown road edge\",\"traffic cone group\",\"guardrail\",\"curb\",\"solid delimiter\",\"vegetation\"]},{\"name\":\"free space\",\"objectClasses\":[\"free space\"]}],\"keypointInterfaces\":[]},\"imageCategorization\":[]}"
                    },
                    {
                        "id": "84ae8b66-6ef4-44a6-8e12-a360f82c331d",
                        "name": "abcd",
                        "labelCount": 0,
                        "progress": 18,
                        "configure": "{\"dataType\":\"image\",\"objectDetection\":{\"annotationTypes\":[\"box\"],\"objectClasses\":[{\"name\":\"Untitled Class\",\"color\":\"#FF625A\",\"annotationType\":\"box\"}],\"objectGroups\":[],\"keypointInterfaces\":[]},\"imageCategorization\":[]}"
                    },
                    {
                        "id": "511f49cf-9827-4017-8be4-a1c49024f221",
                        "name": "abcdeqrq",
                        "labelCount": 0,
                        "progress": 18,
                        "configure": "{\"dataType\":\"image\",\"objectDetection\":{\"annotationTypes\":[\"box\"],\"objectClasses\":[{\"name\":\"Untitled Class\",\"color\":\"#FF625A\",\"annotationType\":\"box\"}],\"objectGroups\":[],\"keypointInterfaces\":[]},\"imageCategorization\":[]}"
                    },
                    {
                        "id": "9d51cefd-c64f-4443-b173-070bc841811a",
                        "name": "asdf",
                        "labelCount": 0,
                        "progress": 18,
                        "configure": "{\"dataType\":\"image\",\"objectDetection\":{\"annotationTypes\":[\"box\"],\"objectClasses\":[{\"name\":\"aasdfds;\",\"color\":\"#FF625A\",\"annotationType\":\"box\"}],\"objectGroups\":[],\"keypointInterfaces\":[]},\"imageCategorization\":[]}"
                    },
                    {
                        "id": "908ce058-0eea-4841-ba0b-6a2a8b825caa",
                        "name": "asdfsf",
                        "labelCount": 3,
                        "progress": 18,
                        "configure": "{\"dataType\":\"image\",\"objectDetection\":{\"annotationTypes\":[\"box\"],\"objectClasses\":[{\"name\":\"Untitled Class\",\"color\":\"#FF625A\",\"annotationType\":\"box\"}],\"objectGroups\":[],\"keypointInterfaces\":[]},\"imageCategorization\":[]}"
                    },
                    {
                        "id": "4910fc5f-4889-4275-a639-d6c80208ca3c",
                        "name": "Categorization Test",
                        "labelCount": 22,
                        "progress": 18,
                        "configure": "{\"dataType\":\"image\",\"objectDetection\":{\"annotationTypes\":[\"box\",\"polyline\",\"polygon\",\"keypoint\"],\"objectClasses\":[{\"name\":\"person\",\"color\":\"#FF625A\",\"annotationType\":\"box\"},{\"name\":\"car\",\"color\":\"#F89400\",\"annotationType\":\"polyline\"},{\"name\":\"flower\",\"color\":\"#FFCC00\",\"annotationType\":\"polygon\"},{\"name\":\"face\",\"color\":\"#A3EB57\",\"annotationType\":\"keypoint\",\"keypointName\":\"face\"}],\"objectGroups\":[{\"name\":\"group 1\",\"objectClasses\":[\"person\",\"car\"]},{\"name\":\"group 2\",\"objectClasses\":[\"flower\",\"face\"]}],\"keypointInterfaces\":[{\"name\":\"face\",\"points\":[\"left eye center\",\"left eye inner corner\",\"left eye outer corner\",\"right eye center\",\"right eye inner corner\",\"right eye outer corner\",\"left eyebrow inner end\",\"left eyebrow outer end\",\"right eyebrow inner end\",\"right eyebrow outer end\",\"nose tip\",\"mouth left corner\",\"mouth right corner\",\"mouth center top lip\",\"mouth center bottom lip\"]}]},\"imageCategorization\":[{\"name\":\"Image Categorization\",\"type\":\"Multiple Selection\",\"options\":[{\"name\":\"남자\",\"children\":[{\"name\":\"상의\",\"children\":[{\"name\":\"맨투맨\"},{\"name\":\"가디건\"},{\"name\":\"니트\"},{\"name\":\"후드티\"}]},{\"name\":\"하의\",\"children\":[{\"name\":\"청바지\"},{\"name\":\"면바지\"}]}]},{\"name\":\"여자\",\"children\":[{\"name\":\"상의\",\"children\":[{\"name\":\"블라우스\"},{\"name\":\"후드티\"}]},{\"name\":\"하의\",\"children\":[{\"name\":\"레깅스\"},{\"name\":\"치마\"},{\"name\":\"청바지\"}]}]},{\"name\":\"강아지\",\"children\":[{\"name\":\"옷\",\"children\":[]},{\"name\":\"신발\",\"children\":[]}]}]}]}"
                    },
                    {
                        "id": "57bdfba4-aa6d-4d65-8e8a-fb2d4f68234e",
                        "name": "cxvav",
                        "labelCount": 0,
                        "progress": 18,
                        "configure": "{\"dataType\":\"image\",\"objectDetection\":{\"annotationTypes\":[],\"objectClasses\":[],\"objectGroups\":[],\"keypointInterfaces\":[]},\"imageCategorization\":[{\"name\":\"Image Categorization\",\"type\":\"Multiple Selection\",\"options\":[{\"name\":\"Category\",\"children\":[{\"name\":\"Category\",\"children\":[{\"name\":\"hk\"},{\"name\":\"hkl\"}]},{\"name\":\"2\"}]},{\"name\":\"Category (1)\",\"children\":[{\"name\":\"hkl\"},{\"name\":\"Category\",\"children\":[{\"name\":\"hkl\"},{\"name\":\"g\"}]},{\"name\":\"Category (1)\",\"children\":[{\"name\":\"hkl\"},{\"name\":\"yi\"}]}]},{\"name\":\"Category (2)\",\"children\":[]},{\"name\":\"1\"}]}]}"
                    }
                ]
            }
        })
        session = Session(access_key='access_key', account_name='account_name')
        res = session.execute(query)

def test_session_can_handle_exception():
    with requests_mock.Mocker() as m:
        m.post(requests_mock.ANY, json={
            "errors": [
                {
                "message": "The data key is duplicated.",
                "locations": [
                    {
                    "line": 2,
                    "column": 3
                    }
                ],
                "path": [
                    "createAsset"
                ],
                "extensions": {
                    "code": "GRAPHQL_VALIDATION_FAILED",
                    "exception": {
                    "stacktrace": [
                        "ValidationError: The data key is duplicated.",
                        "    at AssetService.upload (/Users/nicola/Workspace/superb/cool-root/.build/src/services/AssetService.js:44:23)",
                        "    at processTicksAndRejections (internal/process/task_queues.js:93:5)"
                    ]
                    }
                }
                }
            ],
            "data": None,
        })

        session = Session(access_key='access_key', account_name='account_name')


        with pytest.raises(APIException) as ei:
            session.execute(query)
        assert 'The data key is duplicated' in ei.value.message

