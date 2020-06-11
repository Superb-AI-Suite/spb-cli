import click
import rich
import rich.table
import rich.console
import os

import spb
from spb.cli_core.helper import Helper
from spb.session import Session

console = rich.console.Console()
helper = Helper()

@click.group()
@click.version_option(version=spb.__version__, message='%(version)s')
def cli():
    pass


@cli.command()
# @click.option('--profile_name', prompt='Profile Name', default='default')]
@click.option('--account_name', required=False)
@click.option('--access_key', required=False)
@click.option('-l', '--list', 'list_flag', is_flag=True)
def configure(account_name, access_key, list_flag):
    profile_name = 'default'
    if list_flag:
        helper.list_config(profile_name)
        return

    if account_name is None:
        account_name = click.prompt('Suite Account Name', type=str)
    if access_key is None:
        access_key = click.prompt('Access Key', type=str)
    helper.set_config(profile_name, account_name, access_key)

@cli.group()
def describe():
    pass

@describe.command()
def projects():
    helper.describe_projects()

@cli.group()
def upload():
    pass

@upload.command()
@click.option('--name', 'name', help='Target dataset name')
@click.option('--project', 'project_name', help='Target project name')
@click.option('--dir', 'directory_path', default='.', help='Target directory path (default=[./])')
@click.option('--include-label', 'include_label', default=False, is_flag=True, help='Upload your pre-labels to the project')
def dataset(name, project_name, directory_path, include_label):
    project = _get_project_with_name(project_name)
    if not project:
        return

    if not name:
        for _ in range(3):
            name = click.prompt('Dataset Name')
            if not name:
                click.echo('Enter dataset name. Try again.')
            else:
                break
        if not name:
            return

    helper.upload(dataset_name=name, project=project, directory_path=directory_path, include_label=include_label)

@upload.command()
@click.option('--project', 'project_name', help='Target project name')
@click.option('--name', 'dataset_name', help='Target dataset name')
@click.option('--dir', 'directory_path', default='.', help='Target directory path (default=[./])')
def labels(project_name, dataset_name, directory_path):
    project = _get_project_with_name(project_name)
    if not project:
        return
    if not dataset_name:
        for _ in range(3):
            dataset_name = click.prompt('Dataset Name')
            if not dataset_name:
                click.echo('Enter dataset name. Try again.')
            else:
                break
        if not dataset_name:
            return
    helper.upload_label(project, dataset_name, directory_path)



@cli.command()
@click.option('--dir', 'directory_path', default='.', help='Target directory path (default=[./])')
@click.option('--project', 'project_name', help='Target project name')
def download(project_name, directory_path):
    project = _get_project_with_name(project_name)
    if not project:
        return
    helper.download(project, directory_path)


@cli.command()
def version():
    click.echo(spb.__version__)

def _get_project_with_name(project_name):
    project = None
    for _ in range(3):
        if not project_name:
            project_name = click.prompt('Project Name')
        project = helper.check_project(project_name)
        if not project:
            click.echo('No such project. Try again.')
            project_name = None
        else:
            break
    return project