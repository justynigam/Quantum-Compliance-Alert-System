from django.core.management.base import BaseCommand
from federated_learning.tasks import run_federated_training

class Command(BaseCommand):
    help = 'Runs one cycle of federated learning to train the global risk model.'

    def handle(self, *args, **options):
        self.stdout.write("Starting federated learning process...")
        result = run_federated_training.delay()
        self.stdout.write(self.style.SUCCESS(
            f"Federated learning task started with ID: {result.id}"
        ))
