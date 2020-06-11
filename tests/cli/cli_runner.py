import pexpect
import contextlib
import io
import os
import pathlib
import shutil

class CLIRunnerException(Exception):
    pass

@contextlib.contextmanager
def run_cli(command):
    spb = pexpect.spawn(command)
    spb.timeout=2
    spb.setwinsize(160,400)
    spb.logfile = io.BytesIO()
    try:
        yield spb
    except pexpect.EOF:
        raise CLIRunnerException(str(spb.logfile.getvalue()))
    except pexpect.TIMEOUT:
        raise CLIRunnerException(str(spb.logfile.getvalue()))
    finally:
        spb.close()

@contextlib.contextmanager
def run_in_workspace(workspace_name='workspace', project_name='0510-holiday'):
    assert not os.path.exists(workspace_name)
    with run_cli(f'python -m spb init {workspace_name}') as spb:
        spb.expect('.*Project Name')
        spb.sendline(project_name)
        spb.expect(f"created.")
        spb.expect(pexpect.EOF)
    assert os.path.exists(workspace_name)
    assert len(os.listdir(workspace_name) ) != 0

    prevdir = os.getcwd()
    os.chdir(workspace_name)
    try:
        yield spb
    finally:
        os.chdir(prevdir)
        shutil.rmtree(workspace_name)

@contextlib.contextmanager
def run_cli_in_workspace(command, workspace_name='workspace', project_name='0510-holiday'):
    with run_in_workspace(workspace_name, project_name):
        with run_cli(command) as spb:
            yield spb
