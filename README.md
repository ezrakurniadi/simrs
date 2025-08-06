# EHR System

Electronic Health Record (EHR) system for healthcare facilities.

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Make sure PostgreSQL is installed and running
   - Create databases for development, testing, and production environments
   - Update the .env files with your database credentials

5. Run the application:
   ```bash
   flask run
   ```

## Environment Configuration

The application uses different configuration files for different environments:
- Development: `.env.development`
- Testing: `.env.testing`
- Production: `.env.production`

The default environment is development. To change the environment, set the `FLASK_ENV` variable:
```bash
export FLASK_ENV=production  # On macOS/Linux
set FLASK_ENV=production     # On Windows
```

## Database Migrations

To initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade