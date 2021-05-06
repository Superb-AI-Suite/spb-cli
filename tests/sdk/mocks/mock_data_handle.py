import spb.sdk
from spb.labels import Label
from .mock_label import MOCK_LABEL
from .mock_project import MOCK_PROJECT

MOCK_DATA_HANDLE = spb.sdk.DataHandle(data = MOCK_LABEL, project = MOCK_PROJECT)

