from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.models import BasicInfo, Appearance, OtherInfo, UrlInfo
from app.config import Config

character_bp = Blueprint('character', __name__)

@character_bp.route('/')
def index():
    per_page = Config.PER_PAGE
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * per_page
    
    selected_ids = session.get('selected_ids', [])
    
    # 使用数据库分页
    basic_query = BasicInfo.query.offset(start).limit(per_page).all()
    total_count = BasicInfo.query.count()
    total_pages = (total_count + per_page - 1) // per_page
    
    characters = []
    for basic in basic_query:
        appearance = Appearance.query.filter_by(page_id=basic.page_id).first()
        other = OtherInfo.query.filter_by(page_id=basic.page_id).first()
        url = UrlInfo.query.filter_by(page_id=basic.page_id).first()
        char = {
            'page_id': basic.page_id,
            'name': basic.name,
            'ID': basic.ID,
            'ALIGN': basic.ALIGN,
            'SEX': basic.SEX,
            'ALIVE': basic.ALIVE,
            'YEAR': basic.YEAR,
            'EYE': appearance.EYE if appearance else 'Unknown',
            'HAIR': appearance.HAIR if appearance else 'Unknown',
            'GSM': other.GSM if other else 'Unknown',
            'APPEARANCES': other.APPEARANCES if other else 'N/A',
            'FIRST APPEARANCE': other.FIRST_APPEARANCE if other else 'N/A',
            'urlslug': url.urlslug if url else 'N/A'
        }
        characters.append(char)
    
    return render_template('index.html', characters=characters, page=page, total_pages=total_pages, selected_ids=selected_ids)

@character_bp.route('/character/<int:id>')
def character_detail(id):
    character_basic = BasicInfo.query.get_or_404(id)
    
    character_appearance = Appearance.query.filter_by(page_id=id).first()
    character_other = OtherInfo.query.filter_by(page_id=id).first()
    character_url = UrlInfo.query.filter_by(page_id=id).first()
    
    character = {
        'page_id': character_basic.page_id,
        'name': character_basic.name,
        'ID': character_basic.ID,
        'ALIGN': character_basic.ALIGN,
        'SEX': character_basic.SEX,
        'ALIVE': character_basic.ALIVE,
        'YEAR': character_basic.YEAR,
        'EYE': character_appearance.EYE if character_appearance else 'Unknown',
        'HAIR': character_appearance.HAIR if character_appearance else 'Unknown',
        'GSM': character_other.GSM if character_other else 'Unknown',
        'APPEARANCES': character_other.APPEARANCES if character_other else 'N/A',
        'FIRST APPEARANCE': character_other.FIRST_APPEARANCE if character_other else 'N/A',
        'urlslug': character_url.urlslug if character_url else 'N/A'
    }
    
    selected_ids = session.get('selected_ids', [])
    return render_template('detail.html', character=character, selected_ids=selected_ids)

@character_bp.route('/compare')
def compare():
    selected_ids = session.get('selected_ids', [])
    if not selected_ids:
        return "No characters selected. <a href='" + url_for('character.index') + "'>Back to Home</a>", 400
    
    selected_ids = [int(id) for id in selected_ids]
    
    characters = []
    for idx in selected_ids:
        char_basic = BasicInfo.query.get(idx)
        if not char_basic:
            continue
        char_appearance = Appearance.query.filter_by(page_id=idx).first()
        char_other = OtherInfo.query.filter_by(page_id=idx).first()
        char_url = UrlInfo.query.filter_by(page_id=idx).first()
        char = {
            'page_id': char_basic.page_id,
            'name': char_basic.name,
            'ID': char_basic.ID,
            'ALIGN': char_basic.ALIGN,
            'SEX': char_basic.SEX,
            'ALIVE': char_basic.ALIVE,
            'YEAR': char_basic.YEAR,
            'EYE': char_appearance.EYE if char_appearance else 'Unknown',
            'HAIR': char_appearance.HAIR if char_appearance else 'Unknown',
            'GSM': char_other.GSM if char_other else 'Unknown',
            'APPEARANCES': char_other.APPEARANCES if char_other else 'N/A',
            'FIRST APPEARANCE': char_other.FIRST_APPEARANCE if char_other else 'N/A',
            'urlslug': char_url.urlslug if char_url else 'N/A'
        }
        characters.append(char)
    
    return render_template('compare.html', characters=characters)

@character_bp.route('/compare/remove/<int:id>')
def remove_from_compare(id):
    selected_ids = session.get('selected_ids', [])
    if selected_ids:
        selected_ids = [int(i) for i in selected_ids if int(i) != id]
        session['selected_ids'] = selected_ids
        session.modified = True
    
    if selected_ids:
        return redirect(url_for('character.compare'))
    else:
        return redirect(url_for('character.index'))

@character_bp.route('/toggle_selection/<int:id>', methods=['POST'])
def toggle_selection(id):
    selected_ids = session.get('selected_ids', [])
    if id in selected_ids:
        selected_ids.remove(id)
    else:
        selected_ids.append(id)
    session['selected_ids'] = selected_ids
    session.modified = True
    return jsonify({'status': 'success', 'selected': id in selected_ids})