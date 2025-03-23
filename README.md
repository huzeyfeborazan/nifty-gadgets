# Nifty Gadgets

A community-driven platform where users share and discover affordable products under $50 that provide exceptional value.

## Features

- User authentication and profiles
- Create and manage product lists
- Browse other users' lists
- Affiliate link integration
- Modern, responsive UI with Tailwind CSS

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.x
- MariaDB/MySQL
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nifty-gadgets
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 4. Database Setup

1. Create the database:
```bash
mysql -u root -e "CREATE DATABASE IF NOT EXISTS nifty_gadgets CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

2. Create database user and grant privileges:
```bash
mysql -u root -e "CREATE USER 'nifty_admin'@'localhost' IDENTIFIED BY 'N1fty@2025DB-gadgets'; GRANT ALL PRIVILEGES ON nifty_gadgets.* TO 'nifty_admin'@'localhost'; FLUSH PRIVILEGES;"
```

### 5. Environment Configuration

1. Create a `.env` file in the project root with the following content:
```env
# Django Settings
DJANGO_SECRET_KEY=fd430dda2ff0457eb3dec040d91b384f
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=nifty_gadgets
DB_USER=nifty_admin
DB_PASSWORD=N1fty@2025DB-gadgets
DB_HOST=localhost
DB_PORT=3306
```

### 6. Run Migrations

```bash
python3 manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python3 manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python3 manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Project Structure

```
nifty-gadgets/
├── core/               # Main application
├── nifty_gadgets/     # Project configuration
├── templates/         # HTML templates
├── static/           # Static files
├── manage.py         # Django management script
├── requirements.txt  # Python dependencies
└── .env             # Environment variables
```

## Development Guidelines

1. Always activate the virtual environment before running any commands
2. Keep the `.env` file secure and never commit it to version control
3. Run migrations when making changes to models
4. Follow PEP 8 style guide for Python code

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues:
1. Ensure MariaDB/MySQL is running
2. Verify database credentials in `.env`
3. Check if the database user has proper privileges

### Static Files Not Loading

If static files are not loading:
1. Ensure the `static` directory exists
2. Run `python3 manage.py collectstatic` if needed
3. Check `STATICFILES_DIRS` in settings.py

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 