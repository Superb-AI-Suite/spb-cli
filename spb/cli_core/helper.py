import os
import configparser
import rich
import rich.table
import rich.console

from spb.cli_core.commands.project import Project
from spb.cli_core.commands.label_data import LabelData
from spb.cli_core.utils import get_project_config
console = rich.console.Console()

class Helper:
    project = Project()
    label_data = LabelData()

    def set_config(self, profile_name, account_name, access_key):
        credential_path = os.path.expanduser('~') + '/.spb/config'
        credential_path = credential_path.replace(os.sep, '/')

        os.makedirs('/'.join(credential_path.split(os.sep)[:-1]), exist_ok=True)

        config_parser = configparser.ConfigParser()
        config_parser.read(credential_path)
        config_parser[profile_name] = {
            'account_name': account_name,
            'access_key': access_key,
        }

        with open(credential_path, 'w') as f:
            config_parser.write(f)

        console.print(f"Profile [b blue]{profile_name}[/b blue] is counfigured with account name '{account_name}'.")

    def list_config(self, profile_name):
        credential_path = os.path.expanduser('~') + '/.spb/config'
        credential_path = credential_path.replace(os.sep, '/')

        with open(credential_path, 'r') as f:
            print(f.read())

    def init_project(self, directory_path, project):
        return self.project.init_project(directory_path, project)

    def describe_projects(self):
        self.project.describe_projects()

    def upload(self, dataset_name, project, directory_path, include_label):
        return self.label_data.upload_data(project, dataset_name, directory_path, include_label)

    def upload_label(self, project, dataset_name, directory_path):
        return self.label_data.upload_label(project, dataset_name, directory_path)

    def download(self, project, directory_path):
        return self.label_data.download(project, directory_path)

    def check_project(self, project_name):
        return self.project.check_project(project_name)

    def _get_workspace_conf(self):
        workspace_conf_path = '.workspace'
        if os.path.isfile(workspace_conf_path):
            try:
                f = open(f"{workspace_conf_path}", 'r')
                return get_project_config(f.readline())
            except:
                console.print(f"Error while reading workspace configuration. Try again")
                return None
        else:
            console.print(f"Workspace is not initiated. 'spb init' first.")
            return None