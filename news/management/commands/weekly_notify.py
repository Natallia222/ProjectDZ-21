from django.core.management.base import BaseCommand
from news.scheduler import my_job


class Command(BaseCommand):
    help = 'Send weekly email notifications to category subscribers'

    def handle(self, *args, **kwargs):
        my_job()
        self.stdout.write(self.style.SUCCESS('Weekly notifications sent successfully!'))
