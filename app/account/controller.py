from flask import Blueprint, render_template

account_routes = Blueprint('account', __name__, template_folder='.')


@account_routes.route('/create')
def create_account():
    return render_template('create.html')
