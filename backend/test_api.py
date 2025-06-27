"""
API Test Script for AI Model Platform Backend

This script tests all the major API endpoints to ensure they're working correctly.
Run this after starting the server with: python test_api.py
"""

import requests
import json
import uuid
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000/api/v1"
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_PASSWORD = "testpass123"
TEST_DEVELOPER_EMAIL = "developer@example.com"
TEST_DEVELOPER_PASSWORD = "devpass123"

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.user_token = None
        self.developer_token = None
        self.test_user_id = None
        self.test_developer_id = None
        self.test_model_id = None
        
    def make_request(self, method, endpoint, data=None, token=None, params=None):
        """Make HTTP request with optional authentication."""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            return response
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return None
    
    def test_user_registration_and_login(self):
        """Test user registration and login."""
        print("\n🔐 Testing User Registration and Login...")
        
        # Test user registration
        user_data = {
            "username": "testuser",
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
            "password_confirm": TEST_USER_PASSWORD,
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = self.make_request('POST', '/users/register/', user_data)
        if response and response.status_code == 201:
            print("✅ User registration successful")
            self.test_user_id = response.json().get('user', {}).get('id')
        else:
            print(f"❌ User registration failed: {response.status_code if response else 'No response'}")
            return False
        
        # Test user login
        login_data = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
        
        response = self.make_request('POST', '/auth/login/', login_data)
        if response and response.status_code == 200:
            print("✅ User login successful")
            self.user_token = response.json().get('access')
            return True
        else:
            print(f"❌ User login failed: {response.status_code if response else 'No response'}")
            return False
    
    def test_developer_registration(self):
        """Test developer registration."""
        print("\n👨‍💻 Testing Developer Registration...")
        
        # First create a developer user
        dev_user_data = {
            "username": "developer",
            "email": TEST_DEVELOPER_EMAIL,
            "password": TEST_DEVELOPER_PASSWORD,
            "password_confirm": TEST_DEVELOPER_PASSWORD,
            "first_name": "Test",
            "last_name": "Developer"
        }
        
        response = self.make_request('POST', '/users/register/', dev_user_data)
        if not (response and response.status_code == 201):
            print("❌ Developer user creation failed")
            return False
        
        # Login as developer
        login_data = {
            "email": TEST_DEVELOPER_EMAIL,
            "password": TEST_DEVELOPER_PASSWORD
        }
        
        response = self.make_request('POST', '/auth/login/', login_data)
        if not (response and response.status_code == 200):
            print("❌ Developer login failed")
            return False
        
        self.developer_token = response.json().get('access')
        
        # Register as developer
        developer_data = {
            "developer_name": "Test Developer",
            "company_name": "Test AI Company",
            "website_url": "https://testai.com",
            "business_email": "business@testai.com",
            "specialization": ["machine_learning", "nlp"],
            "bio": "Test developer for AI models",
            "years_experience": 5
        }
        
        response = self.make_request('POST', '/developers/register/', developer_data, self.developer_token)
        if response and response.status_code == 201:
            print("✅ Developer registration successful")
            self.test_developer_id = response.json().get('developer', {}).get('id')
            return True
        else:
            print(f"❌ Developer registration failed: {response.status_code if response else 'No response'}")
            return False
    
    def test_ai_model_creation(self):
        """Test AI model creation."""
        print("\n🤖 Testing AI Model Creation...")
        
        model_data = {
            "name": "Test Chat Model",
            "description": "A test chatbot model for demonstration",
            "category": "nlp",
            "api_name": f"test_chat_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "api_endpoint": "https://api.testai.com/chat",
            "api_version": "v1",
            "tags": ["chatbot", "nlp", "test"],
            "pricing_type": "per_request",
            "price_per_request": "0.01",
            "rate_limit_per_minute": 60,
            "supported_languages": ["en", "es"],
            "is_public": True
        }
        
        response = self.make_request('POST', '/models/', model_data, self.developer_token)
        if response and response.status_code == 201:
            print("✅ AI model creation successful")
            self.test_model_id = response.json().get('id')
            return True
        else:
            print(f"❌ AI model creation failed: {response.status_code if response else 'No response'}")
            if response:
                print(f"Response: {response.text}")
            return False
    
    def test_user_history_creation(self):
        """Test user history creation."""
        print("\n📊 Testing User History Creation...")
        
        if not self.test_model_id:
            print("❌ No test model available for history creation")
            return False
        
        history_data = {
            "model": self.test_model_id,
            "session_id": f"test_session_{uuid.uuid4()}",
            "prompt": "Hello, how are you?",
            "response": "I'm doing well, thank you for asking!",
            "response_status": "success",
            "response_time_ms": 250,
            "input_tokens": 5,
            "output_tokens": 8,
            "ip_address": "127.0.0.1",
            "user_agent": "Test Client",
            "api_version": "v1"
        }
        
        response = self.make_request('POST', '/history/', history_data, self.user_token)
        if response and response.status_code == 201:
            print("✅ User history creation successful")
            return True
        else:
            print(f"❌ User history creation failed: {response.status_code if response else 'No response'}")
            if response:
                print(f"Response: {response.text}")
            return False
    
    def test_review_creation(self):
        """Test review creation."""
        print("\n⭐ Testing Review Creation...")
        
        if not self.test_model_id:
            print("❌ No test model available for review creation")
            return False
        
        review_data = {
            "model": self.test_model_id,
            "rating": 5,
            "review_title": "Excellent AI Model",
            "review_text": "This model works really well and provides accurate responses."
        }
        
        response = self.make_request('POST', '/reviews/', review_data, self.user_token)
        if response and response.status_code == 201:
            print("✅ Review creation successful")
            return True
        else:
            print(f"❌ Review creation failed: {response.status_code if response else 'No response'}")
            if response:
                print(f"Response: {response.text}")
            return False
    
    def test_list_endpoints(self):
        """Test various list endpoints."""
        print("\n📋 Testing List Endpoints...")
        
        endpoints = [
            ('/users/', 'Users'),
            ('/developers/', 'Developers'),
            ('/models/', 'AI Models'),
            ('/models/categories/', 'Model Categories'),
            ('/reviews/', 'Reviews'),
        ]
        
        success_count = 0
        for endpoint, name in endpoints:
            response = self.make_request('GET', endpoint)
            if response and response.status_code == 200:
                print(f"✅ {name} list endpoint working")
                success_count += 1
            else:
                print(f"❌ {name} list endpoint failed: {response.status_code if response else 'No response'}")
        
        return success_count == len(endpoints)
    
    def test_search_and_filter(self):
        """Test search and filter functionality."""
        print("\n🔍 Testing Search and Filter...")
        
        # Test model search
        response = self.make_request('GET', '/models/search/', params={'q': 'test'})
        if response and response.status_code == 200:
            print("✅ Model search working")
        else:
            print(f"❌ Model search failed: {response.status_code if response else 'No response'}")
        
        # Test model filtering
        response = self.make_request('GET', '/models/', params={'category': 'nlp'})
        if response and response.status_code == 200:
            print("✅ Model filtering working")
        else:
            print(f"❌ Model filtering failed: {response.status_code if response else 'No response'}")
        
        return True
    
    def test_statistics_endpoints(self):
        """Test statistics endpoints."""
        print("\n📈 Testing Statistics Endpoints...")
        
        endpoints = [
            (f'/users/{self.test_user_id}/stats/', 'User Stats', self.user_token),
            (f'/developers/{self.test_developer_id}/stats/', 'Developer Stats', self.developer_token),
            ('/history/stats/', 'History Stats', self.user_token),
        ]
        
        success_count = 0
        for endpoint, name, token in endpoints:
            if not endpoint.split('/')[2]:  # Skip if ID is None
                continue
                
            response = self.make_request('GET', endpoint, token=token)
            if response and response.status_code == 200:
                print(f"✅ {name} endpoint working")
                success_count += 1
            else:
                print(f"❌ {name} endpoint failed: {response.status_code if response else 'No response'}")
        
        return success_count > 0
    
    def test_api_documentation(self):
        """Test API documentation endpoints."""
        print("\n📚 Testing API Documentation...")
        
        # Test schema endpoint
        response = requests.get(f"{self.base_url.replace('/api/v1', '')}/api/schema/")
        if response and response.status_code == 200:
            print("✅ OpenAPI schema accessible")
        else:
            print(f"❌ OpenAPI schema failed: {response.status_code if response else 'No response'}")
        
        # Test Swagger UI
        response = requests.get(f"{self.base_url.replace('/api/v1', '')}/api/docs/")
        if response and response.status_code == 200:
            print("✅ Swagger UI accessible")
        else:
            print(f"❌ Swagger UI failed: {response.status_code if response else 'No response'}")
        
        return True
    
    def run_all_tests(self):
        """Run all API tests."""
        print("🚀 Starting AI Model Platform API Tests...")
        print(f"Base URL: {self.base_url}")
        
        tests = [
            ("User Registration and Login", self.test_user_registration_and_login),
            ("Developer Registration", self.test_developer_registration),
            ("AI Model Creation", self.test_ai_model_creation),
            ("User History Creation", self.test_user_history_creation),
            ("Review Creation", self.test_review_creation),
            ("List Endpoints", self.test_list_endpoints),
            ("Search and Filter", self.test_search_and_filter),
            ("Statistics Endpoints", self.test_statistics_endpoints),
            ("API Documentation", self.test_api_documentation),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {e}")
        
        print(f"\n📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! The API is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the output above.")
        
        return passed == total


if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
