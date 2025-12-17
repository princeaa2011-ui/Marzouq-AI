"""
keyboards.py - لوحات المفاتيح والأرقام
Keyboards and Keypads for Marzouq Voice Agent

يحتوي على:
- لوحة مفاتيح عربية (حروف وأرقام)
- لوحة مفاتيح إنجليزية (حروف وأرقام)
"""


# ========================================
# لوحة المفاتيح العربية - Arabic Keyboard
# ========================================

ARABIC_KEYBOARD = {
    # الحروف العربية - Arabic Letters
    "letters": [
        # الصف الأول - First Row
        ["ض", "ص", "ث", "ق", "ف", "غ", "ع", "ه", "خ", "ح", "ج", "د"],
        # الصف الثاني - Second Row
        ["ش", "س", "ي", "ب", "ل", "ا", "ت", "ن", "م", "ك", "ط"],
        # الصف الثالث - Third Row
        ["ئ", "ء", "ؤ", "ر", "لا", "ى", "ة", "و", "ز", "ظ"]
    ],
    
    # الأرقام - Numbers
    "numbers": ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"],
    
    # الأرقام الإنجليزية (للتوافق) - English Numbers (for compatibility)
    "english_numbers": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    
    # رموز خاصة - Special Characters
    "special": [
        "؟", "،", "؛", ":", ".", "!", "@", "#", 
        "$", "%", "^", "&", "*", "(", ")", "-", 
        "_", "+", "=", "/", "\\", "|", "[", "]", 
        "{", "}", "<", ">", "~", "`"
    ],
    
    # أزرار التحكم - Control Keys
    "controls": {
        "space": " ",
        "enter": "\n",
        "backspace": "⌫",
        "clear": "⌧",
        "shift": "⇧",
        "caps": "⇪"
    }
}


# ========================================
# لوحة المفاتيح الإنجليزية - English Keyboard
# ========================================

ENGLISH_KEYBOARD = {
    # الحروف الإنجليزية - English Letters
    "letters": [
        # الصف الأول - First Row (QWERTY)
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        # الصف الثاني - Second Row
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        # الصف الثالث - Third Row
        ["Z", "X", "C", "V", "B", "N", "M"]
    ],
    
    # الحروف الصغيرة - Lowercase Letters
    "lowercase": [
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
        ["z", "x", "c", "v", "b", "n", "m"]
    ],
    
    # الأرقام - Numbers
    "numbers": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    
    # رموز خاصة - Special Characters
    "special": [
        "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
        "-", "_", "+", "=", "[", "]", "{", "}", "\\", "|",
        ";", ":", "'", "\"", ",", ".", "<", ">", "/", "?",
        "~", "`"
    ],
    
    # أزرار التحكم - Control Keys
    "controls": {
        "space": " ",
        "enter": "\n",
        "backspace": "⌫",
        "clear": "⌧",
        "shift": "⇧",
        "caps": "⇪",
        "tab": "⇥"
    }
}


# ========================================
# لوحة الأرقام - Numeric Keypad
# ========================================

NUMERIC_KEYPAD = {
    # لوحة أرقام عربية - Arabic Numeric Keypad
    "arabic": [
        ["٧", "٨", "٩"],
        ["٤", "٥", "٦"],
        ["١", "٢", "٣"],
        ["٠", ".", "⌫"]
    ],
    
    # لوحة أرقام إنجليزية - English Numeric Keypad
    "english": [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        ["0", ".", "⌫"]
    ]
}


# ========================================
# دوال مساعدة - Helper Functions
# ========================================

def get_keyboard(language="arabic"):
    """
    الحصول على لوحة المفاتيح حسب اللغة
    Get keyboard based on language
    
    Args:
        language (str): "arabic" or "english"
        
    Returns:
        dict: لوحة المفاتيح
    """
    if language.lower() == "arabic":
        return ARABIC_KEYBOARD
    elif language.lower() == "english":
        return ENGLISH_KEYBOARD
    else:
        return ARABIC_KEYBOARD  # افتراضي


def get_numeric_keypad(language="english"):
    """
    الحصول على لوحة الأرقام حسب اللغة
    Get numeric keypad based on language
    
    Args:
        language (str): "arabic" or "english"
        
    Returns:
        list: لوحة الأرقام
    """
    if language.lower() == "arabic":
        return NUMERIC_KEYPAD["arabic"]
    elif language.lower() == "english":
        return NUMERIC_KEYPAD["english"]
    else:
        return NUMERIC_KEYPAD["english"]  # افتراضي


def arabic_to_english_number(arabic_num):
    """
    تحويل الأرقام العربية إلى إنجليزية
    Convert Arabic numbers to English
    
    Args:
        arabic_num (str): رقم عربي
        
    Returns:
        str: رقم إنجليزي
    """
    arabic_to_english = {
        "٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4",
        "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9"
    }
    
    result = ""
    for char in str(arabic_num):
        result += arabic_to_english.get(char, char)
    
    return result


def english_to_arabic_number(english_num):
    """
    تحويل الأرقام الإنجليزية إلى عربية
    Convert English numbers to Arabic
    
    Args:
        english_num (str): رقم إنجليزي
        
    Returns:
        str: رقم عربي
    """
    english_to_arabic = {
        "0": "٠", "1": "١", "2": "٢", "3": "٣", "4": "٤",
        "5": "٥", "6": "٦", "7": "٧", "8": "٨", "9": "٩"
    }
    
    result = ""
    for char in str(english_num):
        result += english_to_arabic.get(char, char)
    
    return result


def display_keyboard(language="arabic", include_numbers=True):
    """
    عرض لوحة المفاتيح
    Display keyboard layout
    
    Args:
        language (str): "arabic" or "english"
        include_numbers (bool): عرض الأرقام
        
    Returns:
        str: تمثيل نصي للوحة المفاتيح
    """
    keyboard = get_keyboard(language)
    output = []
    
    output.append(f"\n{'='*50}")
    output.append(f"  {language.upper()} KEYBOARD")
    output.append(f"{'='*50}\n")
    
    # عرض الأرقام - Display Numbers
    if include_numbers:
        output.append("NUMBERS:")
        output.append(" ".join(keyboard["numbers"]))
        output.append("")
    
    # عرض الحروف - Display Letters
    output.append("LETTERS:")
    if language == "english":
        letters = keyboard["letters"]
    else:
        letters = keyboard["letters"]
    
    for row in letters:
        output.append(" ".join(row))
    
    output.append("")
    
    # عرض الرموز الخاصة - Display Special Characters
    output.append("SPECIAL CHARACTERS:")
    special = keyboard["special"]
    # عرض 10 رموز في كل سطر
    for i in range(0, len(special), 10):
        output.append(" ".join(special[i:i+10]))
    
    output.append("")
    output.append(f"{'='*50}\n")
    
    return "\n".join(output)


def display_numeric_keypad(language="english"):
    """
    عرض لوحة الأرقام
    Display numeric keypad
    
    Args:
        language (str): "arabic" or "english"
        
    Returns:
        str: تمثيل نصي للوحة الأرقام
    """
    keypad = get_numeric_keypad(language)
    output = []
    
    output.append(f"\n{'='*30}")
    output.append(f"  {language.upper()} NUMERIC KEYPAD")
    output.append(f"{'='*30}\n")
    
    for row in keypad:
        output.append("  ".join(f"[{key}]" for key in row))
    
    output.append(f"\n{'='*30}\n")
    
    return "\n".join(output)


# ========================================
# اختبار - Testing
# ========================================

if __name__ == "__main__":
    print("🎹 اختبار لوحات المفاتيح - Testing Keyboards\n")
    
    # عرض لوحة المفاتيح العربية
    print(display_keyboard("arabic"))
    
    # عرض لوحة المفاتيح الإنجليزية
    print(display_keyboard("english"))
    
    # عرض لوحة الأرقام العربية
    print(display_numeric_keypad("arabic"))
    
    # عرض لوحة الأرقام الإنجليزية
    print(display_numeric_keypad("english"))
    
    # اختبار التحويل بين الأرقام
    print("\n🔢 Number Conversion Tests:")
    print(f"Arabic '٥٦٧' to English: {arabic_to_english_number('٥٦٧')}")
    print(f"English '123' to Arabic: {english_to_arabic_number('123')}")
    print(f"Mixed '٥6٧' to English: {arabic_to_english_number('٥6٧')}")
    
    print("\n✅ All keyboards loaded successfully!")
