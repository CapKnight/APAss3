from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

try:
    data = pd.read_csv('dc_data.csv').to_dict(orient='records')
except FileNotFoundError:
    data = []
    print("Error: dc_data.csv not found.")

@app.route('/')
def index():
    return render_template('index.html', characters=data)

@app.route('/character/<int:id>')
def character_detail(id):
    character = next((c for c in data if c['page_id'] == id), None)
    if character:
        return render_template('detail.html', character=character)
    else:
        return "Character not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
