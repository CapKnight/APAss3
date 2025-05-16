import os
from app import app  # 导入已定义的 app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))

gunicorn "app:create_app()"