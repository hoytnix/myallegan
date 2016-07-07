from flask import Flask, render_template, request
from celery import Celery

from myallegan.blueprints.page.views import page

from myallegan.extensions import (
    db,
    debug_toolbar,
    login_manager,
    csrf
)

CELERY_TASK_LIST = [
    'myallegan.tasks'
]


def create_celery_app(app=None):
    """Create a new Celery object and tie together the Celery config to the
    app's config. Wrap all tasks in the context of the application.

    Args:
        app (Flask)

    Returns:
        celery (Celery)

    """

    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """Create a Flask application using the app factory pattern.

    Args:
        settings_override (obj): Key-values to be used for configuration.
    
    Returns:
        app (Flask): Fully configured Flask-object.

    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    extensions(app)
    template_processors(app)
    
    app.register_blueprint(page)
    
    error_templates(app)

    return app


def extensions(app):
    """Register 0 or more extensions.

    Mutates the app passed in.

    Args:
        app (Flask): Flask-application instance.

    Returns:
        None

    """

    db.init_app(app)
    debug_toolbar.init_app(app)
    #login_manager.init_app(app)
    csrf.init_app(app)

    return None


def template_processors(app):
    """Register 0 or more custom template processors.

    Mutates the app passed in.

    Args:
        app (Flask): Flask-application instance.

    Returns:
        jinja_env (Flask.jinja_env): Updated jinja environment.

    """

    #app.jinja_env.filters['filter_name'] = filter_function
    #app.jinja_env.globals.update(current_year=current_year)

    return app.jinja_env


def error_templates(app):
    """Register 0 or more custom error pages (mutates the app passed in).

    Args:
        app (Flask): Flask-application instance.
    
    Returns:
        None

    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, 'code', 500)
        return render_template('errors/{0}.html'.format(code)), code

    for error in [404, 429, 500]:
        app.errorhandler(error)(render_status)

    return None
