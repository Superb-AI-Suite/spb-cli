import pytest
import spb
from spb.command import Command
from spb.models import Project

def test_describe_project():
    spb.client()
    command = Command(type='describe_project')
    projects = spb.run(command=command)

    for item in projects:
        print(item)

if __name__ == "__main__":
    test_describe_project()
