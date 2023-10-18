from flask import render_template, Blueprint

error = Blueprint('error',__name__, static_folder='asset', template_folder='view')

@error.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@error.errorhandler(405)
def not_found(e):
    return render_template('405.html')