from myallegan.models import Work

from math import ceil, floor

from myallegan.app import create_celery_app
from myallegan.extensions import db

celery = create_celery_app()


@celery.task()
def adjust_salary_percentile():
    """Task to update the salary percentiles.
    
    A remainder of 1 is assigned to the middle-percentile, and a remainder of 2
    is assigned to the lower-bound and middle.
    """

    return Work.update_percentiles()
