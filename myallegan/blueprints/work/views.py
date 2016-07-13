from flask import Blueprint, render_template, request, flash, redirect, url_for

from sqlalchemy import text

from myallegan.models import Work
from myallegan.forms import SearchForm, WorkForm

blueprint_title = 'work'
work = Blueprint(blueprint_title, __name__, template_folder='templates',
                        url_prefix='/work')


# Index -----------------------------------------------------------------------
@work.route('/')
def index():
    return render_template('work/index.html')


# Details ---------------------------------------------------------------------
@work.route('/<string:slug>/<int:work_id>')
@work.route('/<int:work_id>')
def detail(work_id, slug=None):
    result = Work.query.filter(Work.id==work_id).first_or_404()

    params = {
        'result': result
    }
    return render_template('work/detail.html', **params)


# Administrative --------------------------------------------------------------
@work.route('/new', methods=['GET', 'POST'])
def new():
    work = Work()
    form = WorkForm(obj=work)

    if form.validate_on_submit():
        form.populate_obj(work)

        form_params = {
            # Details
            'title': work.title,
            'salary': work.salary,
            'employment_status': work.employment_status,

            # Relationships
            'business_id': work.business_id
        }

        if Work.create(form_params):
            flash('Work has been created successfully.', 'success')
            return redirect(url_for('{}.{}'.format(blueprint_title, 'most_recent')))

    params = {
        'form': form,
        'work': work
    }
    return render_template('work/_form.html', **params)


@work.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    work = Work.query.get(id)
    form = WorkForm(obj=work)

    if form.validate_on_submit():
        form.populate_obj(work)

        work.save()

        flash('Work has been saved successfully.', 'success')
        return redirect(url_for('{}.{}'.format(blueprint_title, 'detail'), 
                                work_id=id))

    params = {
        'form': form,
        'work': work
    }
    return render_template('work/_form.html', **params)


# Lists -----------------------------------------------------------------------
@work.route('/most-recent', defaults={'page': 1})
@work.route('/most-recent/page/<int:page>')
def most_recent(page):
    search_form = SearchForm()

    sort_by = Work.sort_by(request.args.get('sort', 'created_on'),
                               request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_results = Work.query \
            .filter(Work.search(request.args.get('q', ''))) \
            .order_by(text(order_values)) \
            .paginate(page, 50, True)

    params = {
        'form': search_form,
        'results': paginated_results
    }
    return render_template('work/list.html', **params)


@work.route('/highest-paying', defaults={'page': 1})
@work.route('/highest-paying/page/<int:page>')
def highest_paying(page):
    search_form = SearchForm()

    paginated_results = Work.query \
            .filter(Work.search(request.args.get('q', ''))) \
            .order_by(Work.salary.desc(), Work.id.desc()) \
            .paginate(page, 50, True)

    params = {
        'form': search_form,
        'results': paginated_results
    }
    return render_template('work/list.html', **params)
