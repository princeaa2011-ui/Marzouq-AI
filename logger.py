"""
logger.py - Advanced Logging System
نظام تسجيل متقدم - Professional Logging Infrastructure

Contains:
- Structured logging
- Multiple log handlers
- Performance tracking
- Error tracking
- Analytics integration
"""

import logging
import logging.handlers
import os
import json
import time
from datetime import datetime
from functools import wraps
from pathlib import Path


# ========================================
# Logger Setup
# ========================================

def setup_logger(name='marzouq', log_level='INFO', log_dir='logs'):
    """
    Setup advanced logger with multiple handlers
    
    Features:
    - Console output with colors
    - File rotation
    - JSON structured logging option
    - Performance tracking
    """
    
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Console Handler with colors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File Handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, 'marzouq.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Error File Handler
    error_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, 'errors.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    logger.addHandler(error_handler)
    
    # JSON Structured Log Handler (optional)
    json_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, 'structured.json'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    json_handler.setLevel(logging.INFO)
    json_handler.setFormatter(JSONFormatter())
    logger.addHandler(json_handler)
    
    return logger


# ========================================
# Custom Formatters
# ========================================

class ColoredFormatter(logging.Formatter):
    """Add colors to console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for structured logging"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add custom fields if present
        if hasattr(record, 'personality'):
            log_data['personality'] = record.personality
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'duration'):
            log_data['duration_ms'] = record.duration
        
        return json.dumps(log_data, ensure_ascii=False)


# ========================================
# Performance Tracking Decorators
# ========================================

def log_performance(func):
    """
    Decorator to log function performance
    Usage: @log_performance
    """
    logger = logging.getLogger('marzouq.performance')
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = (time.time() - start_time) * 1000  # milliseconds
            
            logger.info(
                f"Function '{func.__name__}' completed in {duration:.2f}ms",
                extra={'duration': duration, 'function': func.__name__}
            )
            
            return result
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(
                f"Function '{func.__name__}' failed after {duration:.2f}ms: {str(e)}",
                extra={'duration': duration, 'function': func.__name__},
                exc_info=True
            )
            raise
    
    return wrapper


def log_api_call(api_name):
    """
    Decorator to log external API calls
    Usage: @log_api_call('OpenAI')
    """
    def decorator(func):
        logger = logging.getLogger('marzouq.api')
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            logger.info(f"Calling {api_name} API - Function: {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                
                logger.info(
                    f"{api_name} API call successful - {duration:.2f}ms",
                    extra={'api': api_name, 'duration': duration, 'status': 'success'}
                )
                
                return result
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                logger.error(
                    f"{api_name} API call failed - {duration:.2f}ms: {str(e)}",
                    extra={'api': api_name, 'duration': duration, 'status': 'error'},
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator


# ========================================
# Conversation Logging
# ========================================

class ConversationLogger:
    """Log conversations for analytics and debugging"""
    
    def __init__(self, log_dir='logs/conversations'):
        self.log_dir = log_dir
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger('marzouq.conversation')
    
    def log_interaction(self, personality, user_input, bot_response, metadata=None):
        """Log a single conversation interaction"""
        
        interaction = {
            'timestamp': datetime.utcnow().isoformat(),
            'personality': personality,
            'user_input': user_input,
            'bot_response': bot_response,
            'metadata': metadata or {}
        }
        
        # Log to main logger
        self.logger.info(
            f"Conversation - {personality}: User said '{user_input[:50]}...'",
            extra={'personality': personality}
        )
        
        # Save to daily conversation log file
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(self.log_dir, f'conversations_{date_str}.jsonl')
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(interaction, ensure_ascii=False) + '\n')
    
    def get_conversation_history(self, date=None, personality=None):
        """Retrieve conversation history with optional filtering"""
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        log_file = os.path.join(self.log_dir, f'conversations_{date}.jsonl')
        
        if not os.path.exists(log_file):
            return []
        
        conversations = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                conv = json.loads(line)
                if personality is None or conv['personality'] == personality:
                    conversations.append(conv)
        
        return conversations


# ========================================
# Error Tracking
# ========================================

class ErrorTracker:
    """Track and analyze errors"""
    
    def __init__(self):
        self.logger = logging.getLogger('marzouq.errors')
        self.error_counts = {}
    
    def log_error(self, error_type, error_message, context=None):
        """Log and track errors"""
        
        # Increment error count
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Log the error
        self.logger.error(
            f"{error_type}: {error_message}",
            extra={'error_type': error_type, 'context': context or {}}
        )
    
    def get_error_stats(self):
        """Get error statistics"""
        return {
            'total_errors': sum(self.error_counts.values()),
            'by_type': self.error_counts
        }


# ========================================
# Analytics Logger
# ========================================

class AnalyticsLogger:
    """Log events for analytics"""
    
    def __init__(self, log_dir='logs/analytics'):
        self.log_dir = log_dir
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger('marzouq.analytics')
    
    def log_event(self, event_type, event_data):
        """Log an analytics event"""
        
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'data': event_data
        }
        
        self.logger.info(f"Event: {event_type}", extra={'event': event_type})
        
        # Save to daily analytics file
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(self.log_dir, f'analytics_{date_str}.jsonl')
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
    
    def track_personality_usage(self, personality):
        """Track which personalities are being used"""
        self.log_event('personality_selected', {'personality': personality})
    
    def track_feature_usage(self, feature):
        """Track which features are being used"""
        self.log_event('feature_used', {'feature': feature})
    
    def track_api_call(self, api_name, success=True):
        """Track external API calls"""
        self.log_event('api_call', {'api': api_name, 'success': success})


# ========================================
# Initialize Global Loggers
# ========================================

# Main application logger
main_logger = setup_logger('marzouq', 'INFO')

# Specialized loggers
conversation_logger = ConversationLogger()
error_tracker = ErrorTracker()
analytics_logger = AnalyticsLogger()


# ========================================
# Helper Functions
# ========================================

def log_info(message, **kwargs):
    """Quick info logging"""
    main_logger.info(message, extra=kwargs)


def log_warning(message, **kwargs):
    """Quick warning logging"""
    main_logger.warning(message, extra=kwargs)


def log_error(message, **kwargs):
    """Quick error logging"""
    main_logger.error(message, extra=kwargs)
    error_tracker.log_error(kwargs.get('error_type', 'general'), message, kwargs)


def log_debug(message, **kwargs):
    """Quick debug logging"""
    main_logger.debug(message, extra=kwargs)


# ========================================
# Export
# ========================================

__all__ = [
    'setup_logger',
    'log_performance',
    'log_api_call',
    'ConversationLogger',
    'ErrorTracker',
    'AnalyticsLogger',
    'main_logger',
    'conversation_logger',
    'error_tracker',
    'analytics_logger',
    'log_info',
    'log_warning',
    'log_error',
    'log_debug'
]


if __name__ == "__main__":
    # Test the logging system
    print("🔍 Testing Marzouq Logging System\n")
    
    log_info("Application started")
    log_debug("Debug information", component='test')
    log_warning("Warning message", severity='medium')
    log_error("Error occurred", error_type='test_error')
    
    # Test conversation logging
    conversation_logger.log_interaction(
        personality='najdi',
        user_input='مرحبا يا مرزوق',
        bot_response='مرحبا كيفك معاك مرزوق',
        metadata={'language': 'ar'}
    )
    
    # Test analytics
    analytics_logger.track_personality_usage('najdi')
    analytics_logger.track_feature_usage('voice_call')
    
    print("\n✅ Logging system test complete")
    print(f"📊 Error stats: {error_tracker.get_error_stats()}")
