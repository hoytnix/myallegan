from flask import Blueprint, render_template

business = Blueprint('business', __name__, template_folder='templates')


@business.route('/')
def index():
    return render_template('business/index.html')
