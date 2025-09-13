from .celery import app as celery_app

if __name__ == '__main__':
    celery_app.main()

__all__ = ('celery_app',)