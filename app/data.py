import pandas as pd
import os

def load_data():
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dc_data.csv')
        # 读取 CSV 并处理空值
        df = pd.read_csv(data_path)
        df = df.fillna({
            'name': 'Unknown',
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
        # 转换为字典列表
        data = df.to_dict(orient='records')
        print(f"Loaded {len(data)} characters from CSV")
        return data
    except FileNotFoundError:
        print("Error: dc_data.csv not found.")
        return []