import pandas as pd
import os
from app import db, create_app
from app.models import BasicInfo, Appearance, OtherInfo, UrlInfo

def migrate_data_to_db():
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dc_data.csv')
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found at {data_path}")
        df = pd.read_csv(data_path)
        df = df.fillna({
            'page_id': 'N/A',
            'name': 'Unknown',
            'urlslug': 'N/A',
            'ID': 'N/A',
            'ALIGN': 'Unknown',
            'EYE': 'Unknown',
            'HAIR': 'Unknown',
            'SEX': 'Unknown',
            'GSM': 'Unknown',
            'ALIVE': 'Unknown',
            'APPEARANCES': 'N/A',
            'FIRST APPEARANCE': 'N/A',
            'YEAR': 'N/A'
        })

        for _, row in df.iterrows():
            # 转换为整数，处理非数字情况
            page_id = row['page_id']
            if page_id == 'N/A' or not str(page_id).isdigit():
                page_id = None  # 或分配一个默认值
            else:
                page_id = int(page_id)

            if page_id is None:
                continue  # 跳过无效 page_id

            # 创建 BasicInfo
            basic = BasicInfo(
                page_id=page_id,
                name=row['name'],
                ID=row['ID'],
                ALIGN=row['ALIGN'],
                SEX=row['SEX'],
                ALIVE=row['ALIVE'],
                YEAR=row['YEAR']
            )
            db.session.add(basic)

            # 关联 Appearance
            appearance = Appearance(
                page_id=page_id,
                EYE=row['EYE'],
                HAIR=row['HAIR']
            )
            basic.appearance = appearance  # 建立关系
            db.session.add(appearance)

            # 关联 OtherInfo
            other = OtherInfo(
                page_id=page_id,
                GSM=row['GSM'],
                APPEARANCES=row['APPEARANCES'],
                FIRST_APPEARANCE=row['FIRST APPEARANCE']
            )
            basic.other_info = other  # 建立关系
            db.session.add(other)

            # 关联 UrlInfo
            url = UrlInfo(
                page_id=page_id,
                urlslug=row['urlslug']
            )
            basic.url_info = url  # 建立关系
            db.session.add(url)

        db.session.commit()
        print(f"Migrated {db.session.query(BasicInfo).count()} characters to database")
    except Exception as e:
        print(f"Error migrating data: {e}")
        db.session.rollback()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.drop_all()  # 删除现有表（可选，仅用于测试）
        db.create_all()  # 重新创建表
        migrate_data_to_db()