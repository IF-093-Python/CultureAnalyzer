from fabric import task
from paramiko import SSHClient


@task
def deploy(ctx):
    print('Running...')
