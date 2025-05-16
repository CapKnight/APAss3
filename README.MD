# DC Character Analysis Platform

A Flask-based web application for browsing, comparing, and analyzing DC character data, featuring data visualization and user-friendly navigation.

## Features

- **Character Browsing**: View a list of characters with their basic information, appearance, and other details.
- **Detail Page**: View the detail information about the characters
- **Character Comparison**: Compare multiple characters side by side based on their attributes.
- **Analysis Dashboard**: View statistics about character alignments (e.g., Good vs. Evil) with percentage breakdowns.
- **Error Handling**: Custom 404 and 500 error pages for a better user experience.
- **Responsive Design**: The application is mobile-friendly with a responsive layout and navigation.

### Steps
You can check the live deployment at: [https://apass3.onrender.com/](https://apass3.onrender.com/)

If you are using my codio, start the server using the terminal: `python3 run.py`. Then open your browser and navigate to `https://fossilelite-newsalgebra-5000.codio-box.uk/` to access the application.

If you are using in other platforms, follow these steps:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CapKnight/APAss3.git
   cd APAss3
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Development Server**:
   ```bash
   python3 run.py
   ```
   Open your browser and navigate to `https://fossilelite-newsalgebra-5000.codio-box.uk/` to access the application.

## Requirements

The following dependencies are listed in `requirements.txt`:

- Flask==2.3.3
- Flask-SQLAlchemy==3.1.1
- SQLAlchemy==2.0.23
- pandas==2.2.2
- Flask-Testing==0.8.1
- gunicorn==22.0.0
- numpy==1.26.4
- psycopg2-binary==2.9.9

## Testing

The project includes unit tests to ensure functionality. To run the tests:

```bash
python3 -m unittest discover -s tests
```

This will execute all test cases and provide a summary of the results.

### Data

Character data is stored in a PostgreSQL database on Render. Ensure you have set up the `DATABASE_URL` environment variable to connect to your database. For local development, you can use SQLite as a fallback by not setting the `DATABASE_URL`.

### Source

Characters' database is from a open source on Github: https://github.com/fivethirtyeight/data/blob/master/comic-characters/dc-wikia-data.csv
The background picture is also from a open source on Pinterest: https://uk.pinterest.com/pin/492649952861069/