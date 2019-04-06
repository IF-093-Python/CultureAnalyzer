from fabric import Connection
from fabric import task
from os import environ as env


def echo_info(text, with_line=True):
    line = '-' * 100 if with_line else ''
    text = text + '\n' if text.startswith('$') else text
    return f'echo -e "{line}\n{text}"'


def command(text):
    return echo_info(f'$ {text}') + '&&' + text


DEV_DEPLOY_COMMANDS = (echo_info('Deploy...'),
                       command('cd CultureAnalyzer-8080'),
                       command('git checkout -f dev'),
                       command('git pull'),
                       command('docker-compose stop'),
                       command('docker-compose up --build -d'),
                       command('docker-compose ps'))

USER = env['GC_DEPLOY_USERNAME']
HOST = env['GC_DEPLOY_HOSTNAME']
PORT = env['GC_DEPLOY_PORT']
KEY_FILE = env['GC_DEPLOY_KEY_FILENAME']


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
