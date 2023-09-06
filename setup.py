import io
from setuptools import setup, find_packages


# Read in the README for the long description on PyPI
def long_description():
    with io.open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
    return readme

def load_config():
    with io.open("spb/sdk_config.py") as fid:
        result = {}
        for line in fid:
            try:
                line.index("End of read")
            except:
                splitted_line = line.strip().split("=")
                result[splitted_line[0]] = splitted_line[-1][1:-1]
            else:
                return result

configs = load_config()
setup(
    name=configs.get("SDK_NAME", ""),
    version=configs.get("SDK_VERSION", ""),
    url=configs.get("SDK_URL", ""),
    license=configs.get("SDK_LICENSE", ""),
    author=configs.get("SDK_AUTHOR", ""),
    author_email=configs.get("SDK_AUTHOR_EMAIL", ""),
    description=configs.get("SDK_DESCRIPTION", ""),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["spb=spb.__main__:cli"]},
    long_description=long_description(),
    long_description_content_type="text/markdown",
    install_requires=[
        "certifi==2020.4.5.2",
        "chardet>=3.0.2,<3.1.0",
        "click>=7.1.2",
        "colorama==0.4.3",
        "commonmark==0.9.1",
        "idna==2.9",
        "importlib-metadata<=4.5.0, >=3.6; python_version < '3.9'",
        "keyring==21.2.1",
        "packaging==20.4",
        "pkginfo==1.5.0.1",
        "pprintpp==0.4.0",
        "readme-renderer==26.0",
        "requests>=2.31.0,<3.0.0",
        "rich==10.2.2",
        "typing-extensions<4.0.0,>=3.7.4",
        "six==1.15.0",
        "tqdm==4.46.1",
        "botocore>=1.20.82",
        "boto3>=1.17.82",
        "natsort>=7.1.0",
        "semver==2.13.0",
    ],
    zip_safe=False,
    dependency_links=[],
)
