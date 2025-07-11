import pandas as pd
import os
from app import db, create_app
from app.models import BasicInfo, Appearance, OtherInfo, UrlInfo

def migrate_data_to_db():
    try:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        data_path = os.path.join(base_dir, '..', 'dc_data.csv')
        
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"CSV文件未找到: {data_path}")

        df = pd.read_csv(data_path)
        df = df.fillna('Unknown')

        db.session.query(UrlInfo).delete()
        db.session.query(OtherInfo).delete()
        db.session.query(Appearance).delete()
        db.session.query(BasicInfo).delete()

        for _, row in df.iterrows():
            try:
                page_id = int(row['page_id']) if str(row['page_id']).isdigit() else None
                if not page_id:
                    continue

                basic = BasicInfo(
                    page_id=page_id,
                    name=row['name'],
                    ID=row.get('ID', ''),
                    ALIGN=row.get('ALIGN', ''),
                    SEX=row.get('SEX', ''),
                    ALIVE=row.get('ALIVE', ''),
                    YEAR=str(row.get('YEAR', ''))
                )
                
                db.session.add(basic)
                db.session.flush()

                db.session.add_all([
                    Appearance(
                        page_id=page_id,
                        EYE=row.get('EYE', ''),
                        HAIR=row.get('HAIR', '')
                    ),
                    OtherInfo(
                        page_id=page_id,
                        GSM=row.get('GSM', ''),
                        APPEARANCES=str(row.get('APPEARANCES', '')),
                        FIRST_APPEARANCE=row.get('FIRST APPEARANCE', '')
                    ),
                    UrlInfo(
                        page_id=page_id,
                        urlslug=row.get('urlslug', '')
                    )
                ])

            except Exception as e:
                print(f"Error processing row {_}: {str(e)}")
                db.session.rollback()
                continue

        db.session.commit()
        print(f"Successfully import {db.session.query(BasicInfo).count()}")

    except Exception as e:
        db.session.rollback()
        print(f"Import Failed: {str(e)}")
        raise