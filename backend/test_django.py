#!/usr/bin/env python
"""
Simple Django test script to check if everything imports correctly
"""
import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_platform.settings_dev')

# Setup Django
django.setup()

# Try importing some models
try:
    from users.models import User
    from developers.models import Developer
    from ai_models.models import AIModel
    print("✅ All models imported successfully!")
    
    # Check database connection
    from django.db import connection
    cursor = connection.cursor()
    print("✅ Database connection successful!")
    
    print("Django setup completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
