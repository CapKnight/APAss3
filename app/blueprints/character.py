from flask import Blueprint, render_template, request
from app.data import basic_info, appearance, other_info
from app.config import Config

character_bp = Blueprint('character', __name__)

@character_bp.route('/')
def index():
    per_page = Config.PER_PAGE
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    
    # 使用 basic_info 进行分页
    paginated_basic = basic_info.iloc[start:end]
    # 合并其他表数据
    merged_data = paginated_basic.merge(appearance, on='page_id', how='left') \
                                .merge(other_info, on='page_id', how='left')
    
    total_pages = (len(basic_info) + per_page - 1) // per_page
    return render_template('index.html', characters=merged_data.to_dict(orient='records'), page=page, total_pages=total_pages)

@character_bp.route('/character/<int:id>')
def character_detail(id):
    # 从基本信息表查询
    character_basic = basic_info[basic_info['page_id'] == id]
    if character_basic.empty:
        return render_template('404.html'), 404
    
    # 合并其他表数据
    character_appearance = appearance[appearance['page_id'] == id]
    character_other = other_info[other_info['page_id'] == id]
    
    character = character_basic.iloc[0].to_dict()
    character.update(character_appearance.iloc[0].to_dict() if not character_appearance.empty else {})
    character.update(character_other.iloc[0].to_dict() if not character_other.empty else {})
    
    return render_template('detail.html', character=character)