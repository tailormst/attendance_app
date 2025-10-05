from django.core.management.base import BaseCommand
from attendance.models import Attendance, Employee


class Command(BaseCommand):
    help = 'Delete all employees and their attendance records'

    def add_arguments(self, parser):
        parser.add_argument('--yes', action='store_true', help='Confirm deletion without prompt')

    def handle(self, *args, **options):
        confirm = options['yes']
        if not confirm:
            self.stdout.write(self.style.WARNING('This will delete ALL employees and attendance.'))
            self.stdout.write(self.style.WARNING('Run with --yes to confirm.'))
            return

        Attendance.objects.all().delete()
        Employee.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All employees and attendance records have been deleted.'))


