from flask import Blueprint, render_template, request
from app.data import load_data
from app.config import Config

character_bp = Blueprint('character', __name__)

data = load_data()

@character_bp.route('/')
def index():
    per_page = Config.PER_PAGE
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_characters = data[start:end]
    total_pages = (len(data) + per_page - 1) // per_page

    return render_template('index.html', characters=paginated_characters, page=page, total_pages=total_pages)

@character_bp.route('/character/<int:id>')
def character_detail(id):
    character = next((c for c in data if c['page_id'] == id), None)
    if character:
        return render_template('detail.html', character=character)
    else:
        return render_template('404.html'), 404