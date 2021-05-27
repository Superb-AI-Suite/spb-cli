import semver

from .label_info import LabelInfo
from .legacy.label_info import LabelInfo as LegacyLabelInfo


def is_camel_version(label_interface):
    return semver.compare(label_interface.get('version', '0.0.0'), '0.4.0') < 0

def build_label_info(label_interface, result=None):
    if is_camel_version(label_interface):
        return LegacyLabelInfo(label_interface, result)
    return LabelInfo(label_interface, result)


__all__ = ('LabelInfo', 'LegacyLabelInfo', 'build_label_info', 'is_camel_version')
