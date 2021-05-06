from spb.exceptions import SDKException
from spb.libs.phy_credit.phy_credit.imageV2 import LabelInfo


class LabelInfoBuildParams:
    def __init__(self, **kwargs):
        self._result = kwargs['result'] if 'result' in kwargs else None
        self._label_interface = kwargs['label_interface'] if 'label_interface' in kwargs else None
        self._labels = kwargs['labels'] if 'labels' in kwargs else None
        self.init_label_info()

    def init_label_info(self):
        if self._label_interface is not None:
            self.__label_info = LabelInfo(label_interface = self._label_interface, result=self._result)
        else:
            self.__label_info = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result

    @property
    def label_interface(self):
        return self._label_interface

    @label_interface.setter
    def label_interface(self, label_interface):
        self._label_interface = label_interface

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels: list):
        self._labels = labels

    def get_objects(self):
        return self.__label_info.get_objects()

    def get_categories(self):
        return self.__label_info.get_categories()

    def add_object(self, class_name, annotation, properties=None, id=None):
        if self.__label_info is not None:
            self.__label_info.add_object(class_name=class_name, annotation=annotation, properties=properties, id=id)

    def set_categories(self, frames=None, properties=None):
        if self.__label_info is not None:
            self.__label_info.set_categories(frames=frames, properties=properties)

    def build_info(self):
        if self.__label_info is None:
            raise SDKException('[LabelInfoBuildParam] init_label_info definition must be called before executing')

        return self.__label_info.build_info()