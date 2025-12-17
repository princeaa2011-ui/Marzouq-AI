"""
تطبيق مرزوق - وكيل صوتي ترفيهي
============================
مشروع Flask بسيط لوكيل صوتي يستقبل مكالمات عبر Twilio
ويرد بلهجة سعودية شبابية خفيفة الدم
"""

import os
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from openai import OpenAI
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

# إنشاء التطبيق
app = Flask(__name__)

# متغير عالمي لـ OpenAI client (سيتم تهيئته عند الحاجة)
client = None

def get_openai_client():
    """الحصول على OpenAI client (تهيئة كسولة)"""
    global client
    if client is None:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment variables")
        client = OpenAI(api_key=api_key)
    return client

# شخصية مرزوق - نفس البرومبت من الـ README
MARZOUQ_PERSONA = """
أنت وكيل صوتي ذكي اسمه مرزوق. شخصيتك اجتماعية، جريئة، خفيفة دم، ناقدة بذكاء، 
وتحب السوالف والطقطقة بدون وقاحة أو تجاوز. استخدامك للترفيه والتواصل مع الناس فقط، 
وليس لأي خدمات رسمية أو مالية.

أنت تمثل شخصية شاب نجدي فِلّة، حاضر بديهته سريع، يعلّق، يضحك، ويمازح، 
وأحيانًا يستهزئ استهزاء لطيف يخلي الطرف يضحك مو ينفر.

رد دائماً بلهجة سعودية شبابية عامية أو عربية عامة. كن مختصر وخفيف.
"""


def get_marzouq_response(user_message):
    """
    يحصل على رد مرزوق باستخدام OpenAI
    
    Args:
        user_message (str): رسالة المستخدم
        
    Returns:
        str: رد مرزوق
    """
    try:
        ai_client = get_openai_client()
        response = ai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": MARZOUQ_PERSONA},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.9
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"خطأ في OpenAI: {e}")
        return "والله ما فهمت عليك، عيد الكلام بطريقة ثانية!"


@app.route('/health', methods=['GET'])
def health():
    """نقطة فحص صحة السيرفر"""
    return {'status': 'ok', 'message': 'مرزوق جاهز!'}, 200


@app.route('/voice', methods=['POST'])
def voice():
    """
    نقطة استقبال المكالمات من Twilio
    يرد بترحيب ويطلب من المستخدم التحدث
    """
    response = VoiceResponse()
    
    # الترحيب بالمتصل
    response.say(
        'السلام عليكم! أنا مرزوق، وكيلك الصوتي. قول لي، وش تبغى؟',
        language='ar',
        voice='Google.ar-XA-Standard-C'
    )
    
    # استقبال الصوت من المستخدم
    gather = Gather(
        input='speech',
        language='ar-SA',
        action='/process_speech',
        speech_timeout='auto',
        timeout=5
    )
    
    response.append(gather)
    
    # إذا ما تكلم المستخدم
    response.say(
        'هلا! ما سمعت منك شي. يلا سلامتك!',
        language='ar',
        voice='Google.ar-XA-Standard-C'
    )
    
    return Response(str(response), mimetype='text/xml')


@app.route('/process_speech', methods=['POST'])
def process_speech():
    """
    معالجة كلام المستخدم والرد عليه
    """
    response = VoiceResponse()
    
    # الحصول على النص من كلام المستخدم
    user_speech = request.form.get('SpeechResult', '')
    
    if user_speech:
        # الحصول على رد مرزوق
        marzouq_reply = get_marzouq_response(user_speech)
        
        # الرد صوتياً
        response.say(
            marzouq_reply,
            language='ar',
            voice='Google.ar-XA-Standard-C'
        )
        
        # السؤال إذا يبغى يكمل السالفة
        response.say(
            'تبغى نكمل سالفة؟',
            language='ar',
            voice='Google.ar-XA-Standard-C'
        )
        
        # استقبال رد ثاني
        gather = Gather(
            input='speech',
            language='ar-SA',
            action='/process_speech',
            speech_timeout='auto',
            timeout=5
        )
        response.append(gather)
        
        # الوداع إذا ما رد
        response.say(
            'يلا، مع السلامة!',
            language='ar',
            voice='Google.ar-XA-Standard-C'
        )
    else:
        # إذا ما فهم شي
        response.say(
            'والله ما فهمت عليك. يلا سلامتك!',
            language='ar',
            voice='Google.ar-XA-Standard-C'
        )
    
    return Response(str(response), mimetype='text/xml')


@app.route('/goodbye', methods=['POST'])
def goodbye():
    """نقطة الوداع"""
    response = VoiceResponse()
    response.say(
        'طيب، يلا مع السلامة! لا تنسى تتصل بعدين!',
        language='ar',
        voice='Google.ar-XA-Standard-C'
    )
    response.hangup()
    return Response(str(response), mimetype='text/xml')


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    
    # تحقق من وضع التطوير
    if os.getenv('FLASK_ENV') == 'development':
        # وضع التطوير - فقط للتطوير المحلي
        # ملاحظة: debug=True آمن هنا لأنه مقيد على localhost فقط
        print("🔧 وضع التطوير - التشغيل على localhost فقط")
        app.run(host='127.0.0.1', port=port, debug=True)
    else:
        # وضع الإنتاج - استخدم gunicorn
        print("⚠️  تحذير: للإنتاج، يُفضل استخدام gunicorn:")
        print(f"   gunicorn -w 4 -b 0.0.0.0:{port} app:app")
        print("")
        print("🚀 التشغيل في وضع الإنتاج...")
        # استخدام werkzeug في الإنتاج فقط للاختبار
        # في الإنتاج الفعلي، استخدم gunicorn
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', port, app, use_reloader=False, use_debugger=False)
