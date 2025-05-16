# Character Analysis Platform

A Flask-based web application for browsing, comparing, and analyzing character data, featuring data visualization and user-friendly navigation.

## Features

- **Character Browsing**: View a list of characters with their basic information, appearance, and other details.
- **Character Comparison**: Compare two characters side by side based on their attributes.
- **Analysis Dashboard**: View statistics about character alignments (e.g., Good vs. Evil) with percentage breakdowns.
- **Error Handling**: Custom 404 and 500 error pages for a better user experience.
- **Responsive Design**: The application is mobile-friendly with a responsive layout and navigation.

### Account
This application does not require user authentication. All features are accessible without logging in.

### Steps
You can check the live deployment at: [https://apass3.onrender.com/](https://apass3.onrender.com/)

If you are using a local development environment like Codio, start the server using the terminal: `python3 run.py`. Then open your browser and navigate to `http://localhost:5000` to access the application.

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/apass3.git
   cd apass3
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Development Server**:
   ```bash
   python3 run.py
   ```
   Open your browser and navigate to `http://localhost:5000` to access the application.

## Requirements

The following dependencies are listed in `requirements.txt`:

- Flask==2.3.3
- Flask-SQLAlchemy==3.1.1
- SQLAlchemy==2.0.23
- pandas==2.2.2
- Flask-Testing==0.8.1
- gunicorn==22.0.0
- numpy==1.26.4
- psycopg2-binary==2.9.9 (for PostgreSQL support)

To generate the `requirements.txt` file, you can use:
```bash
pip freeze > requirements.txt
```

## Testing

The project includes unit tests to ensure functionality. To run the tests:

```bash
python -m unittest discover -s tests
```

This will execute all test cases and provide a summary of the results.

### Data

Character data is stored in a PostgreSQL database on Render. Ensure you have set up the `DATABASE_URL` environment variable to connect to your database. For local development, you can use SQLite as a fallback by not setting the `DATABASE_URL`.

To initialize the database tables:
```bash
python -c "from app import db, create_app; app = create_app(); with app.app_context(): db.create_all()"
```

If you have a data loading script (e.g., `app/data.py`), run:
```bash
python -m app.data
```