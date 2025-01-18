
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = "Generate test data"

    def handle(self, *args, **kwargs):
        self.create_users()
        
    def create_users(self):
        user, created = User.objects.get_or_create(username="admin", email="admin@example.com")
        if created:
            user.set_password("password")
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user: admin with password: password"))
        else:
            self.stdout.write(self.style.WARNING(f"User admin already exists"))

        user, created = User.objects.get_or_create(username="test", email="test@example.com")
        if created:
            user.set_password("password")
            # user.is_superuser = True
            # user.is_staff = True
            # admin_group = Group.objects.get(name='ADMIN')
            # user.groups.add(admin_group)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user: test with password: password"))
        else:
            self.stdout.write(self.style.WARNING(f"User test already exists"))