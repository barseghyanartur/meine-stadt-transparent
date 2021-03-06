import datetime

from django.core.management.base import BaseCommand
from django.db.models import F

from mainapp.models import Paper, File


class Command(BaseCommand):
    help = "After the initial import, this command guesses the sort_date-Attribute of papers and files"

    def add_arguments(self, parser):
        help_str = (
            "The date of the first import in the format YYYY-MM-DD. "
            + "All documents/files created up to this day will have the sort_date-Attribute modified."
        )
        parser.add_argument("import_date", type=str, help=help_str)

        help_str = "If no date can be determined, this will be used as fallback. Should be far in the past."
        parser.add_argument("fallback_date", type=str, help=help_str)

    def handle(self, *args, **options):
        import_date = datetime.datetime.strptime(
            options["import_date"] + " 23:59:59", "%Y-%m-%d %H:%M:%S"
        )
        fallback_date = datetime.datetime.strptime(options["fallback_date"], "%Y-%m-%d")

        self.stdout.write("Fixing papers...")
        num = Paper.objects.filter(
            created__lte=import_date, legal_date__isnull=False
        ).update(sort_date=F("legal_date"), modified=F("legal_date"))
        self.stdout.write("=> Changed records: ", num)
        num = Paper.objects.filter(legal_date__isnull=True).update(
            sort_date=fallback_date
        )
        self.stdout.write("=> Not determinable: ", num)

        self.stdout.write("Fixing files...")
        num = File.objects.filter(
            created__lte=import_date, legal_date__isnull=False
        ).update(sort_date=F("legal_date"), modified=F("legal_date"))
        self.stdout.write("=> Changed records: ", num)
        num = File.objects.filter(legal_date__isnull=True).update(
            sort_date=fallback_date
        )
        self.stdout.write("=> Not determinable: ", num)
