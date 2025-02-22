from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta
from sample.models import Test  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Generates random test data for the Test model'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create a list to store all instances
        test_instances = []
        
        # Generate base datetime for random date range
        base_date = timezone.now()
        
        self.stdout.write('Generating 200 random records...')
        
        for _ in range(200):
            # Generate random date within last 30 days
            random_days = random.randint(-30, 0)
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            random_date = base_date + timedelta(
                days=random_days,
                hours=random_hours,
                minutes=random_minutes
            )
            
            test_instance = Test(
                text=fake.text(max_nb_chars=100),
                date=random_date,
                bool=random.choice([True, False]),
                number=random.randint(0, 1000),
                float=round(random.uniform(0, 100), 2)
            )
            test_instances.append(test_instance)
        
        # Bulk create all instances
        Test.objects.bulk_create(test_instances)
        
        self.stdout.write(self.style.SUCCESS('Successfully created 200 test records!'))