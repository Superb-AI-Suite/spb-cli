import os
import configparser
import rich
import rich.table
import rich.console

from spb.cli_core.commands.project import Project
from spb.cli_core.commands.label_data import LabelData
from spb.cli_core.commands.video_label_data import VideoLabelData
from spb.cli_core.utils import get_project_config
console = rich.console.Console()

class Helper:
    project = Project()
    label_data = LabelData()
    video_label_data = VideoLabelData()

    def init_project(self, directory_path, project):
        return self.project.init_project(directory_path, project)

    def describe_projects(self):
        self.project.describe_projects()

    def upload(self, dataset_name, project, directory_path, include_label, is_forced):
        return self.label_data.upload_data(project, dataset_name, directory_path, include_label, is_forced)
    
    def upload_video(self, dataset_name, project, directory_path, include_label, is_forced):
        return self.video_label_data.upload_data(project, dataset_name, directory_path, include_label, is_forced)

    def upload_label(self, project, dataset_name, directory_path, is_forced):
        return self.label_data.upload_label(project, dataset_name, directory_path, is_forced)

    def upload_video_label(self, project, dataset_name, directory_path, is_forced):
        return self.video_label_data.upload_label(project, dataset_name, directory_path, is_forced)

    def download(self, project, directory_path, is_forced):
        return self.label_data.download(project, directory_path, is_forced)
    
    def download_video(self, project, directory_path, is_forced):
        return self.video_label_data.download(project, directory_path, is_forced)

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