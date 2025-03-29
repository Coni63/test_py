from django.core.management.base import BaseCommand, CommandError
from customer.models import Domain, Tenant


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)

    def handle(self, *args, **options):
        name = options["name"]
        tenant = Tenant(schema_name=name, name=name)
        tenant.save()

        domain = Domain()
        domain.domain = f'{name}.localhost'  # For local testing
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()