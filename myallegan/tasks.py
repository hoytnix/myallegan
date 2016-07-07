from myallegan.app import create_celery_app

celery = create_celery_app()


@celery.task()
def do_nothing():
    """Placeholder function."""

    return None
