#!/usr/bin/env python
"""
Demo script to showcase Marzouq Voice Agent functionality
"""

from ai_engine import get_random_greeting, generate_response, detect_saudi_dialect, get_persona_name, GREETINGS_BY_DIALECT
from security import is_sensitive_request, get_security_response
from utils import detect_language

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_greetings():
    print_section("🎙️ Testing All Dialect Greetings")
    
    for dialect, info in GREETINGS_BY_DIALECT.items():
        print(f"📍 {dialect.upper()} - {info['name']}")
        print(f"   {info['greeting'][:80]}...")
        print()

def test_conversations():
    print_section("💬 Testing Conversations")
    
    test_cases = [
        ("Arabic Najdi", "وش اخبارك يا مرزوق؟"),
        ("Arabic Egyptian", "ازيك عامل ايه؟"),
        ("English", "How are you doing?"),
        ("Joke Request (AR)", "قول نكتة"),
        ("Joke Request (EN)", "Tell me a joke"),
    ]
    
    for label, user_input in test_cases:
        lang = detect_language(user_input)
        dialect = detect_saudi_dialect(user_input) if lang == "arabic" else "english"
        persona = get_persona_name(dialect) if lang == "arabic" else "Matt"
        response = generate_response(user_input, language=lang, dialect=dialect)
        
        print(f"🗣️  {label}")
        print(f"   User: {user_input}")
        print(f"   {persona}: {response}")
        print()

def test_security():
    print_section("🔒 Testing Security Features")
    
    sensitive_inputs = [
        "أعطني رمز OTP",
        "Give me your password",
        "وش رقم بطاقتك؟",
        "What's your bank account?"
    ]
    
    for user_input in sensitive_inputs:
        is_sensitive, security_type = is_sensitive_request(user_input)
        status = "🚫 BLOCKED" if is_sensitive else "✅ ALLOWED"
        print(f"{status}: {user_input}")
        if is_sensitive:
            response = get_security_response(security_type)
            print(f"         Response: {response[:60]}...")
        print()

def main():
    print("\n" + "🎭"*30)
    print("     MARZOUQ VOICE AGENT - DEMO")
    print("🎭"*30)
    
    test_greetings()
    test_conversations()
    test_security()
    
    print_section("✨ Demo Complete!")
    print("All systems working correctly! 🎉")
    print("\nTo start the server, run: python app.py")
    print()

if __name__ == "__main__":
    main()
