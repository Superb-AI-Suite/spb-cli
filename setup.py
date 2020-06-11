import io
from setuptools import setup, find_packages

from spb import __version__


# Read in the README for the long description on PyPI
def long_description():
    with io.open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
    return readme


setup(
    name="spb-cli",
    version=__version__,
    url="https://github.com/Superb-AI-Suite/cool-tree.git",
    license="MIT",
    author="Superb AI",
    author_email="support@superb-ai.com",
    description="Suite Standard Library",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["spb=spb.__main__:cli"]},
    long_description=long_description(),
    long_description_content_type="text/markdown",
    install_requires=[
        "bleach==3.1.5",
        "certifi==2020.4.5.1",
        "chardet==3.0.4",
        "click==7.1.2",
        "colorama==0.4.3",
        "commonmark==0.9.1",
        "docutils==0.16",
        "idna==2.9",
        "importlib-metadata==1.6.0; python_version < '3.8'",
        "keyring==21.2.1",
        "packaging==20.4",
        "pkginfo==1.5.0.1",
        "pprintpp==0.4.0",
        "pygments==2.6.1",
        "pyparsing==2.4.7",
        "python-datauri==0.2.8",
        "readme-renderer==26.0",
        "requests==2.23.0",
        "requests-toolbelt==0.9.1",
        "rich==1.2.3",
        "six==1.15.0",
        "stringcase==1.2.0",
        "tqdm==4.46.0",
        "twine==3.1.1",
        "typing-extensions==3.7.4.2",
        "urllib3==1.25.9",
        "webencodings==0.5.1",
        "zipp==3.1.0",
    ],
    zip_safe=False,
    dependency_links=[],
)
