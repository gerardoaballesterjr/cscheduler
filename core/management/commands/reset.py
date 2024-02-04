from django.core.management import call_command
from django.core.management.base import BaseCommand
from core.models import Day, User
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        # clean
        os.system('pyclean .')
        
        # remove migrations
        try:
            migrations_dir = 'core/migrations'
            for file in os.listdir(migrations_dir):
                if file != '__init__.py':
                    os.remove(os.path.join(migrations_dir, file))
        except:
            pass
        
        # remove migrations
        try:
            os.remove('main.db')
        except:
            pass
        
        call_command('makemigrations')
        call_command('migrate')

        # create superuser
        superuser =  User()
        superuser.first_name = 'John'
        superuser.last_name = 'Doe'
        superuser.username = 'admin'
        superuser.set_password('admin')
        superuser.is_superuser = True
        superuser.save()

        # create days
        [Day(name=day).save() for day in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']]

        # clean
        os.system('pyclean .')