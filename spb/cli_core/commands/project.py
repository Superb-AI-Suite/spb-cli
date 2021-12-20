import os
import click
import rich
import math
import rich.table
import rich.console

from spb.projects import Project
from spb.projects.manager import ProjectManager
from spb.exceptions import ParameterException

console = rich.console.Console()

class Project():
    CURRENT_PAGE_COUNT = 10
    def describe_projects(self, show_options = 'default'):

        supported_options = ['default', 'reviews']
        if show_options not in supported_options:
            raise ParameterException(f'{show_options} is not supported.')
        page = 1
        while True:
            projects, project_count = self._get_projects(page=page, page_size=self.CURRENT_PAGE_COUNT)
            table = rich.table.Table(show_header=True, header_style="bold magenta")
            table.add_column("NAME", width=50)
            table.add_column("LABELS", justify="right")

            if show_options == 'default':
                self.print_default_option_projects(projects=projects, table=table)
            elif show_options == 'reviews':
                self.print_review_option_projects(projects=projects, table=table)

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

    def print_default_option_projects(self, projects, table):
        table.add_column("IN PROGRESS", justify="right")
        table.add_column("SUBMITTED", justify="right")
        table.add_column("SKIPPED", justify="right")

        for project in projects:
            in_progress_ratio = math.ceil( project.in_progress_label_count / project.label_count * 100 ) if project.label_count > 0 else 0
            skipped_ratio = math.ceil( project.skipped_label_count / project.label_count * 100 ) if project.label_count > 0 else 0
            table.add_row(
                project.name,
                f"{project.label_count}",
                f"{project.in_progress_label_count} ({in_progress_ratio} %)",
                f"{project.submitted_label_count} ({project.progress} %)",
                f"{project.skipped_label_count} ({skipped_ratio} %)"
            )

    def print_review_option_projects(self, projects, table):
        table.add_column("IN PROGRESS\nRejected")
        table.add_column("IN PROGRESS\nNot Submitted")
        table.add_column("SUBMITTED\nApproved")
        table.add_column("SUBMITTED\nPending Review")
        table.add_column("SKIPPED\nApproved")
        table.add_column("SKIPPED\nPending Review")

        for project in projects:
            stats = project.stats if project.stats is not None else []

            in_progress_count = ([item for item in stats if item['type'] == 'IN_PROGRESS_COUNT'][0:1] or [{}])[0].get('info', {})
            submitted_count = ([item for item in stats if item['type'] == 'SUBMITTED_COUNT'][0:1] or [{}])[0].get('info', {})
            skipped_count = ([item for item in stats if item['type'] == 'SKIPPED_COUNT'][0:1] or [{}])[0].get('info', {})

            table.add_row(
                project.name,
                f'{project.label_count}',
                f'{in_progress_count.get("rejected", 0)}',
                f'{in_progress_count.get("not_submitted", 0)}',
                f'{submitted_count.get("approved", 0)}',
                f'{submitted_count.get("pending_review", 0)}',
                f'{skipped_count.get("approved", 0)}',
                f'{skipped_count.get("pending_review", 0)}'
            )

    def check_project(self, project_name):
        projects, _ = self._get_projects(name=project_name)
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
        manager = ProjectManager()
        if name is None:
            count, projects = manager.get_project_list(page = page, page_size = page_size)
            return projects, count
        else:
            project = manager.get_project(name=name)
            return [project], 1
