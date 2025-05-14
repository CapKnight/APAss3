import pandas as pd
import os
from app import db
from app.models import BasicInfo, Appearance, OtherInfo, UrlInfo

def migrate_data_to_db():
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dc_data.csv')
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
            basic = BasicInfo(
                page_id=row['page_id'],
                name=row['name'],
                ID=row['ID'],
                ALIGN=row['ALIGN'],
                SEX=row['SEX'],
                ALIVE=row['ALIVE'],
                YEAR=row['YEAR']
            )
            db.session.add(basic)

            # 插入 Appearance
            appearance = Appearance(
                page_id=row['page_id'],
                EYE=row['EYE'],
                HAIR=row['HAIR']
            )
            db.session.add(appearance)

            # 插入 OtherInfo
            other = OtherInfo(
                page_id=row['page_id'],
                GSM=row['GSM'],
                APPEARANCES=row['APPEARANCES'],
                FIRST_APPEARANCE=row['FIRST APPEARANCE']
            )
            db.session.add(other)

            # 插入 UrlInfo
            url = UrlInfo(
                page_id=row['page_id'],
                urlslug=row['urlslug']
            )
            db.session.add(url)

        db.session.commit()
        print(f"Migrated {len(df)} characters to database")
    except Exception as e:
        print(f"Error migrating data: {e}")
        db.session.rollback()

if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.drop_all()  # 删除现有表（可选，仅用于测试）
        db.create_all()  # 重新创建表
        migrate_data_to_db()