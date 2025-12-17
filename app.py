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
