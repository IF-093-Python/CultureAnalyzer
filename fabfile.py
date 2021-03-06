from fabric import Connection
from fabric import task
from os import environ as env


def echo_info(text, with_line=True):
    line = '-' * 100 if with_line else ''
    text = text + ('\n' if text.startswith('$') else '')
    return f'echo -e "{line}\n{text}"'


def command(text):
    return echo_info(f'$ {text}') + '&&' + text


def open_project(folder):
    return (echo_info('Deploy running...'),
            command(f'cd {folder}'))


def update_project(branch):
    return (command(f'git checkout -f {branch}'),
            command('git pull'))


def update_docker(docker_compose_file):
    return (command('docker-compose down'),
            command(f'docker-compose -f {docker_compose_file} up -d --build'),
            command('docker-compose ps'))


MASTER_DEPLOY_COMMANDS = (
    *open_project(folder='CultureAnalyzer'),
    *update_project(branch='master'),
    *update_docker(docker_compose_file='docker-compose.prod.yml')
)

DEV_DEPLOY_COMMANDS = (
    *open_project(folder='CultureAnalyzer-8080'),
    *update_project(branch='dev'),
    *update_docker(docker_compose_file='docker-compose.dev.yml')
)

USER = env['GC_DEPLOY_USERNAME']
HOST = env['GC_DEPLOY_HOSTNAME']
PORT = env['GC_DEPLOY_PORT']
KEY_FILE = env['GC_DEPLOY_KEY_FILENAME']


@task
def gc_deploy_master(_ctx):
    deploy(username=USER, hostname=HOST, port=PORT, key_filename=KEY_FILE,
           deploy_commands=MASTER_DEPLOY_COMMANDS)


@task
def gc_deploy_dev(_ctx):
    deploy(username=USER, hostname=HOST, port=PORT, key_filename=KEY_FILE,
           deploy_commands=DEV_DEPLOY_COMMANDS)


def deploy(username, hostname, port, key_filename, deploy_commands):
    print('---> Run fab deploy <---')
    connection = Connection(host=hostname, user=username, port=port,
                            connect_kwargs={"key_filename": key_filename})
    with connection as c:
        result = c.run(' && '.join(deploy_commands))
        print(result)
    print('---> End deploy <---')
