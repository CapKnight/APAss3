from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.data import basic_info, appearance, other_info, url_info
from app.config import Config

character_bp = Blueprint('character', __name__)

@character_bp.route('/')
def index():
    per_page = Config.PER_PAGE
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    
    selected_ids = session.get('selected_ids', [])
    
    paginated_basic = basic_info.iloc[start:end]
    merged_data = paginated_basic.merge(appearance, on='page_id', how='left') \
                                .merge(other_info, on='page_id', how='left') \
                                .merge(url_info, on='page_id', how='left')
    
    total_pages = (len(basic_info) + per_page - 1) // per_page
    return render_template('index.html', characters=merged_data.to_dict(orient='records'), page=page, total_pages=total_pages, selected_ids=selected_ids)

@character_bp.route('/character/<int:id>')
def character_detail(id):
    character_basic = basic_info[basic_info['page_id'] == id]
    if character_basic.empty:
        return render_template('404.html'), 404
    
    character_appearance = appearance[appearance['page_id'] == id]
    character_other = other_info[other_info['page_id'] == id]
    character_url = url_info[url_info['page_id'] == id]
    
    character = character_basic.iloc[0].to_dict()
    character.update(character_appearance.iloc[0].to_dict() if not character_appearance.empty else {})
    character.update(character_other.iloc[0].to_dict() if not character_other.empty else {})
    character.update(character_url.iloc[0].to_dict() if not character_url.empty else {})
    
    selected_ids = session.get('selected_ids', [])
    return render_template('detail.html', character=character, selected_ids=selected_ids)

@character_bp.route('/compare')
def compare():
    selected_ids = session.get('selected_ids', [])
    if not selected_ids:
        return "No characters selected. <a href='" + url_for('character.index') + "'>Back to Home</a>", 400
    
    selected_ids = [int(id) for id in selected_ids]
    
    selected_basic = basic_info[basic_info['page_id'].isin(selected_ids)]
    selected_appearance = appearance[appearance['page_id'].isin(selected_ids)]
    selected_other = other_info[other_info['page_id'].isin(selected_ids)]
    selected_url = url_info[url_info['page_id'].isin(selected_ids)]
    
    characters = []
    for idx in selected_ids:
        char_basic = selected_basic[selected_basic['page_id'] == idx].iloc[0].to_dict()
        char_appearance = selected_appearance[selected_appearance['page_id'] == idx].iloc[0].to_dict() if not selected_appearance.empty else {}
        char_other = selected_other[selected_other['page_id'] == idx].iloc[0].to_dict() if not selected_other.empty else {}
        char_url = selected_url[selected_url['page_id'] == idx].iloc[0].to_dict() if not selected_url.empty else {}
        char = char_basic.copy()
        char.update(char_appearance)
        char.update(char_other)
        char.update(char_url)
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