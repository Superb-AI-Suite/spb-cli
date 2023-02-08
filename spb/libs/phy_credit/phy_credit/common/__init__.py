import semver


def is_camel_version(label_interface):
    return (
        semver.VersionInfo.parse(label_interface.version).compare("0.4.0") < 0
    )


# __all__ = (
#     "CategorizationDef",
#     "PropertyDef",
#     "PropertyOptionsDef",
#     "PropertyOptionsItemDef",
# )
