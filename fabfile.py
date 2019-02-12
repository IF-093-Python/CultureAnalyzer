import os
from fabric import task
from paramiko import SSHClient, AutoAddPolicy

env = os.environ


@task
def deploy(ctx):
    print('-> Run fab deploy <-')
    ssh_client = SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.connect(username=env['DEPLOY_USERNAME'],
                       hostname=env['DEPLOY_HOSTNAME'],
                       port=env['DEPLOY_PORT'],
                       key_filename=env['DEPLOY_KEY_FILENAME'])
    stdin, stdout, stderr = ssh_client.exec_command(env['DEPLOY_COMMAND'])
    print(get_output(stderr, stdout))
    ssh_client.close()
    print('-> End deploy <-')


def get_output(stderr, stdout):
    return 'out: ' + str(stdout.read()) + '\nerr: ' + str(stderr.read())
