import os
import click
import rich
import math
import rich.table
import rich.console

import spb
from spb.cli_core.utils import get_project_config

console = rich.console.Console()

class Project():
    CURRENT_PAGE_COUNT = 10
    def describe_projects(self):
        page = 1
        while True:
            projects, project_count = self._get_projects(page=page, page_size=self.CURRENT_PAGE_COUNT)
            table = rich.table.Table(show_header=True, header_style="bold magenta")
            table.add_column("NAME", width=50)
            table.add_column("LABELS", justify="right")
            table.add_column("PROGRESS", justify="right")

            for item in projects:
                table.add_row(item.name, f"{item.label_count}", f"{item.progress}%")

            console.print(table)
            total_page = math.ceil(project_count/self.CURRENT_PAGE_COUNT)

            if total_page > page:
                click.echo(f'Press any button to continue to the next page ({page}/{total_page}). Otherwise press ‘Q’ to quit.', nl=False)
                key = click.getchar()
                click.echo()
                page = page + 1
                if key=='q' or key=='Q':
                    return
            elif total_page <= page:
                return


    def check_project(self, project_name):
        projects = self._get_projects(name=project_name)
        return projects[0] if projects and projects[0] else None

    def init_project(self, directory_path, project):
        if os.path.isdir(directory_path):
            console.print(f"Error whilte initiating project. directory already exists. Try again")
            return
        os.mkdir(directory_path)

        f = open(f"{directory_path}/.workspace", 'w')
        f.write(f"{project.name}\t{project.id}")
        f.close()
        console.print(f"Workspace '{directory_path}' for project '{project.name}' has been created.")

    def _get_projects(self, name=None, page=None, page_size=None):
        spb.client()
        command = spb.Command(type='describe_project')
        if name is not None:
            return spb.run(command=command, option={'name':name})
        else:
            return spb.run(command=command, page=page, page_size=page_size)
