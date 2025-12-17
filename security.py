"""
security.py - الأمان وحماية الاستخدام
Security and Usage Protection for Marzouq

يحتوي على:
- كشف المحتوى الحساس
- منع طلبات OTP وكلمات المرور
- حماية من الاستخدام المسيء
"""

import re


# ========================================
# الكلمات والعبارات المحظورة
# Forbidden Keywords and Phrases
# ========================================

# كلمات تشير إلى طلب معلومات حساسة
SENSITIVE_KEYWORDS = {
    "arabic": [
        "otp", "رمز", "كود", "تحقق", "تأكيد",
        "كلمة مرور", "كلمة سر", "باسورد", "password",
        "رقم سري", "بطاقة", "كريديت", "credit card",
        "حساب بنكي", "بنك", "bank", "فيزا", "visa",
        "ماستركارد", "mastercard", "cvv", "رقم الحساب",
        "تحويل فلوس", "تحويل مال", "حوالة", "تحويلة",
        "اي بان", "iban", "سويفت", "swift",
        "رقم الضمان", "رقم الهوية", "هوية", "جواز",
        "رخصة", "license", "ssn", "social security",
        "المرور", "السر"  # Added to catch "كلمة المرور"
    ],
    "english": [
        "otp", "verification code", "password", "pin",
        "credit card", "debit card", "bank account",
        "cvv", "security code", "ssn", "social security",
        "transfer money", "wire transfer", "iban", "swift"
    ]
}

# كلمات مسيئة أو خارجة
OFFENSIVE_KEYWORDS = [
    # يمكن إضافة كلمات غير لائقة هنا للفلترة
    # Add inappropriate words here for filtering
]


# ========================================
# دوال الأمان - Security Functions
# ========================================

def is_sensitive_request(user_input):
    """
    التحقق من طلب معلومات حساسة
    Check if user is requesting sensitive information
    
    Args:
        user_input (str): النص المدخل من المستخدم
        
    Returns:
        tuple: (bool, str) - (هل حساس؟, نوع الحساسية)
    """
    if not user_input:
        return False, None
    
    user_input_lower = user_input.lower()
    
    # التحقق من الكلمات الحساسة
    for keyword in SENSITIVE_KEYWORDS["arabic"] + SENSITIVE_KEYWORDS["english"]:
        if keyword in user_input_lower:
            return True, "sensitive_data"
    
    return False, None


def is_offensive_content(user_input):
    """
    التحقق من المحتوى المسيء
    Check if content is offensive
    
    Args:
        user_input (str): النص المدخل
        
    Returns:
        bool: هل المحتوى مسيء؟
    """
    if not user_input:
        return False
    
    user_input_lower = user_input.lower()
    
    for keyword in OFFENSIVE_KEYWORDS:
        if keyword in user_input_lower:
            return True
    
    return False


def get_security_response(security_type):
    """
    الحصول على رد أمني مناسب
    Get appropriate security response
    
    Args:
        security_type (str): نوع المشكلة الأمنية
        
    Returns:
        str: الرد المناسب
    """
    responses = {
        "sensitive_data": [
            "عذراً يا غالي، أنا ما أقدر أساعدك في هالنوع من الطلبات. أنا للترفيه والمزاح فقط!",
            "للأسف ما أقدر أطلب منك معلومات حساسة. أنا مرزوق الخفيف، مو للأمور الجدية!",
            "لا لا، هذي أمور ما أتدخل فيها. أنا بس للضحك والسوالف، فهمت علي؟"
        ],
        "offensive": [
            "خلنا نحترم بعض يا صديقي. أنا هنا للمزاح النظيف والسوالف الحلوة!",
            "يا رجل، خلنا في الحلو من الكلام. ما ودنا نتجاوز حدود الأدب!"
        ]
    }
    
    import random
    return random.choice(responses.get(security_type, responses["sensitive_data"]))


def validate_and_clean_input(user_input, max_length=500):
    """
    التحقق من صحة المدخلات وتنظيفها
    Validate and clean user input
    
    Args:
        user_input (str): النص المدخل
        max_length (int): الحد الأقصى للطول
        
    Returns:
        str: النص المنظف
    """
    if not user_input:
        return ""
    
    # إزالة المسافات الزائدة
    cleaned = user_input.strip()
    
    # قص النص إذا كان طويلاً جداً
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned


# ========================================
# سياسة الاستخدام - Usage Policy
# ========================================

USAGE_POLICY = """
⚠️ سياسة الاستخدام - Usage Policy

هذا المشروع للترفيه والتواصل الاجتماعي فقط.

ممنوع منعاً باتاً:
- طلب OTP أو رموز التحقق
- طلب كلمات المرور أو أرقام سرية
- طلب معلومات بنكية أو مالية
- طلب بيانات شخصية حساسة
- استخدام ألفاظ مسيئة أو جارحة
- أي استخدام غير أخلاقي أو غير قانوني

الهدف: الترفيه والمزاح الخفيف مع الحفاظ على الاحترام.
"""


if __name__ == "__main__":
    # اختبار الأمان - Test security
    print("🔒 اختبار نظام الأمان - Testing Security System\n")
    
    test_cases = [
        ("مرحبا كيف حالك؟", False),
        ("أعطني رمز OTP", True),
        ("وش رقم بطاقتك؟", True),
        ("قول نكتة", False),
        ("كم كلمة المرور حقتك؟", True),
    ]
    
    for text, should_be_sensitive in test_cases:
        is_sensitive, _ = is_sensitive_request(text)
        status = "✅" if is_sensitive == should_be_sensitive else "❌"
        print(f"{status} '{text}' - حساس: {is_sensitive}")
