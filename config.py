"""
Configuration management for JamaAlca application
This file holds all the settings and API keys that the app needs to work
Think of this as the app's settings file - it tells the app where to find things and how to behave
"""

import os

# Try to load environment variables from .env file if dotenv is available
# This lets us keep sensitive information like API keys in a separate file
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load variables from .env file if it exists
except ImportError:
    # If dotenv is not available, we'll just use environment variables directly
    # This means the app can still work even without the dotenv package
    pass

class Config:
    """
    Configuration class for JamaAlca application
    This is like a settings menu where all the app's options are stored
    You can change these values to make the app behave differently
    """
    
    # ===== AZURE OPENAI SETTINGS =====
    # These settings control how the app talks to Microsoft's AI service
    # This is what makes the app smart - it can give advice about farming
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://aihubstarbucks3126937967.cognitiveservices.azure.com/')
    AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY', 'CzUXl0GKZIRwS0aoZJzgapKotKKFUefg05xVIUnSsEWemH4FB6PfJQQJ99ALACfhMk5XJ3w3AAAAACOGokTd')
    DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME', 'ja-students-gpt-5-chat')
    
    # ===== AZURE VISION SETTINGS =====
    # These settings control the image recognition feature
    # This is what lets the app look at photos of plants and tell you what's wrong
    AZURE_VISION_ENDPOINT = os.getenv('AZURE_VISION_ENDPOINT', 'https://southcentralus.api.cognitive.microsoft.com/')
    AZURE_VISION_PREDICTION_KEY = os.getenv('AZURE_VISION_PREDICTION_KEY', '90ca8ee92dd24300a83bacd04f5ad06c')
    AZURE_VISION_PROJECT_ID = os.getenv('AZURE_VISION_PROJECT_ID', '2c93ae6d-150e-429a-ad9c-d2b605d02e65')
    AZURE_VISION_PUBLISHED_NAME = os.getenv('AZURE_VISION_PUBLISHED_NAME', 'JamaAlca Vision')
    
    # ===== DATABASE SETTINGS =====
    # This is where the app stores information about farms, crops, and users
    # Right now it's empty, but later we'll connect to Azure SQL database
    DATABASE_CONNECTION_STRING = os.getenv('DATABASE_CONNECTION_STRING', '')
    
    # ===== NOTIFICATION SETTINGS =====
    # These control how the app sends alerts and messages to farmers
    # Like text messages when there's a problem with crops
    AZURE_NOTIFICATION_HUB_CONNECTION_STRING = os.getenv('AZURE_NOTIFICATION_HUB_CONNECTION_STRING', '')
    AZURE_COMMUNICATION_SERVICES_CONNECTION_STRING = os.getenv('AZURE_COMMUNICATION_SERVICES_CONNECTION_STRING', '')
    
    # ===== API MANAGEMENT SETTINGS =====
    # These control how the app talks to other services securely
    # Like a security guard that checks who's allowed to use the app
    API_BASE_URL = os.getenv('API_BASE_URL', '')
    API_SUBSCRIPTION_KEY = os.getenv('API_SUBSCRIPTION_KEY', '')
    
    # ===== APP BEHAVIOR SETTINGS =====
    # These control how the app behaves - you can change these to test different things
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'  # Set to True to see more detailed error messages
    USE_REAL_DATA = os.getenv('USE_REAL_DATA', 'True').lower() == 'true'  # Set to False to use fake data for testing
