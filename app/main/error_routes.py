from flask import render_template

from app import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('partials/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('partials/500.html'), 500
