"""
utils.py - أدوات مساعدة
Utility Functions for Marzouq

يحتوي على:
- كشف اللغة
- أدوات النصوص
- دوال مساعدة عامة
"""

import re


# ========================================
# كشف اللغة - Language Detection
# ========================================

def detect_language(text):
    """
    كشف لغة النص (عربي، إنجليزي)
    Detect text language (Arabic, English)
    
    Args:
        text (str): النص المراد فحصه
        
    Returns:
        str: "arabic", "english", أو "unknown"
    """
    if not text:
        return "unknown"
    
    # فحص الأحرف العربية
    arabic_chars = re.findall(r'[\u0600-\u06FF]', text)
    # فحص الأحرف الإنجليزية
    english_chars = re.findall(r'[a-zA-Z]', text)
    
    arabic_count = len(arabic_chars)
    english_count = len(english_chars)
    
    if arabic_count > english_count:
        return "arabic"
    elif english_count > arabic_count:
        return "english"
    else:
        return "unknown"


def is_saudi_dialect(text):
    """
    محاولة تحديد إذا كان النص بلهجة سعودية
    Try to detect if text is in Saudi dialect
    
    Args:
        text (str): النص
        
    Returns:
        bool: احتمالية كون النص سعودي
    """
    if not text:
        return False
    
    text_lower = text.lower()
    
    # كلمات وعبارات سعودية شائعة
    saudi_indicators = [
        "وش", "ايش", "كيفك", "زين", "تمام",
        "يالله", "ياخي", "ياهو", "عيل", "مدري",
        "والله", "ماشاء الله", "ان شاء الله",
        "حلو", "زي", "قلت", "شلون", "شسمك"
    ]
    
    for indicator in saudi_indicators:
        if indicator in text_lower:
            return True
    
    return False


# ========================================
# أدوات النصوص - Text Utilities
# ========================================

def truncate_text(text, max_length=100):
    """
    قص النص مع إضافة نقاط
    Truncate text with ellipsis
    
    Args:
        text (str): النص
        max_length (int): الحد الأقصى
        
    Returns:
        str: النص المقصوص
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def contains_question(text):
    """
    التحقق من وجود سؤال في النص
    Check if text contains a question
    
    Args:
        text (str): النص
        
    Returns:
        bool: هل يحتوي على سؤال؟
    """
    if not text:
        return False
    
    # علامات الاستفهام
    question_marks = ['؟', '?']
    
    # كلمات استفهام عربية
    question_words = [
        'كيف', 'ليش', 'وش', 'ايش', 'متى',
        'وين', 'من', 'ماذا', 'هل', 'شلون'
    ]
    
    # فحص علامات الاستفهام
    for mark in question_marks:
        if mark in text:
            return True
    
    # فحص كلمات الاستفهام
    text_lower = text.lower()
    for word in question_words:
        if word in text_lower:
            return True
    
    return False


def get_response_length(text):
    """
    حساب طول الرد المناسب
    Calculate appropriate response length
    
    Args:
        text (str): النص المدخل
        
    Returns:
        str: "short", "medium", "long"
    """
    if not text:
        return "short"
    
    length = len(text.split())
    
    if length <= 5:
        return "short"
    elif length <= 15:
        return "medium"
    else:
        return "long"


# ========================================
# دوال مساعدة Twilio - Twilio Helpers
# ========================================

def format_for_speech(text):
    """
    تنسيق النص ليكون أفضل للنطق
    Format text for better speech output
    
    Args:
        text (str): النص الأصلي
        
    Returns:
        str: النص المنسق
    """
    if not text:
        return ""
    
    # إزالة الإيموجي (قد تسبب مشاكل في TTS)
    # Remove emojis (may cause issues in TTS)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        "]+", flags=re.UNICODE)
    
    cleaned = emoji_pattern.sub(r'', text)
    
    # إزالة المسافات المتعددة
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    return cleaned.strip()


def get_voice_settings(language):
    """
    الحصول على إعدادات الصوت حسب اللغة
    Get voice settings based on language
    
    Args:
        language (str): اللغة ("arabic" أو "english")
        
    Returns:
        dict: إعدادات الصوت
    """
    if language == "english":
        return {
            "voice": "Polly.Joanna",
            "language": "en-US"
        }
    else:  # Arabic (default)
        return {
            "voice": "Polly.Zeina",
            "language": "ar-SA"
        }


# ========================================
# التسجيل والتتبع - Logging & Tracking
# ========================================

def log_interaction(caller_number, user_input, bot_response):
    """
    تسجيل التفاعل (للتطوير والتحليل)
    Log interaction (for development and analysis)
    
    Args:
        caller_number (str): رقم المتصل
        user_input (str): مدخلات المستخدم
        bot_response (str): رد البوت
    """
    # في الإنتاج، يمكن حفظ هذا في قاعدة بيانات
    # In production, this can be saved to a database
    
    print(f"""
    📞 تفاعل جديد - New Interaction
    -----------------------------------
    المتصل: {caller_number or 'غير معروف'}
    المدخل: {truncate_text(user_input, 50)}
    الرد: {truncate_text(bot_response, 50)}
    اللغة: {detect_language(user_input)}
    -----------------------------------
    """)


if __name__ == "__main__":
    # اختبار الأدوات - Test utilities
    print("🛠️ اختبار الأدوات المساعدة - Testing Utilities\n")
    
    test_texts = [
        "مرحبا كيف حالك؟",
        "Hello, how are you?",
        "وش اخبارك يا مرزوق؟",
        "This is a test message"
    ]
    
    for text in test_texts:
        lang = detect_language(text)
        is_q = contains_question(text)
        is_saudi = is_saudi_dialect(text)
        print(f"نص: {text}")
        print(f"  اللغة: {lang}, سؤال: {is_q}, سعودي: {is_saudi}\n")
