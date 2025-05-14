import pandas as pd
import os

def load_linked_tables():
    try:
        # 获取 dc_data.csv 路径
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dc_data.csv')
        # 读取整个 CSV 文件
        df = pd.read_csv(data_path)
        # 处理空值
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
        # 创建关联表
        basic_info = df[['page_id', 'name', 'ID', 'ALIGN', 'SEX', 'ALIVE', 'YEAR']].copy()
        appearance = df[['page_id', 'EYE', 'HAIR']].copy()
        other_info = df[['page_id', 'GSM', 'APPEARANCES', 'FIRST APPEARANCE']].copy()
        url_info = df[['page_id', 'urlslug']].copy()
        
        print(f"Loaded {len(df)} characters into linked tables")
        return basic_info, appearance, other_info, url_info
    except FileNotFoundError:
        print("Error: dc_data.csv not found.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# 加载数据（供其他模块使用）
basic_info, appearance, other_info, url_info = load_linked_tables()