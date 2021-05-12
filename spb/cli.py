import click
import configparser
import rich
import rich.table
import rich.console
import os

import spb
from spb.session import Session

helper = None
console = rich.console.Console()

def _initiation_cli():

    from spb.cli_core.helper import Helper

    global helper
    if helper is None:
        helper = Helper()
    spb.client()

@click.group()
@click.version_option(version=spb.__version__, message='%(version)s')
def cli():
    pass

@cli.command()
# @click.option('--profile_name', prompt='Profile Name', default='default')]
@click.option('-n', '--account_name', required=False, help="Your account name")
@click.option('-k', '--access_key', required=False, help="Your access key")
@click.option('-l', '--list', 'list_flag', is_flag=True, help="Displays all your configurations")
def configure(account_name, access_key, list_flag):
    """Config your CREDENTIALS(Profile Name, Access Key)"""
    profile_name = 'default'

    if list_flag:
        credential_path = os.path.join(os.path.expanduser('~'), '.spb', 'config')
        try:
            with open(credential_path, 'r') as f:
                print(f.read())
        except:
            console.print( "Credential is not configured. Plz, Config your credential first.")
        return

    if account_name is None:
        account_name = click.prompt('Suite Account Name', type=str)
    if access_key is None:
        access_key = click.prompt('Access Key', type=str)

    credential_path = os.path.join(os.path.expanduser('~'), '.spb', 'config')
    credential_dir = (os.sep).join(credential_path.split(os.sep)[:-1])

    os.makedirs(credential_dir, exist_ok=True)

    config_parser = configparser.ConfigParser()
    config_parser.read(credential_path)
    config_parser[profile_name] = {
        'account_name': account_name,
        'access_key': access_key,
    }

    with open(credential_path, 'w') as f:
        config_parser.write(f)

    console.print(f"Profile [b blue]{profile_name}[/b blue] is counfigured with account name '{account_name}'.")

@cli.group()
def describe():
    """Describe your RESOURCES in Suite"""
    _initiation_cli()
    spb.client()
    pass

@describe.command()
def projects():
    """Get all of your project in Suite"""
    helper.describe_projects()

@cli.group()
def upload():
    """Upload your data to Suite"""
    _initiation_cli()
    pass

@upload.command()
@click.option('-n', '--name', 'name', help='Target dataset name')
@click.option('-p', '--project', 'project_name', help='Target project name')
@click.option('-d', '--dir', 'directory_path', default='.', help='Target directory path (default=[./])')
@click.option('-l', '--include-label', 'include_label', default=False, is_flag=True, help='Upload your pre-labels to the project')
@click.option('-y', '--yes', 'is_forced', required=False, default=False, help='Say YES to all prompts', is_flag=True)
def dataset(name, project_name, directory_path, include_label, is_forced):
    """Upload images to your Suite project"""
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

    if project.workapp.startswith('video'):
        helper.upload_video(dataset_name=name, project=project, directory_path=directory_path, include_label=include_label, is_forced=is_forced)
    elif project.workapp.startswith('image'):
        helper.upload(dataset_name=name, project=project, directory_path=directory_path, include_label=include_label, is_forced=is_forced)

@upload.command()
@click.option('-p', '--project', 'project_name', help='Target project name')
@click.option('-n', '--name', 'dataset_name', help='Target dataset name')
@click.option('-d', '--dir', 'directory_path', default='.', help='Target directory path (default=[./])')
@click.option('-y', '--yes', 'is_forced', required=False, default=False, help='Say YES to all prompts', is_flag=True)
def labels(project_name, dataset_name, directory_path, is_forced):
    """Upload label json to your Suite project"""
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

    if project.workapp.startswith('video'):
        helper.upload_video_label(project, dataset_name, directory_path, is_forced=is_forced)
    elif project.workapp.startswith('image'):
        helper.upload_label(project, dataset_name, directory_path, is_forced=is_forced)

@cli.command()
@click.option('-d', '--dir', 'directory_path', default='.', help='Target directory path (default=[./])')
@click.option('-p', '--project', 'project_name', help='Target project name')
@click.option('-y', '--yes', 'is_forced', required=False, default=False, help='Say YES to all prompts', is_flag=True)
def download(project_name, directory_path, is_forced):
    """Download all data and labels of your project in Suite """
    _initiation_cli()
    project = _get_project_with_name(project_name)
    if not project:
        return

    if project.workapp.startswith('video'):
        helper.download_video(project, directory_path, is_forced=is_forced)
    elif project.workapp.startswith('image'):
        helper.download(project, directory_path, is_forced=is_forced)

@cli.command()
def version():
    click.echo(spb.sdk_config.SDK_VERSION)

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
