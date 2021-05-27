import re, ast
from setuptools import setup, find_packages


def version(name):
    _re = re.compile(r'__version__\s+=\s+(.*)')
    with open(f'{name}/__init__.py', 'rb') as f:
        return str(ast.literal_eval(_re.search(f.read().decode('utf-8')).group(1)))


setup(
    name='phy_credit',
    version=version('phy_credit'),
    packages=find_packages(),
    install_requires=[
        'semver>=2.13.0',
    ],
)
