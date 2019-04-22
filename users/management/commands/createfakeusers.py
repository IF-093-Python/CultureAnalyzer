from django.core.management.base import BaseCommand

from users.management.commands._fake_users import create_fake_users


class Command(BaseCommand):
    help = 'Creates fake users and stores in DB'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, nargs='?', default=10,
                            help='The number of users to be created')
        parser.add_argument('-p', '--prefix', type=str,
                            default='',
                            help='A username prefix')
        parser.add_argument('-r', '--role', type=str,
                            default='trainee',
                            help='A username prefix')

    def handle(self, *args, **options):
        number, prefix = options['number'], options['prefix']
        role = get_role_id_by_name(options['role'])
        create_fake_users(number, prefix, role)


def get_role_id_by_name(name):
    from CultureAnalyzer.constants import TRAINEE_ID, ADMIN_ID, MENTOR_ID
    name = name.lower()
    if name == 'admin':
        return ADMIN_ID
    elif name == 'mentor':
        return MENTOR_ID
    elif name == 'trainee':
        return TRAINEE_ID
    else:
        raise Exception(f'Not valid role name. Accepted names: '
                        f'[admin, mentor, trainee]')
