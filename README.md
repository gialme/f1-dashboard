# Formula 1 Dashboard

A Django web application that displays Formula 1 racing data and statistics using the FastF1 API.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gialme/F1-Dashboard.git
   cd F1-Dashboard
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py migrate
   ```

## Running the Application

1. **Start the development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the dashboard**
   
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Deploy with Docker

Using **Docker Compose**, you can easily build and run the entire environment with a single command.

### Environment configuration

Before starting, create a `.env` file in the root of the project and add the required environment variables:

```txt
# PostgreSQL
DB_NAME=f1_dashboard_db
DB_USER=postgres
DB_PASSWORD=superpassword
DB_HOST=db
DB_PORT=5432

# Django
SECRET_KEY=changeme
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

> [!WARNING]  
> **Never commit** your `.env` file with sensitive information to public repositories.

### Running the project

To build and start all containers:

``` bash
docker-compose up --build
```

- The **PostgreSQL database** will run on port `5432`.
- The **Django** web application will be available at [http://localhost:8000](http://localhost:8000).

## Acknowledgments

- [FastF1](https://github.com/theOehrly/Fast-F1) - The amazing F1 data API
- [Django](https://www.djangoproject.com/) - The web framework
- Formula 1 - For the exciting sport and data
