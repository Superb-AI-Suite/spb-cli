from spb.exceptions import SDKException
from spb.libs.phy_credit.phy_credit.imageV2 import build_label_info


class LabelInfoBuildParams:
    def __init__(self, **kwargs):
        self._result = kwargs['result'] if 'result' in kwargs else None
        self._label_interface = kwargs['label_interface'] if 'label_interface' in kwargs else None
        self.init_label_info()

    def init_label_info(self):
        if self._label_interface is not None:
            self._label_info = build_label_info(label_interface = self._label_interface, result=self._result)
        else:
            self._label_info = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result
        self.init_label_info()

    @property
    def label_interface(self):
        return self._label_interface

    @label_interface.setter
    def label_interface(self, label_interface):
        self._label_interface = label_interface

    def get_objects(self):
        return self._label_info.get_objects()

    def get_categories(self):
        return self._label_info.get_categories()

    def init_objects(self):
        if self._label_info is not None:
            self._label_info.init_objects()

    def add_object(self, class_name, annotation, properties=None, id=None):
        if self._label_info is not None:
            self._label_info.add_object(class_name=class_name, annotation=annotation, properties=properties, id=id)

    def set_categories(self, properties=None):
        if self._label_info is not None:
            self._label_info.set_categories(properties=properties)

    def build_info(self):
        if self._label_info is None:
            raise SDKException('[LabelInfoBuildParam] init_label_info definition must be called before executing')

        return self._label_info.build_info()