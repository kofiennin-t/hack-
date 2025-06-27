# AI Model Platform Backend

A comprehensive Django REST API backend for an AI model platform that allows users to access specialized AI models created by developers.

## Features

### Core Functionality
- **User Management**: Registration, authentication, profile management
- **Developer Profiles**: Developer registration and verification
- **AI Model Marketplace**: CRUD operations for AI models with detailed metadata
- **User History**: Track all interactions with AI models
- **Review System**: User reviews and ratings for AI models
- **API Usage Logging**: Comprehensive logging and analytics

### Technical Features
- **JWT Authentication**: Secure token-based authentication
- **PostgreSQL Database**: Robust relational database with UUID primary keys
- **RESTful API**: Well-structured REST endpoints with proper HTTP methods
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Input Validation**: Comprehensive request validation and error handling
- **Pagination**: Efficient pagination for large datasets
- **Filtering & Search**: Advanced filtering and search capabilities
- **Rate Limiting**: Built-in rate limiting for API endpoints
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip (Python package installer)

### Installation

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Run the Setup Script**
   ```bash
   # On Windows
   start.bat
   
   # On Linux/Mac
   chmod +x start.sh
   ./start.sh
   ```

3. **Manual Setup (Alternative)**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Copy environment file
   cp .env.example .env
   # Edit .env with your database credentials
   
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   
   # Start server
   python manage.py runserver
   ```

### Database Setup

1. **Create PostgreSQL Database**
   ```sql
   CREATE DATABASE ai_model_platform;
   CREATE USER postgres WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE ai_model_platform TO postgres;
   ```

2. **Update .env File**
   ```env
   DB_NAME=ai_model_platform
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/refresh/` - Refresh JWT token
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/verify/` - Verify JWT token

### Users
- `POST /api/v1/users/register/` - User registration
- `GET /api/v1/users/me/` - Get current user profile
- `PUT /api/v1/users/me/` - Update current user profile
- `GET /api/v1/users/` - List users (admin only)
- `GET /api/v1/users/{id}/` - Get user details
- `POST /api/v1/users/{id}/change_password/` - Change password
- `GET /api/v1/users/{id}/stats/` - Get user statistics

### Developers
- `POST /api/v1/developers/register/` - Register as developer
- `GET /api/v1/developers/` - List developers
- `GET /api/v1/developers/{id}/` - Get developer details
- `PUT /api/v1/developers/{id}/` - Update developer profile
- `GET /api/v1/developers/{id}/stats/` - Get developer statistics
- `GET /api/v1/developers/{id}/models/` - Get developer's models

### AI Models
- `GET /api/v1/models/` - List AI models
- `POST /api/v1/models/` - Create AI model (developers only)
- `GET /api/v1/models/{id}/` - Get model details
- `PUT /api/v1/models/{id}/` - Update model (owner only)
- `DELETE /api/v1/models/{id}/` - Delete model (owner only)
- `GET /api/v1/models/search/` - Advanced model search
- `GET /api/v1/models/featured/` - Get featured models
- `GET /api/v1/models/categories/` - Get model categories
- `GET /api/v1/models/{id}/stats/` - Get model statistics
- `GET /api/v1/models/{id}/reviews/` - Get model reviews

### User History
- `GET /api/v1/history/` - Get user's interaction history
- `POST /api/v1/history/` - Create history entry
- `GET /api/v1/history/{id}/` - Get history details
- `PUT /api/v1/history/{id}/` - Update history (rating/feedback)
- `GET /api/v1/history/stats/` - Get user history statistics
- `GET /api/v1/history/sessions/` - Get user sessions
- `GET /api/v1/history/timeline/` - Get interaction timeline
- `GET /api/v1/history/export/` - Export history to CSV

### Reviews
- `GET /api/v1/reviews/` - List reviews
- `POST /api/v1/reviews/` - Create review
- `GET /api/v1/reviews/{id}/` - Get review details
- `PUT /api/v1/reviews/{id}/` - Update review (owner only)
- `DELETE /api/v1/reviews/{id}/` - Delete review (owner only)
- `POST /api/v1/reviews/{id}/vote/` - Vote on review helpfulness
- `DELETE /api/v1/reviews/{id}/remove_vote/` - Remove vote
- `GET /api/v1/reviews/stats/model/{model_id}/` - Model review stats
- `GET /api/v1/reviews/stats/user/` - User review stats

### API Logs
- `GET /api/v1/logs/usage/` - Get API usage logs
- `POST /api/v1/logs/usage/` - Create usage log entry
- `GET /api/v1/logs/metrics/` - Get API metrics
- `GET /api/v1/logs/stats/` - Get general API statistics (admin)
- `GET /api/v1/logs/stats/developer/{id}/` - Developer API stats
- `GET /api/v1/logs/stats/model/{id}/` - Model API stats

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

## Database Schema

The platform uses the following main entities:

### Users
- User authentication and profile management
- Supports email verification and password reset
- Activity tracking (login count, last login)

### Developers
- Extended profiles for AI model creators
- API key management and quota tracking
- Revenue and performance metrics

### AI Models
- Comprehensive model metadata and configuration
- Pricing models (per-request, per-token, subscription, free)
- Rate limiting and performance tracking
- Categories, tags, and search optimization

### User History
- Complete interaction tracking with AI models
- Session management and analytics
- Cost calculation and user feedback

### Reviews
- User reviews and ratings for models
- Helpfulness voting system
- Verification based on usage history

### API Logs
- Comprehensive API usage logging
- Performance metrics and analytics
- Error tracking and monitoring

## Authentication

The platform uses JWT (JSON Web Tokens) for authentication:

```python
# Include token in requests
headers = {
    'Authorization': 'Bearer <your_access_token>',
    'Content-Type': 'application/json'
}
```

## Error Handling

The API returns consistent error responses:

```json
{
    "error": true,
    "message": "Error description",
    "details": {
        "field": ["Specific field error"]
    },
    "status_code": 400
}
```

## Rate Limiting

API endpoints have built-in rate limiting:
- Default: 1000 requests per hour per user
- Model-specific limits can be configured
- Rate limit headers included in responses

## Development

### Project Structure
```
backend/
├── ai_platform/          # Main Django project
├── core/                 # Shared utilities and base models
├── authentication/       # JWT authentication views
├── users/               # User management
├── developers/          # Developer profiles
├── ai_models/           # AI model management
├── user_history/        # Interaction tracking
├── reviews/             # Review system
├── api_logs/            # API logging
├── static/              # Static files
├── media/               # Media uploads
├── logs/                # Application logs
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── manage.py           # Django management script
```

### Adding New Features

1. Create new app: `python manage.py startapp app_name`
2. Add models in `app_name/models.py`
3. Create serializers in `app_name/serializers.py`
4. Implement views in `app_name/views.py`
5. Configure URLs in `app_name/urls.py`
6. Update main `urls.py` to include app URLs
7. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment

### Production Settings

1. Set `DEBUG=False` in `.env`
2. Configure production database
3. Set up static file serving
4. Configure logging
5. Set up monitoring

### Docker Deployment

```dockerfile
# Use Python 3.9 slim image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=ai_platform.settings

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ai_platform.wsgi:application"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions and support:
- Check the API documentation at `/api/docs/`
- Review the database schema in `/db/` directory
- Open an issue for bugs or feature requests
