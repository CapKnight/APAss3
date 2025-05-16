import os
  from app import create_app  # 从 app 包中导入 create_app

  app = create_app()

  if __name__ == "__main__":
      app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))