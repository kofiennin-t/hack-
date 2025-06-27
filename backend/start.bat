@echo off
echo Starting AI Model Platform Backend...

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Copy environment file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your database credentials
    pause
)

REM Create logs directory
if not exist "logs\" (
    mkdir logs
)

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser (optional)
echo.
set /p create_superuser="Do you want to create a superuser? (y/n): "
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Start development server
echo.
echo Starting development server...
echo API will be available at: http://127.0.0.1:8000/
echo API Documentation at: http://127.0.0.1:8000/api/docs/
echo Admin panel at: http://127.0.0.1:8000/admin/
echo.
python manage.py runserver
