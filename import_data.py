import os
from app.data import migrate_data_to_db
from app import create_app

def initialize_database():
    app = create_app()
    with app.app_context():
        print("Starting data import...")
        migrate_data_to_db()
        print("Data import completed")

if __name__ == "__main__":
    initialize_database()