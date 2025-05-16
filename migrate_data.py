import os
from app import create_app, db
from app.models import BasicInfo, Appearance, OtherInfo, UrlInfo
from sqlalchemy import create_engine
import pandas as pd

def migrate_from_sqlite():
    app = create_app()
    with app.app_context():
        # 从SQLite提取数据
        sqlite_engine = create_engine('sqlite:///characters.db')
        
        tables = {
            'basic_info': BasicInfo,
            'appearance': Appearance,
            'other_info': OtherInfo,
            'url_info': UrlInfo
        }

        for table_name, model in tables.items():
            # 使用pandas读取SQLite数据
            df = pd.read_sql_table(table_name, sqlite_engine)
            
            # 写入PostgreSQL
            if not df.empty:
                df.to_sql(
                    table_name,
                    db.engine,
                    if_exists='append',
                    index=False,
                    method='multi'
                )
                print(f"Migrated {len(df)} rows to {table_name}")

if __name__ == '__main__':
    migrate_from_sqlite()