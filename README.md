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

## Acknowledgments

- [FastF1](https://github.com/theOehrly/Fast-F1) - The amazing F1 data API
- [Django](https://www.djangoproject.com/) - The web framework
- Formula 1 - For the exciting sport and data
