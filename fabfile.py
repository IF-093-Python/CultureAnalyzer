import os
from fabric import task
from paramiko import SSHClient, AutoAddPolicy

env = os.environ


@task
def deploy_aws(ctx):
    deploy(username=env['DEPLOY_USERNAME'],
           hostname=env['DEPLOY_HOSTNAME'],
           port=env['DEPLOY_PORT'],
           key_filename=env['DEPLOY_KEY_FILENAME'],
           deploy_command=env['DEPLOY_COMMAND'])


def deploy_gc(ctx):
    deploy(username=env['GC_DEPLOY_USERNAME'],
           hostname=env['GC_DEPLOY_HOSTNAME'],
           port=env['GC_DEPLOY_PORT'],
           key_filename=env['GC_DEPLOY_KEY_FILENAME'],
           deploy_command=env['GC_DEPLOY_COMMAND'])


def deploy(username, hostname, port, key_filename, deploy_command):
    print('-> Run fab deploy <-')
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.load_system_host_keys()
    ssh_client.connect(username=username, hostname=hostname,
                       port=port, key_filename=key_filename)
    stdout, stderr = ssh_client.exec_command(deploy_command)[1:]
    print(get_output(stderr, stdout))
    ssh_client.close()
    print('-> End deploy <-')


def get_output(stderr, stdout):
    out = stdout.read().decode("utf8")
    err = stderr.read().decode("utf8")
    return f'\nout: \n{out}\n\nerr: \n{err}'
