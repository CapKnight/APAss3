from flask import render_template
from app import app
from app.blueprints.character import character_bp

app.register_blueprint(character_bp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'), 500