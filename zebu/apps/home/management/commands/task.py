# app/management/commands/task.py
from django.core.management.base import NoArgsCommand

import kronos

@kronos.register('0 0 * * *')
class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        print('Hello, world!')