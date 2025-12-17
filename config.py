"""
config.py - Advanced Configuration Management
إعدادات متقدمة للمشروع - Professional Configuration System

Contains:
- Environment configuration
- API keys management
- Feature flags
- Performance settings
- Caching configuration
- Rate limiting
- Logging configuration
"""

import os
from dotenv import load_dotenv
from datetime import timedelta

# تحميل المتغيرات البيئية - Load environment variables
load_dotenv()


# ========================================
# Application Settings
# ========================================

class Config:
    """Base configuration class"""
    
    # Flask Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = False
    
    # Server Settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Session Configuration
    SESSION_COOKIE_SECURE = True  # HTTPS only in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # CORS Settings
    CORS_ENABLED = os.getenv('CORS_ENABLED', 'True').lower() == 'true'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True


# ========================================
# API Keys & External Services
# ========================================

class APIConfig:
    """API keys and external service configuration"""
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')
    TWILIO_TWIML_APP_SID = os.getenv('TWILIO_TWIML_APP_SID', '')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.8'))
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '500'))
    
    # Google AI Configuration (Gemini, Veo)
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-3-pro')
    VEO_MODEL = os.getenv('VEO_MODEL', 'veo-3')
    
    # Grok AI Configuration (for Adriana's selfies)
    GROK_API_KEY = os.getenv('GROK_API_KEY', '')
    GROK_IMAGE_MODEL = os.getenv('GROK_IMAGE_MODEL', 'grok-image-2')
    
    # Nanobanana AI Configuration (for image editing)
    NANOBANANA_API_KEY = os.getenv('NANOBANANA_API_KEY', '')
    
    # Google Custom Search (for Lopez's soccer data)
    GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY', '')
    GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')


# ========================================
# Feature Flags - Advanced Feature Control
# ========================================

class FeatureFlags:
    """Control features dynamically without code changes"""
    
    # Core Features
    VOICE_CALLING_ENABLED = os.getenv('VOICE_CALLING_ENABLED', 'True').lower() == 'true'
    CHAT_ENABLED = os.getenv('CHAT_ENABLED', 'True').lower() == 'true'
    
    # AI Features
    CHATGPT_INTEGRATION = os.getenv('CHATGPT_INTEGRATION', 'True').lower() == 'true'
    GEMINI_INTEGRATION = os.getenv('GEMINI_INTEGRATION', 'False').lower() == 'true'
    GROK_IMAGE_GEN = os.getenv('GROK_IMAGE_GEN', 'False').lower() == 'true'
    VEO_VIDEO_GEN = os.getenv('VEO_VIDEO_GEN', 'False').lower() == 'true'
    
    # Personality Features
    ADRIANA_SELFIE_GEN = os.getenv('ADRIANA_SELFIE_GEN', 'True').lower() == 'true'
    LOPEZ_SOCCER_SEARCH = os.getenv('LOPEZ_SOCCER_SEARCH', 'True').lower() == 'true'
    MATT_DOCUMENT_AI = os.getenv('MATT_DOCUMENT_AI', 'True').lower() == 'true'
    
    # Advanced Features
    PERSONALITY_CALLING = os.getenv('PERSONALITY_CALLING', 'True').lower() == 'true'
    PHONE_NUMBER_CREATOR = os.getenv('PHONE_NUMBER_CREATOR', 'True').lower() == 'true'
    IPHONE_DIALER = os.getenv('IPHONE_DIALER', 'True').lower() == 'true'
    
    # Security Features
    RATE_LIMITING = os.getenv('RATE_LIMITING', 'True').lower() == 'true'
    SENSITIVE_DATA_BLOCKING = os.getenv('SENSITIVE_DATA_BLOCKING', 'True').lower() == 'true'
    CONTENT_FILTERING = os.getenv('CONTENT_FILTERING', 'True').lower() == 'true'


# ========================================
# Performance & Caching
# ========================================

class PerformanceConfig:
    """Performance optimization settings"""
    
    # Caching
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')  # simple, redis, memcached
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '300'))  # 5 minutes
    CACHE_KEY_PREFIX = 'marzouq_'
    
    # Redis Configuration (if using Redis cache)
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    
    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per hour')
    
    # API Rate Limits
    OPENAI_RATE_LIMIT = '50 per minute'
    GOOGLE_RATE_LIMIT = '100 per minute'
    TWILIO_RATE_LIMIT = '1000 per hour'
    
    # Connection Pooling
    MAX_DB_CONNECTIONS = int(os.getenv('MAX_DB_CONNECTIONS', '20'))
    CONNECTION_TIMEOUT = int(os.getenv('CONNECTION_TIMEOUT', '30'))
    
    # Request Timeouts
    API_REQUEST_TIMEOUT = int(os.getenv('API_REQUEST_TIMEOUT', '30'))
    TWILIO_REQUEST_TIMEOUT = int(os.getenv('TWILIO_REQUEST_TIMEOUT', '10'))


# ========================================
# Logging Configuration
# ========================================

class LoggingConfig:
    """Advanced logging configuration"""
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.getenv('LOG_FILE', 'logs/marzouq.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', '10485760'))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '5'))
    
    # Structured Logging
    STRUCTURED_LOGGING = os.getenv('STRUCTURED_LOGGING', 'False').lower() == 'true'
    LOG_JSON_FORMAT = os.getenv('LOG_JSON_FORMAT', 'False').lower() == 'true'
    
    # Log to External Services
    LOG_TO_CLOUDWATCH = os.getenv('LOG_TO_CLOUDWATCH', 'False').lower() == 'true'
    LOG_TO_DATADOG = os.getenv('LOG_TO_DATADOG', 'False').lower() == 'true'


# ========================================
# Personality Configuration
# ========================================

class PersonalityConfig:
    """Configuration for each personality"""
    
    # Default personality
    DEFAULT_PERSONALITY = os.getenv('DEFAULT_PERSONALITY', 'najdi')
    
    # Personality-specific settings
    PERSONALITIES = {
        'najdi': {
            'enabled': True,
            'model': 'gpt-4',
            'temperature': 0.8,
            'max_tokens': 500,
            'features': ['finance', 'investment', 'sarcasm']
        },
        'hijazi': {
            'enabled': True,
            'model': 'gpt-4',
            'temperature': 0.9,
            'max_tokens': 600,
            'features': ['rap', 'music', 'fun']
        },
        'egyptian': {
            'enabled': True,
            'model': 'gpt-4',
            'temperature': 0.8,
            'max_tokens': 600,
            'features': ['problem_solving', 'mechanics', 'price_comparison']
        },
        'northern': {
            'enabled': True,
            'model': 'gpt-4',
            'temperature': 0.7,
            'max_tokens': 700,
            'features': ['poetry', 'history', 'wisdom']
        },
        'jordanian': {
            'enabled': True,
            'model': 'gpt-4',
            'temperature': 0.8,
            'max_tokens': 500,
            'features': ['wit', 'sarcasm']
        },
        'southern': {
            'enabled': True,
            'model': 'gpt-4',
            'temperature': 0.7,
            'max_tokens': 500,
            'features': ['traditional', 'calm']
        },
        'iraqi': {
            'enabled': True,
            'model': 'gpt-4',
            'temperature': 0.8,
            'max_tokens': 500,
            'features': ['hospitality', 'friendly']
        },
        'american': {  # Matt
            'enabled': True,
            'model': 'gpt-4',
            'temperature': 0.7,
            'max_tokens': 800,
            'features': ['cv_creation', 'document_analysis', 'image_ai', 'video_gen']
        },
        'ebonics': {  # Danso
            'enabled': True,
            'model': 'gpt-4',
            'temperature': 0.9,
            'max_tokens': 500,
            'features': ['street_culture']
        },
        'latina': {  # Adriana
            'enabled': True,
            'model': 'gpt-4',
            'temperature': 0.9,
            'max_tokens': 600,
            'features': ['fashion', 'beauty', 'image_gen', 'grok_selfies']
        },
        'latino': {  # Lopez
            'enabled': True,
            'model': ['gpt-4', 'gemini-3'],  # Multi-model support
            'temperature': 0.7,
            'max_tokens': 700,
            'features': ['math', 'science', 'soccer', 'spanish_teaching', 'google_search']
        }
    }
    
    # Adriana-specific settings
    ADRIANA_SELFIE_PROBABILITY = float(os.getenv('ADRIANA_SELFIE_PROBABILITY', '0.10'))
    ADRIANA_GROK_MODEL = os.getenv('ADRIANA_GROK_MODEL', 'grok-image-2')
    
    # Lopez-specific settings
    LOPEZ_GOOGLE_SEARCH_ENABLED = os.getenv('LOPEZ_GOOGLE_SEARCH', 'True').lower() == 'true'
    LOPEZ_SOCCER_API_KEY = os.getenv('LOPEZ_SOCCER_API_KEY', '')


# ========================================
# Security Configuration
# ========================================

class SecurityConfig:
    """Security settings"""
    
    # Content Security
    MAX_INPUT_LENGTH = int(os.getenv('MAX_INPUT_LENGTH', '1000'))
    MIN_INPUT_LENGTH = int(os.getenv('MIN_INPUT_LENGTH', '1'))
    
    # Sensitive Data Patterns
    BLOCK_OTP_REQUESTS = os.getenv('BLOCK_OTP_REQUESTS', 'True').lower() == 'true'
    BLOCK_PASSWORD_REQUESTS = os.getenv('BLOCK_PASSWORD_REQUESTS', 'True').lower() == 'true'
    BLOCK_BANK_INFO = os.getenv('BLOCK_BANK_INFO', 'True').lower() == 'true'
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', '60'))
    MAX_REQUESTS_PER_HOUR = int(os.getenv('MAX_REQUESTS_PER_HOUR', '1000'))
    
    # IP Blocking
    BLOCKED_IPS = os.getenv('BLOCKED_IPS', '').split(',')
    ALLOWED_IPS = os.getenv('ALLOWED_IPS', '').split(',')
    
    # HTTPS
    FORCE_HTTPS = os.getenv('FORCE_HTTPS', 'True').lower() == 'true'
    
    # CSRF Protection
    CSRF_ENABLED = os.getenv('CSRF_ENABLED', 'True').lower() == 'true'


# ========================================
# Database Configuration (for future expansion)
# ========================================

class DatabaseConfig:
    """Database configuration for analytics and logging"""
    
    # PostgreSQL
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'marzouq')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'marzouq_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
    
    # MongoDB (for conversation history)
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/marzouq')
    
    # SQLite (for development)
    SQLITE_DB = os.getenv('SQLITE_DB', 'marzouq.db')


# ========================================
# Analytics Configuration
# ========================================

class AnalyticsConfig:
    """Analytics and monitoring configuration"""
    
    # Google Analytics
    GA_TRACKING_ID = os.getenv('GA_TRACKING_ID', '')
    
    # Custom Analytics
    TRACK_CONVERSATIONS = os.getenv('TRACK_CONVERSATIONS', 'True').lower() == 'true'
    TRACK_PERSONALITY_USAGE = os.getenv('TRACK_PERSONALITY_USAGE', 'True').lower() == 'true'
    TRACK_FEATURE_USAGE = os.getenv('TRACK_FEATURE_USAGE', 'True').lower() == 'true'
    
    # Metrics
    COLLECT_METRICS = os.getenv('COLLECT_METRICS', 'True').lower() == 'true'
    METRICS_INTERVAL = int(os.getenv('METRICS_INTERVAL', '60'))  # seconds


# ========================================
# Environment Selection
# ========================================

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig


# ========================================
# Configuration Validation
# ========================================

def validate_config():
    """Validate configuration and warn about missing settings"""
    warnings = []
    
    # Check critical API keys
    if not APIConfig.OPENAI_API_KEY and FeatureFlags.CHATGPT_INTEGRATION:
        warnings.append("⚠️ OpenAI API key not set - ChatGPT features will not work")
    
    if not APIConfig.TWILIO_ACCOUNT_SID and FeatureFlags.VOICE_CALLING_ENABLED:
        warnings.append("⚠️ Twilio credentials not set - Voice calling will not work")
    
    if not APIConfig.GOOGLE_API_KEY and FeatureFlags.GEMINI_INTEGRATION:
        warnings.append("⚠️ Google API key not set - Gemini features will not work")
    
    if not APIConfig.GROK_API_KEY and FeatureFlags.ADRIANA_SELFIE_GEN:
        warnings.append("⚠️ Grok API key not set - Adriana selfie generation will not work")
    
    return warnings


# ========================================
# Export Current Configuration
# ========================================

current_config = get_config()
config_warnings = validate_config()


if __name__ == "__main__":
    print("🔧 Marzouq Configuration System")
    print("=" * 50)
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Debug Mode: {current_config.DEBUG}")
    print(f"Host: {current_config.HOST}:{current_config.PORT}")
    print("\n📋 Feature Flags:")
    print(f"  - Voice Calling: {FeatureFlags.VOICE_CALLING_ENABLED}")
    print(f"  - ChatGPT: {FeatureFlags.CHATGPT_INTEGRATION}")
    print(f"  - Gemini: {FeatureFlags.GEMINI_INTEGRATION}")
    print(f"  - Adriana Selfies: {FeatureFlags.ADRIANA_SELFIE_GEN}")
    print(f"  - Lopez Soccer Search: {FeatureFlags.LOPEZ_SOCCER_SEARCH}")
    
    if config_warnings:
        print("\n⚠️ Configuration Warnings:")
        for warning in config_warnings:
            print(f"  {warning}")
    else:
        print("\n✅ Configuration is valid!")
