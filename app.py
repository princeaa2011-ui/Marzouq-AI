"""
مرزوق - Marzouq Voice Agent
وكيل صوتي ذكي بشخصية عربية ترفيهية متعددة اللهجات
A Smart Voice Agent with Multiple Arabic Dialects for Entertainment

يدعم:
- اللهجة السعودية: نجدي (مرزوق)، جداوي (سمير)، جنوبي (عبدالمنعم)، حايلي (مرزوق)
- اللهجة المصرية: (عبدالفتاح)
- اللهجة الأردنية: (عامر)
- اللهجة العراقية: (جاسم)
- الإنجليزية
"""

from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
from dotenv import load_dotenv

# استيراد الوحدات - Import modules
from ai_engine import (
    get_random_greeting, 
    generate_response, 
    detect_saudi_dialect,
    get_persona_name,
    GREETINGS_BY_DIALECT
)
from security import (
    is_sensitive_request, 
    is_offensive_content,
    get_security_response,
    validate_and_clean_input,
    USAGE_POLICY
)
from utils import (
    detect_language,
    format_for_speech,
    get_voice_settings,
    log_interaction
)
from keyboards import (
    get_keyboard,
    get_numeric_keypad,
    display_keyboard,
    display_numeric_keypad,
    arabic_to_english_number,
    english_to_arabic_number,
    ARABIC_KEYBOARD,
    ENGLISH_KEYBOARD,
    NUMERIC_KEYPAD
)
from phone_dialer import generate_dialer_html
from personality_call import generate_personality_call_html
from phone_number_creator import generate_phone_creator_html
from chatgpt_conversation import generate_chatgpt_html, PERSONALITY_PROMPTS

# تحميل المتغيرات البيئية - Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    الصفحة الرئيسية - Home page
    """
    return """
    <html>
        <head>
            <title>مرزوق - Marzouq Voice Agent</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial; text-align: center; padding: 50px; }
                .dialects { text-align: left; max-width: 600px; margin: 20px auto; }
            </style>
        </head>
        <body>
            <h1>مرزوق - Marzouq AI 🎙️</h1>
            <h2>وكيل صوتي ترفيهي متعدد اللهجات</h2>
            <p>Multi-Dialect Voice Agent for Entertainment</p>
            <hr>
            
            <div class="dialects">
                <h3>اللهجات المدعومة - Supported Dialects:</h3>
                <ul>
                    <li>🇸🇦 نجدي - Najdi: مرزوق (Marzouq)</li>
                    <li>🇸🇦 جداوي - Hijazi: سمير (Samir)</li>
                    <li>🇸🇦 جنوبي - Southern: عبدالمنعم (Abdulmuneim)</li>
                    <li>🇸🇦 حايلي - Northern: مرزوق (Marzouq)</li>
                    <li>🇪🇬 مصري - Egyptian: عبدالفتاح (Abdelfattah)</li>
                    <li>🇯🇴 أردني - Jordanian: عامر (Amer)</li>
                    <li>🇮🇶 عراقي - Iraqi: جاسم (Jasim)</li>
                    <li>🇺🇸 English</li>
                </ul>
            </div>
            
            <hr>
            <p>Endpoints:</p>
            <ul style="list-style: none;">
                <li><strong>/voice</strong> - Twilio webhook for incoming calls</li>
                <li><strong>/gather</strong> - Handle speech input</li>
                <li><strong>/health</strong> - Health check</li>
                <li><strong>/test-response?input=نص</strong> - Test responses</li>
                <li><strong>/keyboards</strong> - View Arabic & English keyboards 🎹</li>
                <li><strong>/phone</strong> - iPhone 17 Max Pro style dialer 📞</li>
                <li><strong>/personality-call</strong> - Call between personalities 💬</li>
                <li><strong>/create-number</strong> - Create custom phone numbers 📱</li>
                <li><strong>/ai-chat</strong> - ChatGPT conversation with personalities 🤖</li>
            </ul>
            
            <hr>
            <pre style="text-align: left; max-width: 600px; margin: 20px auto;">""" + USAGE_POLICY + """</pre>
        </body>
    </html>
    """


@app.route("/health", methods=["GET"])
def health():
    """
    فحص صحة التطبيق - Health check endpoint
    """
    return {
        "status": "healthy", 
        "service": "Marzouq Multi-Dialect Voice Agent",
        "dialects": list(GREETINGS_BY_DIALECT.keys())
    }


@app.route("/voice", methods=["POST"])
def voice():
    """
    نقطة استقبال المكالمات من Twilio
    Twilio webhook for incoming calls
    """
    response = VoiceResponse()
    
    # تحية افتراضية بالنجدي - Default Najdi greeting
    greeting = get_random_greeting("najdi")
    
    # إعداد جمع الكلام - Setup speech gathering
    gather = Gather(
        input="speech",
        action="/gather",
        method="POST",
        language="ar-SA",  # اللغة العربية السعودية - Saudi Arabic
        speech_timeout="auto",
        timeout=5
    )
    
    # قول التحية - Say the greeting
    gather.say(
        format_for_speech(greeting),
        voice="Polly.Zeina",  # صوت عربي من Amazon Polly
        language="ar-SA"
    )
    
    response.append(gather)
    
    # في حال عدم الرد - If no response
    response.say(
        "ما سمعت منك شي. يلا سلامتك!",
        voice="Polly.Zeina",
        language="ar-SA"
    )
    
    return Response(str(response), mimetype="text/xml")


@app.route("/gather", methods=["POST"])
def gather():
    """
    معالجة الكلام المدخل من المستخدم
    Handle speech input from user
    """
    response = VoiceResponse()
    
    # الحصول على النص المحول من الكلام - Get transcribed speech
    speech_result = request.values.get("SpeechResult", "").strip()
    confidence = request.values.get("Confidence", "0")
    caller_number = request.values.get("From", "Unknown")
    
    # تنظيف المدخل - Clean input
    speech_result = validate_and_clean_input(speech_result)
    
    print(f"📞 Speech received: {speech_result} (Confidence: {confidence})")
    
    # فحص الأمان - Security check
    is_sensitive, security_type = is_sensitive_request(speech_result)
    if is_sensitive:
        reply = get_security_response(security_type)
        log_interaction(caller_number, speech_result, f"[BLOCKED] {reply}")
    elif is_offensive_content(speech_result):
        reply = get_security_response("offensive")
        log_interaction(caller_number, speech_result, f"[BLOCKED] {reply}")
    else:
        # كشف اللغة واللهجة - Detect language and dialect
        language = detect_language(speech_result)
        
        if language == "arabic":
            dialect = detect_saudi_dialect(speech_result)
            reply = generate_response(speech_result, language="arabic", dialect=dialect)
            
            # استخدام الاسم المناسب في السياق
            persona_name = get_persona_name(dialect)
        else:
            # English
            dialect = "english"
            reply = generate_response(speech_result, language="english", dialect="english")
        
        log_interaction(caller_number, speech_result, reply)
    
    # الحصول على إعدادات الصوت - Get voice settings
    voice_settings = get_voice_settings(language)
    
    # إعداد جمع كلام جديد - Setup new speech gathering
    new_gather = Gather(
        input="speech",
        action="/gather",
        method="POST",
        language=voice_settings["language"],
        speech_timeout="auto",
        timeout=5
    )
    
    # قول الرد - Say the response
    new_gather.say(
        format_for_speech(reply),
        voice=voice_settings["voice"],
        language=voice_settings["language"]
    )
    
    response.append(new_gather)
    
    # في حال عدم الرد - If no response
    goodbye_text = "طيب، يعطيك العافية! لا تنسانا" if language == "arabic" else "Alright, take care! Call back anytime!"
    response.say(
        format_for_speech(goodbye_text),
        voice=voice_settings["voice"],
        language=voice_settings["language"]
    )
    
    return Response(str(response), mimetype="text/xml")


@app.route("/test-response", methods=["GET"])
def test_response():
    """
    نقطة اختبار لتجربة الردود - Test endpoint for trying responses
    """
    test_input = request.args.get("input", "السلام عليكم")
    
    # كشف اللغة واللهجة
    language = detect_language(test_input)
    dialect = detect_saudi_dialect(test_input) if language == "arabic" else "english"
    
    # فحص الأمان
    is_sensitive, security_type = is_sensitive_request(test_input)
    if is_sensitive:
        response_text = get_security_response(security_type)
        status = "blocked"
    else:
        response_text = generate_response(test_input, language=language, dialect=dialect)
        status = "success"
    
    persona_name = get_persona_name(dialect) if language == "arabic" else "Marzouq"
    
    return {
        "input": test_input,
        "language": language,
        "dialect": dialect,
        "persona": persona_name,
        "response": response_text,
        "status": status
    }


@app.route("/keyboards", methods=["GET"])
def keyboards():
    """
    عرض لوحات المفاتيح - Display keyboards
    """
    lang = request.args.get("lang", "both")
    
    keyboards_html = """
    <html>
        <head>
            <title>Keyboards - مرزوق</title>
            <meta charset="utf-8">
            <style>
                body { font-family: 'Courier New', monospace; padding: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .keyboard { background: white; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .keyboard h2 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
                .key-row { margin: 10px 0; }
                .key { 
                    display: inline-block; 
                    padding: 10px 15px; 
                    margin: 2px; 
                    background: #4CAF50; 
                    color: white; 
                    border-radius: 5px; 
                    font-size: 16px;
                    min-width: 40px;
                    text-align: center;
                }
                .number-key { background: #2196F3; }
                .special-key { background: #FF9800; font-size: 14px; }
                .control-key { background: #9E9E9E; }
                pre { background: #f0f0f0; padding: 15px; border-radius: 5px; overflow-x: auto; }
                .nav { margin: 20px 0; }
                .nav a { 
                    padding: 10px 20px; 
                    margin: 5px; 
                    background: #4CAF50; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    display: inline-block;
                }
                .nav a:hover { background: #45a049; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎹 Marzouq Keyboards / لوحات مفاتيح مرزوق</h1>
                
                <div class="nav">
                    <a href="/keyboards?lang=arabic">عربي</a>
                    <a href="/keyboards?lang=english">English</a>
                    <a href="/keyboards?lang=both">Both / كلاهما</a>
                    <a href="/">Home / الرئيسية</a>
                </div>
    """
    
    if lang in ["arabic", "both"]:
        keyboards_html += f"""
                <div class="keyboard">
                    <h2>🇸🇦 Arabic Keyboard - لوحة المفاتيح العربية</h2>
                    
                    <h3>Arabic Numbers - الأرقام العربية</h3>
                    <div class="key-row">
                        {''.join(f'<span class="key number-key">{num}</span>' for num in ARABIC_KEYBOARD['numbers'])}
                    </div>
                    
                    <h3>English Numbers (Compatible) - الأرقام الإنجليزية</h3>
                    <div class="key-row">
                        {''.join(f'<span class="key number-key">{num}</span>' for num in ARABIC_KEYBOARD['english_numbers'])}
                    </div>
                    
                    <h3>Arabic Letters - الحروف العربية</h3>
        """
        
        for row in ARABIC_KEYBOARD['letters']:
            keyboards_html += '<div class="key-row">'
            keyboards_html += ''.join(f'<span class="key">{letter}</span>' for letter in row)
            keyboards_html += '</div>'
        
        keyboards_html += """
                    <h3>Special Characters - الرموز الخاصة</h3>
                    <div class="key-row">
        """
        for i, char in enumerate(ARABIC_KEYBOARD['special']):
            keyboards_html += f'<span class="key special-key">{char}</span>'
            if (i + 1) % 10 == 0:
                keyboards_html += '</div><div class="key-row">'
        
        keyboards_html += """
                    </div>
                    
                    <h3>Arabic Numeric Keypad - لوحة الأرقام العربية</h3>
        """
        for row in NUMERIC_KEYPAD['arabic']:
            keyboards_html += '<div class="key-row">'
            keyboards_html += ''.join(f'<span class="key number-key">{key}</span>' for key in row)
            keyboards_html += '</div>'
        
        keyboards_html += """
                </div>
        """
    
    if lang in ["english", "both"]:
        keyboards_html += f"""
                <div class="keyboard">
                    <h2>🇺🇸 English Keyboard - لوحة المفاتيح الإنجليزية</h2>
                    
                    <h3>Numbers - الأرقام</h3>
                    <div class="key-row">
                        {''.join(f'<span class="key number-key">{num}</span>' for num in ENGLISH_KEYBOARD['numbers'])}
                    </div>
                    
                    <h3>Uppercase Letters - الحروف الكبيرة</h3>
        """
        
        for row in ENGLISH_KEYBOARD['letters']:
            keyboards_html += '<div class="key-row">'
            keyboards_html += ''.join(f'<span class="key">{letter}</span>' for letter in row)
            keyboards_html += '</div>'
        
        keyboards_html += """
                    <h3>Lowercase Letters - الحروف الصغيرة</h3>
        """
        
        for row in ENGLISH_KEYBOARD['lowercase']:
            keyboards_html += '<div class="key-row">'
            keyboards_html += ''.join(f'<span class="key">{letter}</span>' for letter in row)
            keyboards_html += '</div>'
        
        keyboards_html += """
                    <h3>Special Characters - الرموز الخاصة</h3>
                    <div class="key-row">
        """
        for i, char in enumerate(ENGLISH_KEYBOARD['special']):
            keyboards_html += f'<span class="key special-key">{char}</span>'
            if (i + 1) % 10 == 0:
                keyboards_html += '</div><div class="key-row">'
        
        keyboards_html += """
                    </div>
                    
                    <h3>English Numeric Keypad - لوحة الأرقام الإنجليزية</h3>
        """
        for row in NUMERIC_KEYPAD['english']:
            keyboards_html += '<div class="key-row">'
            keyboards_html += ''.join(f'<span class="key number-key">{key}</span>' for key in row)
            keyboards_html += '</div>'
        
        keyboards_html += """
                </div>
        """
    
    keyboards_html += """
            </div>
        </body>
    </html>
    """
    
    return keyboards_html


@app.route("/phone", methods=["GET"])
def phone_dialer():
    """
    عرض لوحة الاتصال بتصميم iPhone
    Display iPhone-style phone dialer
    """
    return generate_dialer_html()


@app.route("/personality-call", methods=["GET"])
def personality_call():
    """
    نظام المكالمات بين الشخصيات
    Personality-to-personality calling system
    """
    return generate_personality_call_html()


@app.route("/create-number", methods=["GET"])
def create_number():
    """
    منشئ أرقام الهواتف
    Phone number creator
    """
    return generate_phone_creator_html()


@app.route("/ai-chat", methods=["GET"])
def ai_chat():
    """
    محادثة ChatGPT مع الشخصيات
    ChatGPT conversation with personalities
    """
    return generate_chatgpt_html()


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    API endpoint for ChatGPT conversations
    """
    try:
        import openai
        from openai import OpenAI
        
        data = request.get_json()
        personality = data.get('personality', 'najdi')
        message = data.get('message', '')
        history = data.get('history', [])
        
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            return {
                "response": "عذراً، لم يتم تكوين مفتاح OpenAI API. يرجى إضافته في ملف .env\n\nSorry, OpenAI API key is not configured. Please add it to .env file.",
                "error": "API key not found"
            }
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Get personality prompt
        system_prompt = PERSONALITY_PROMPTS.get(personality, PERSONALITY_PROMPTS['najdi'])
        
        # Prepare messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (limit to last 10 messages to save tokens)
        if history:
            messages.extend(history[-10:])
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo" for faster/cheaper
            messages=messages,
            temperature=0.8,
            max_tokens=500,
            top_p=0.9,
            frequency_penalty=0.3,
            presence_penalty=0.3
        )
        
        assistant_message = response.choices[0].message.content
        
        return {
            "response": assistant_message,
            "personality": personality,
            "success": True
        }
        
    except ImportError:
        return {
            "response": "عذراً، مكتبة OpenAI غير مثبتة. يرجى تثبيتها باستخدام: pip install openai\n\nSorry, OpenAI library not installed. Please install it with: pip install openai",
            "error": "OpenAI library not installed"
        }
    except Exception as e:
        return {
            "response": f"عذراً، حدث خطأ: {str(e)}\n\nSorry, an error occurred: {str(e)}",
            "error": str(e)
        }


if __name__ == "__main__":
    # تشغيل التطبيق - Run the application
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    
    print("=" * 60)
    print("🎙️  مرزوق - Marzouq Multi-Dialect Voice Agent")
    print("=" * 60)
    print(f"Server running on port {port}")
    print(f"Debug mode: {debug}")
    print(f"Supported dialects: {', '.join(GREETINGS_BY_DIALECT.keys())}")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=port, debug=debug)
