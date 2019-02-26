import os
from fabric import task
from paramiko import SSHClient, AutoAddPolicy

env = os.environ


@task
def deploy(ctx):
    print('-> Run fab deploy <-')
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.load_system_host_keys()
    ssh_client.connect(username=env['DEPLOY_USERNAME'],
                       hostname=env['DEPLOY_HOSTNAME'],
                       port=env['DEPLOY_PORT'],
                       key_filename=env['DEPLOY_KEY_FILENAME'])
    stdout, stderr = ssh_client.exec_command(env['DEPLOY_COMMAND'])[1:]
    print(get_output(stderr, stdout))
    ssh_client.close()
    print('-> End deploy <-')


def get_output(stderr, stdout):
    out = stdout.read().decode("utf8")
    err = stderr.read().decode("utf8")
    return f'\nout: \n{out}\n\nerr: \n{err}'
