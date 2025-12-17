"""
api_manager.py - Advanced API Integration Manager
مدير API متقدم - Professional API Management System

Contains:
- Unified API client for all external services
- Rate limiting and retry logic
- Caching layer
- Error handling
- Response validation
"""

import time
import requests
from functools import wraps
from typing import Dict, Any, Optional, List
import json
from datetime import datetime, timedelta

try:
    from config import APIConfig, PerformanceConfig, FeatureFlags
    from logger import log_api_call, log_error, log_warning, log_info
except ImportError:
    # Fallback for standalone testing
    class APIConfig:
        OPENAI_API_KEY = ''
        GOOGLE_API_KEY = ''
        GROK_API_KEY = ''
    class PerformanceConfig:
        API_REQUEST_TIMEOUT = 30
    class FeatureFlags:
        CHATGPT_INTEGRATION = True


# ========================================
# Base API Client
# ========================================

class BaseAPIClient:
    """Base class for all API clients"""
    
    def __init__(self, api_name: str, base_url: str, api_key: str, timeout: int = 30):
        self.api_name = api_name
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.cache = {}
        self.rate_limiter = RateLimiter()
    
    def _make_request(self, method: str, endpoint: str, **kwargs):
        """Make HTTP request with error handling and retries"""
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = kwargs.pop('headers', {})
        
        # Add API key to headers
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        # Rate limiting
        self.rate_limiter.wait_if_needed(self.api_name)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    timeout=self.timeout,
                    **kwargs
                )
                
                response.raise_for_status()
                return response.json() if response.content else {}
                
            except requests.exceptions.Timeout:
                log_warning(f"{self.api_name} API timeout (attempt {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except requests.exceptions.HTTPError as e:
                log_error(f"{self.api_name} API HTTP error: {e}", error_type='api_error')
                raise
                
            except Exception as e:
                log_error(f"{self.api_name} API error: {e}", error_type='api_error')
                raise
    
    def get(self, endpoint: str, **kwargs):
        """GET request"""
        return self._make_request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs):
        """POST request"""
        return self._make_request('POST', endpoint, **kwargs)


# ========================================
# Rate Limiter
# ========================================

class RateLimiter:
    """Simple rate limiter to prevent API overuse"""
    
    def __init__(self):
        self.call_times = {}
        self.limits = {
            'openai': {'calls': 50, 'period': 60},      # 50 calls per minute
            'google': {'calls': 100, 'period': 60},     # 100 calls per minute
            'grok': {'calls': 30, 'period': 60},        # 30 calls per minute
            'nanobanana': {'calls': 20, 'period': 60},  # 20 calls per minute
        }
    
    def wait_if_needed(self, api_name: str):
        """Wait if rate limit is exceeded"""
        
        api_key = api_name.lower()
        if api_key not in self.limits:
            return
        
        limit = self.limits[api_key]
        now = time.time()
        
        # Initialize call times if not exists
        if api_key not in self.call_times:
            self.call_times[api_key] = []
        
        # Remove old call times outside the period
        self.call_times[api_key] = [
            t for t in self.call_times[api_key]
            if now - t < limit['period']
        ]
        
        # Check if limit is reached
        if len(self.call_times[api_key]) >= limit['calls']:
            oldest_call = self.call_times[api_key][0]
            wait_time = limit['period'] - (now - oldest_call)
            if wait_time > 0:
                log_warning(f"Rate limit reached for {api_name}, waiting {wait_time:.1f}s")
                time.sleep(wait_time)
        
        # Record this call
        self.call_times[api_key].append(now)


# ========================================
# OpenAI API Client
# ========================================

class OpenAIClient(BaseAPIClient):
    """Client for OpenAI ChatGPT API"""
    
    def __init__(self):
        super().__init__(
            api_name='OpenAI',
            base_url='https://api.openai.com/v1',
            api_key=APIConfig.OPENAI_API_KEY,
            timeout=PerformanceConfig.API_REQUEST_TIMEOUT
        )
    
    @log_api_call('OpenAI')
    def chat_completion(self, messages: List[Dict], model: str = 'gpt-4',
                       temperature: float = 0.8, max_tokens: int = 500, **kwargs):
        """Create a chat completion"""
        
        payload = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
            **kwargs
        }
        
        try:
            response = self.post('chat/completions', json=payload)
            return {
                'success': True,
                'response': response['choices'][0]['message']['content'],
                'usage': response.get('usage', {}),
                'model': response.get('model', model)
            }
        except Exception as e:
            log_error(f"OpenAI chat completion failed: {e}", error_type='openai_error')
            return {
                'success': False,
                'error': str(e),
                'response': "عذراً، حدث خطأ في الاتصال بالخدمة. حاول مرة أخرى."
            }


# ========================================
# Google Gemini API Client
# ========================================

class GeminiClient(BaseAPIClient):
    """Client for Google Gemini API"""
    
    def __init__(self):
        super().__init__(
            api_name='Gemini',
            base_url='https://generativelanguage.googleapis.com/v1beta',
            api_key=APIConfig.GOOGLE_API_KEY,
            timeout=PerformanceConfig.API_REQUEST_TIMEOUT
        )
    
    @log_api_call('Gemini')
    def generate_content(self, prompt: str, model: str = 'gemini-pro', **kwargs):
        """Generate content using Gemini"""
        
        payload = {
            'contents': [{
                'parts': [{'text': prompt}]
            }],
            **kwargs
        }
        
        try:
            endpoint = f'models/{model}:generateContent?key={self.api_key}'
            response = self.post(endpoint, json=payload)
            
            return {
                'success': True,
                'response': response['candidates'][0]['content']['parts'][0]['text'],
                'model': model
            }
        except Exception as e:
            log_error(f"Gemini generation failed: {e}", error_type='gemini_error')
            return {
                'success': False,
                'error': str(e),
                'response': "عذراً، حدث خطأ في الاتصال بخدمة Gemini."
            }
    
    @log_api_call('Gemini')
    def analyze_image(self, image_data: str, prompt: str, model: str = 'gemini-pro-vision'):
        """Analyze image using Gemini Vision"""
        
        payload = {
            'contents': [{
                'parts': [
                    {'text': prompt},
                    {'inline_data': {'mime_type': 'image/jpeg', 'data': image_data}}
                ]
            }]
        }
        
        try:
            endpoint = f'models/{model}:generateContent?key={self.api_key}'
            response = self.post(endpoint, json=payload)
            
            return {
                'success': True,
                'analysis': response['candidates'][0]['content']['parts'][0]['text'],
                'model': model
            }
        except Exception as e:
            log_error(f"Gemini image analysis failed: {e}", error_type='gemini_error')
            return {
                'success': False,
                'error': str(e)
            }


# ========================================
# Grok AI Client (for Adriana's selfies)
# ========================================

class GrokClient(BaseAPIClient):
    """Client for Grok AI Image Generation"""
    
    def __init__(self):
        super().__init__(
            api_name='Grok',
            base_url='https://api.x.ai/v1',  # TODO: Replace with actual Grok API URL when available
            api_key=APIConfig.GROK_API_KEY,
            timeout=60  # Image generation takes longer
        )
    
    @log_api_call('Grok')
    def generate_image(self, prompt: str, **kwargs):
        """Generate image using Grok AI"""
        
        payload = {
            'prompt': prompt,
            'model': 'grok-image-2',
            **kwargs
        }
        
        try:
            response = self.post('images/generate', json=payload)
            
            return {
                'success': True,
                'image_url': response.get('data', [{}])[0].get('url'),
                'prompt': prompt,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            log_error(f"Grok image generation failed: {e}", error_type='grok_error')
            return {
                'success': False,
                'error': str(e)
            }


# ========================================
# Google Custom Search Client (for Lopez)
# ========================================

class GoogleSearchClient(BaseAPIClient):
    """Client for Google Custom Search API"""
    
    def __init__(self):
        super().__init__(
            api_name='GoogleSearch',
            base_url='https://www.googleapis.com/customsearch/v1',
            api_key=APIConfig.GOOGLE_SEARCH_API_KEY,
            timeout=10
        )
        self.search_engine_id = APIConfig.GOOGLE_SEARCH_ENGINE_ID
    
    @log_api_call('GoogleSearch')
    def search_soccer_info(self, query: str, num_results: int = 5):
        """Search for soccer-related information"""
        
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': num_results
        }
        
        try:
            response = self.get('', params=params)
            
            results = []
            for item in response.get('items', []):
                results.append({
                    'title': item.get('title'),
                    'snippet': item.get('snippet'),
                    'link': item.get('link')
                })
            
            return {
                'success': True,
                'results': results,
                'query': query
            }
        except Exception as e:
            log_error(f"Google search failed: {e}", error_type='search_error')
            return {
                'success': False,
                'error': str(e),
                'results': []
            }


# ========================================
# Unified API Manager
# ========================================

class APIManager:
    """Unified manager for all API clients"""
    
    def __init__(self):
        self.openai = OpenAIClient() if FeatureFlags.CHATGPT_INTEGRATION else None
        self.gemini = GeminiClient() if FeatureFlags.GEMINI_INTEGRATION else None
        self.grok = GrokClient() if FeatureFlags.GROK_IMAGE_GEN else None
        self.google_search = GoogleSearchClient() if FeatureFlags.LOPEZ_SOCCER_SEARCH else None
        
        log_info("API Manager initialized")
    
    def get_chat_response(self, personality: str, messages: List[Dict], **kwargs):
        """Get chat response from appropriate AI model"""
        
        # Use Gemini for Lopez if enabled
        if personality == 'latino' and self.gemini and FeatureFlags.GEMINI_INTEGRATION:
            # Convert messages to single prompt for Gemini
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            return self.gemini.generate_content(prompt, **kwargs)
        
        # Default to OpenAI
        if self.openai:
            return self.openai.chat_completion(messages, **kwargs)
        
        return {
            'success': False,
            'error': 'No AI service configured',
            'response': 'عذراً، الخدمة غير متاحة حالياً.'
        }
    
    def generate_adriana_selfie(self, prompt: str):
        """Generate Adriana's selfie using Grok AI"""
        
        if self.grok and FeatureFlags.ADRIANA_SELFIE_GEN:
            return self.grok.generate_image(prompt)
        
        return {
            'success': False,
            'error': 'Grok AI not configured'
        }
    
    def search_soccer_data(self, query: str):
        """Search for soccer data using Google"""
        
        if self.google_search and FeatureFlags.LOPEZ_SOCCER_SEARCH:
            return self.google_search.search_soccer_info(query)
        
        return {
            'success': False,
            'error': 'Google Search not configured',
            'results': []
        }
    
    def analyze_image(self, image_data: str, prompt: str):
        """Analyze image using Gemini Vision"""
        
        if self.gemini:
            return self.gemini.analyze_image(image_data, prompt)
        
        return {
            'success': False,
            'error': 'Image analysis not available'
        }


# ========================================
# Singleton Instance
# ========================================

api_manager = APIManager()


# ========================================
# Helper Functions
# ========================================

def get_ai_response(personality: str, conversation_history: List[Dict], **kwargs):
    """Helper to get AI response"""
    return api_manager.get_chat_response(personality, conversation_history, **kwargs)


def generate_image(prompt: str):
    """Helper to generate image"""
    return api_manager.generate_adriana_selfie(prompt)


def search_soccer(query: str):
    """Helper to search soccer info"""
    return api_manager.search_soccer_data(query)


# ========================================
# Export
# ========================================

__all__ = [
    'APIManager',
    'OpenAIClient',
    'GeminiClient',
    'GrokClient',
    'GoogleSearchClient',
    'api_manager',
    'get_ai_response',
    'generate_image',
    'search_soccer'
]


if __name__ == "__main__":
    print("🔌 Testing API Manager\n")
    
    manager = APIManager()
    
    print(f"OpenAI Client: {'✅' if manager.openai else '❌'}")
    print(f"Gemini Client: {'✅' if manager.gemini else '❌'}")
    print(f"Grok Client: {'✅' if manager.grok else '❌'}")
    print(f"Google Search: {'✅' if manager.google_search else '❌'}")
    
    print("\n✅ API Manager ready!")
