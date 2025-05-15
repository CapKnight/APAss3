from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.models import BasicInfo, Appearance, OtherInfo, UrlInfo
from app.config import Config
from sqlalchemy import distinct, asc, desc, func, cast, Integer
from collections import defaultdict

character_bp = Blueprint('character', __name__)

@character_bp.route('/')
def index():
    per_page = Config.PER_PAGE
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * per_page

    search_name = request.args.get('search_name', '')
    filter_id = request.args.get('filter_id', '')
    filter_align = request.args.get('filter_align', '')
    filter_eye = request.args.get('filter_eye', '')
    filter_hair = request.args.get('filter_hair', '')
    filter_sex = request.args.get('filter_sex', '')
    filter_alive = request.args.get('filter_alive', '')
    sort_appearances = request.args.get('sort_appearances', 'asc')
    
    selected_ids = session.get('selected_ids', [])
    
    # 获取筛选字段的唯一值
    id_values = [id[0] for id in BasicInfo.query.with_entities(distinct(BasicInfo.ID)).all() if id[0] and id[0] != 'N/A']
    align_values = [align[0] for align in BasicInfo.query.with_entities(distinct(BasicInfo.ALIGN)).all() if align[0] and align[0] != 'Unknown']
    eye_values = [eye[0] for eye in Appearance.query.with_entities(distinct(Appearance.EYE)).all() if eye[0] and eye[0] != 'Unknown']
    hair_values = [hair[0] for hair in Appearance.query.with_entities(distinct(Appearance.HAIR)).all() if hair[0] and hair[0] != 'Unknown']
    sex_values = [sex[0] for sex in BasicInfo.query.with_entities(distinct(BasicInfo.SEX)).all() if sex[0] and sex[0] != 'Unknown']
    alive_values = [alive[0] for alive in BasicInfo.query.with_entities(distinct(BasicInfo.ALIVE)).all() if alive[0] and alive[0] != 'Unknown']
    
    # 构建查询
    query = BasicInfo.query
    if search_name:
        query = query.filter(BasicInfo.name.ilike(f'%{search_name}%'))
    if filter_id and filter_id != 'All':
        query = query.filter(BasicInfo.ID == filter_id)
    if filter_align and filter_align != 'All':
        query = query.filter(BasicInfo.ALIGN == filter_align)
    if filter_eye and filter_eye != 'All':
        query = query.join(Appearance).filter(Appearance.EYE == filter_eye)
    if filter_hair and filter_hair != 'All':
        query = query.join(Appearance).filter(Appearance.HAIR == filter_hair)
    if filter_sex and filter_sex != 'All':
        query = query.filter(BasicInfo.SEX == filter_sex)
    if filter_alive and filter_alive != 'All':
        query = query.filter(BasicInfo.ALIVE == filter_alive)
    
    # 加入 OtherInfo 表以访问 APPEARANCES
    query = query.join(OtherInfo, BasicInfo.page_id == OtherInfo.page_id)
    
    # 按 APPEARANCES 排序
    sort_func_appearances = asc if sort_appearances == 'asc' else desc
    query = query.order_by(sort_func_appearances(
        func.cast(func.coalesce(OtherInfo.APPEARANCES, '0'), Integer)
    ))
    
    # 应用分页
    total_count = query.count()
    basic_query = query.offset(start).limit(per_page).all()
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
    
    return render_template('index.html', characters=characters, page=page, total_pages=total_pages, selected_ids=selected_ids,
                          search_name=search_name, filter_id=filter_id, filter_align=filter_align, filter_eye=filter_eye,
                          filter_hair=filter_hair, filter_sex=filter_sex, filter_alive=filter_alive,
                          id_values=id_values, align_values=align_values, eye_values=eye_values,
                          hair_values=hair_values, sex_values=sex_values, alive_values=alive_values,
                          sort_appearances=sort_appearances)

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
        return render_template('compare.html', characters=[], message="No characters selected."), 400
    
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

@character_bp.route('/clear_filters')
def clear_filters():
    return redirect(url_for('character.index', 
                            page=1, 
                            search_name='', 
                            filter_id='All', 
                            filter_align='All', 
                            filter_eye='All', 
                            filter_hair='All', 
                            filter_sex='All', 
                            filter_alive='All', 
                            sort_appearances='asc'))

@character_bp.route('/toggle_selection/<int:id>', methods=['POST'])
def toggle_selection(id):
    # 获取当前筛选和分页状态
    page = request.form.get('page', 1, type=int)
    search_name = request.form.get('search_name', '')
    filter_id = request.form.get('filter_id', '')
    filter_align = request.form.get('filter_align', '')
    filter_eye = request.form.get('filter_eye', '')
    filter_hair = request.form.get('filter_hair', '')
    filter_sex = request.form.get('filter_sex', '')
    filter_alive = request.form.get('filter_alive', '')
    sort_appearances = request.form.get('sort_appearances', 'asc')
    
    # 更新 selected_ids
    selected_ids = session.get('selected_ids', [])
    is_selected = request.form.get('select') == '1'
    
    if is_selected and id not in selected_ids:
        selected_ids.append(id)
    elif not is_selected and id in selected_ids:
        selected_ids.remove(id)
    
    session['selected_ids'] = selected_ids
    session.modified = True
    
    # 重定向回 index，保持筛选和分页状态
    return redirect(url_for('character.index', page=page, search_name=search_name, filter_id=filter_id,
                            filter_align=filter_align, filter_eye=filter_eye, filter_hair=filter_hair,
                            filter_sex=filter_sex, filter_alive=filter_alive, sort_appearances=sort_appearances))

@character_bp.route('/analysis')
def analysis():
    # 阵营比例
    total_chars = BasicInfo.query.count()
    alignment_counts = {
        'Good': BasicInfo.query.filter(BasicInfo.ALIGN.ilike('%Good%')).count(),
        'Bad': BasicInfo.query.filter(BasicInfo.ALIGN.ilike('%Bad%')).count(),
        'Neutral': BasicInfo.query.filter(BasicInfo.ALIGN.ilike('%Neutral%')).count()
    }
    
    # 性别统计（简化：仅统计 Male, Female, Unknown）
    gender_counts = {
        'Male': 0,
        'Female': 0,
        'Unknown': 0
    }
    for char in BasicInfo.query.all():
        gender = char.SEX if char.SEX else 'Unknown'
        if gender == 'Unknown' or gender == 'Genderless Characters':
            gender_counts['Unknown'] += 1
        elif 'Male' in gender:
            gender_counts['Male'] += 1
        elif 'Female' in gender:
            gender_counts['Female'] += 1
    
    return render_template('analysis.html', 
                          total_chars=total_chars, 
                          alignment_counts=alignment_counts, 
                          gender_counts=gender_counts)