from flask import Blueprint, render_template, request, flash, redirect, url_for

from sqlalchemy import text

from myallegan.models import Business
from myallegan.forms import SearchForm, BusinessForm

blueprint_title = 'business'
business = Blueprint(blueprint_title, __name__, template_folder='templates',
                        url_prefix='/business')


# Index -----------------------------------------------------------------------
@business.route('/')
def index():
    return render_template('business/index.html')


# Details ---------------------------------------------------------------------
@business.route('/<string:slug>/<int:business_id>')
@business.route('/<int:business_id>')
def detail(business_id, slug=None):
    result = Business.query.filter(Business.id==business_id).first_or_404()

    params = {
        'result': result
    }
    return render_template('business/detail.html', **params)


# Administrative --------------------------------------------------------------
@business.route('/new', methods=['GET', 'POST'])
def new():
    business = Business()
    form = BusinessForm(obj=business)

    if form.validate_on_submit():
        form.populate_obj(business)

        form_params = {
            'title': business.title
        }

        if Business.create(form_params):
            flash('Business has been created successfully.', 'success')
            return redirect(url_for('{}.{}'.format(blueprint_title, 'index')))

    params = {
        'form': form,
        'business': business
    }
    return render_template('business/_form.html', **params)


@business.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    business = Business.query.get(id)
    form = BusinessForm(obj=business)

    if form.validate_on_submit():
        form.populate_obj(business)

        business.save()

        flash('Business has been saved successfully.', 'success')
        return redirect(url_for('{}.{}'.format(blueprint_title, 'detail'), 
                                business_id=id))

    params = {
        'form': form,
        'business': business
    }
    return render_template('business/_form.html', **params)


# Lists -----------------------------------------------------------------------
@business.route('/most-recent', defaults={'page': 1})
@business.route('/most-recent/page/<int:page>')
def most_recent(page):
    search_form = SearchForm()

    sort_by = Business.sort_by(request.args.get('sort', 'created_on'),
                               request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_results = Business.query \
            .filter(Business.search(request.args.get('q', ''))) \
            .order_by(text(order_values)) \
            .paginate(page, 50, True)

    params = {
        'form': search_form,
        'results': paginated_results
    }
    return render_template('business/list.html', **params)
