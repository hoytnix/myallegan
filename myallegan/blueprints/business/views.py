from flask import Blueprint, render_template, request

from sqlalchemy import text

from myallegan.models import Business
from myallegan.forms import SearchForm

business = Blueprint('business', __name__, template_folder='templates',
                        url_prefix='/business')


@business.route('/')
def index():
    return render_template('business/index.html')


@business.route('/')
def detail():
    pass


# Lists -----------------------------------------------------------------------
@business.route('/most-recent', defaults={'page': 1})
@business.route('/most-recent/page/<int:page>')
def most_recent(page):
    search_form = SearchForm()

    sort_by = Business.sort_by(request.args.get('sort', 'created_on'),
                               request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_businesses = Business.query \
            .filter(Business.search(request.args.get('q', ''))) \
            .order_by(text(order_values)) \
            .paginate(page, 50, True)

    return render_template('business/list.html', form=search_form,
            businesses=paginated_businesses)
