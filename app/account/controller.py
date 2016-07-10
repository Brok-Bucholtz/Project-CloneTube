from flask import Blueprint, render_template

account_page_routes = Blueprint('account_page', __name__, template_folder='.')


@account_page_routes.route('/create')
def create_account():
    return render_template('create.html')
