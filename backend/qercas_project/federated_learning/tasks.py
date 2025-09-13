from celery import shared_task
from federated_learning.services import FederatedTrainingService

@shared_task(name="federated_learning.tasks.run_federated_training")
def run_federated_training():
    """Celery task to run federated learning training"""
    try:
        model_path = FederatedTrainingService.run_training_cycle()
        return {
            'status': 'success',
            'model_path': model_path,
            'message': f'Model updated at: {model_path}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'message': 'Federated learning training failed'
        }
