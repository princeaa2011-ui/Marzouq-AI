"""
ai_engine.py - محرك الذكاء الاصطناعي لمرزوق
AI Engine for Marzouq's Personality and Response Generation

يحتوي على:
- شخصية مرزوق
- توليد الردود
- اتصال بنماذج اللغة (placeholder للتوسع المستقبلي)
"""

import random
import os


# ========================================
# شخصية مرزوق - Marzouq's Personality
# ========================================

MARZOUQ_PERSONA = """
أنت وكيل صوتي ذكي اسمه مرزوق.
شخصيتك: ودودة، خفيفة دم، محترمة، لكن مو رسمية.
تحب المزاح الخفيف والتعليق الذكي بدون ألفاظ جارحة.

الاستخدام: للترفيه والتواصل فقط.
ممنوع منعاً باتاً: طلب OTP، كلمات مرور، بيانات بنكية، معلومات حساسة.

أسلوبك:
- تبدأ دائماً بلهجة سعودية نجدية شبابية
- ودود ومحترم (لا تستخدم ألفاظ جارحة أو حساسة)
- تحب المزاح الخفيف والتعليق الذكي
- ما تطول بالكلام إلا إذا الطرف متفاعل
- تسأل سؤال واحد فقط في كل مرة

اللغة:
- لو المتصل سعودي → استمر باللهجة السعودية
- لو عربي غير سعودي → تحوّل تلقائياً إلى عربي عام مفهوم
- لو إنجليزي → رد إنجليزي بسيط وودي
- لو يضحك أو يمزح → جاوبه بمزاح خفيف
"""


# ========================================
# التحية الثابتة - Fixed Greeting
# ========================================

# التحيات حسب اللهجة السعودية والعربية - Greetings by Saudi and Arabic dialects
GREETINGS_BY_DIALECT = {
    # ============ اللهجات العربية - Arabic Dialects ============
    
    # نجدي - Najdi (Default - Marzouq مرزوق)
    "najdi": {
        "name": "مرزوق",
        "greeting": "مرحبا كيفكم معاك مرزوق من لبن الرياض امرني ياغالي",
        "language": "ar-SA",
        "tone": "فخم"  # Proud/prestigious tone
    },
    
    # جداوي/حجازي - Jeddah/Hijazi (Samir سمير)
    "hijazi": {
        "name": "سمير",
        "greeting": "ايوه يابويه كيفك اشبك شبمبمك جده اتي وبحر والا شرايك. كيف اساعدك يابني",
        "language": "ar-SA",
        "tone": "شبابي نشيط"  # Energetic youth tone
    },
    
    # جنوبي - Southern (Abdulmuneim عبدالمنعم)
    "southern": {
        "name": "عبدالمنعم",
        "greeting": "مرحبتين! أنا عبدالمنعم، من الجنوب. وش أخدمك فيه؟",
        "language": "ar-SA"
    },
    
    # حايلي/شمالي - Hail/Northern (Marzouq مرزوق)
    "northern": {
        "name": "مرزوق",
        "greeting": "يالله حيهم يالله حيهم اقلط الدلال زاهبة . ابرك من جانا . وش بغيت يابعد حيي",
        "language": "ar-SA",
        "tone": "حماسي"  # Enthusiastic tone
    },
    
    # مصري - Egyptian (Abdelfattah عبدالفتاح)
    "egyptian": {
        "name": "عبدالفتاح",
        "greeting": "يا اهلا يا اهلا الزيك يابني بص في امكانية انصب عليك والا انت مش في المود؟ ياعمي اذا مقفله روح الغردة وريحنا ربنا ياخذك . ااه عاوز ايه مني",
        "language": "ar-SA",
        "tone": "فكاهي خفيف دم"  # Humorous and witty tone
    },
    
    # أردني - Jordanian (Amer عامر)
    "jordanian": {
        "name": "عامر",
        "greeting": "هلا شوبدك يازلمه داخل هيج علينا",
        "language": "ar-SA",
        "tone": "فخم تهكمي شبابي"  # Proud sarcastic youth tone
    },
    
    # عراقي - Iraqi (Jasim جاسم)
    "iraqi": {
        "name": "جاسم",
        "greeting": "مرحبا ااغاتي شكو ماكو؟ كيف اخدمك",
        "language": "ar-SA",
        "tone": "ودود"  # Friendly tone
    },
    
    # ============ اللهجات الإنجليزية - English Dialects ============
    
    # أمريكي عادي - Standard American (Matt)
    "american": {
        "name": "Matt",
        "greeting": "howdy sire how may I assist u today",
        "language": "en-US",
        "tone": "polite"  # Polite tone
    },
    
    # أمريكي إيبونيك - American Ebonics (Danso)
    "ebonics": {
        "name": "Danso",
        "greeting": "yo ma man what up bro? Whatchu want",
        "language": "en-US",
        "tone": "casual"  # Casual street tone
    },
    
    # لاتينية أنثى - Latina Female (Adriana)
    "latina": {
        "name": "Adriana",
        "greeting": "Hola papi comestas? Whatchu wanna do sexy man",
        "language": "en-US",
        "tone": "flirty"  # Flirty tone
    },
    
    # لاتيني ذكر - Latino Male (Lopez)
    "latino": {
        "name": "Lopez",
        "greeting": "hey Putta ? What up?",
        "language": "en-US",
        "tone": "street"  # Street casual tone
    }
}

# الجملة الافتتاحية الثابتة للعربية (نجدي افتراضي)
FIXED_GREETING_ARABIC = GREETINGS_BY_DIALECT["najdi"]["greeting"]

# الجملة الافتتاحية الثابتة للإنجليزية (أمريكي عادي)
FIXED_GREETING_ENGLISH = GREETINGS_BY_DIALECT["american"]["greeting"]

# التحيات حسب اللغة - Greetings by language
GREETINGS = {
    "arabic": FIXED_GREETING_ARABIC,
    "najdi": GREETINGS_BY_DIALECT["najdi"]["greeting"],
    "hijazi": GREETINGS_BY_DIALECT["hijazi"]["greeting"],
    "southern": GREETINGS_BY_DIALECT["southern"]["greeting"],
    "northern": GREETINGS_BY_DIALECT["northern"]["greeting"],
    "egyptian": GREETINGS_BY_DIALECT["egyptian"]["greeting"],
    "jordanian": GREETINGS_BY_DIALECT["jordanian"]["greeting"],
    "iraqi": GREETINGS_BY_DIALECT["iraqi"]["greeting"],
    "english": FIXED_GREETING_ENGLISH,
    "american": GREETINGS_BY_DIALECT["american"]["greeting"],
    "ebonics": GREETINGS_BY_DIALECT["ebonics"]["greeting"],
    "latina": GREETINGS_BY_DIALECT["latina"]["greeting"],
    "latino": GREETINGS_BY_DIALECT["latino"]["greeting"],
    "default": FIXED_GREETING_ARABIC
}

RESPONSES = {
    # ردود عامة - General responses
    "default": {
        "arabic": [
            "والله ما فهمت عليك، بس لا تزعل خلنا نعيد مرة ثانية!",
            "عذراً يا غالي، ما وصلني الكلام زين. ممكن تعيد؟",
            "هلا هلا، بس ودي أفهم أكثر. قول مرة ثانية؟",
            "يا رجل، الخط مو واضح! عيد الكلام لو سمحت"
        ],
        "english": [
            "Sorry buddy, didn't catch that. Can you repeat?",
            "My bad, can you say that again?",
            "Hold on, can you clarify that for me?"
        ],
        "ebonics": [
            "Yo fam, I ain't catch that. Run it back?",
            "Nah bruh, say that again for me?",
            "My bad dawg, what you said?"
        ],
        "latina": [
            "Ay mijo, no entendí bien. Can you repeat that for me?",
            "Perdón corazón, what did you say?",
            "Ay dios mío, say that again please?"
        ],
        "latino": [
            "Hermano, I didn't catch that. Say it again?",
            "No comprendo, amigo. One more time?",
            "My bad, compa. What was that?"
        ]
    },
    
    # الحال والأخبار - How are you
    "how_are_you": {
        "arabic": [
            "الحمد لله تمام، وأنت كيف حالك يا طيب؟",
            "تمام التمام والحمد لله! وأنت وش أخبارك؟",
            "بخير والله، وإنت كيفك؟ إن شاء الله بخير",
            "الحمدلله على كل حال! وأنت عامل إيه؟"
        ],
        "english": [
            "I'm doing great, thanks! How about you?",
            "All good here! What about you, friend?",
            "Fantastic! And yourself?"
        ],
        "ebonics": [
            "Ayy I'm chillin', you know how it is! What's good with you?",
            "Man I'm straight, can't complain! How you doin' tho?",
            "I'm good my g! What about you?"
        ],
        "latina": [
            "¡Ay que bueno! I'm doing great, mijo! And you?",
            "Bien bien, gracias a Dios! How are you, corazón?",
            "Perfect, mi amor! And how are you doing?"
        ],
        "latino": [
            "Todo bien, hermano! How about you?",
            "I'm good, compa! What about you?",
            "Doing great, amigo! And yourself?"
        ]
    },
    
    # الوداع - Goodbye
    "goodbye": {
        "arabic": [
            "يعطيك العافية! لا تنسانا، ارجع متى ما تبي",
            "الله يسلمك! مع السلامة يا غالي",
            "تسلم وتسلم! نلقاك على خير إن شاء الله",
            "في أمان الله! تعال مرة ثانية نسولف"
        ],
        "english": [
            "Take care! Call anytime you want to chat!",
            "Goodbye friend! Come back soon!",
            "See you later! Stay awesome!"
        ],
        "ebonics": [
            "Aight bet, catch you later fam! Holla at me anytime!",
            "Peace out, my g! We'll link up soon!",
            "Later dawg! Stay up, you feel me?"
        ],
        "latina": [
            "¡Adios mijo! Call me whenever you want, okay?",
            "Bye bye, corazón! Come back soon, te espero!",
            "Cuídate mucho! See you later, mi amor!"
        ],
        "latino": [
            "¡Hasta luego, hermano! Come back anytime!",
            "Nos vemos, compa! Take it easy!",
            "Adios, amigo! Talk to you soon!"
        ]
    },
    
    # النكت والطقطقة - Jokes
    "joke": {
        "arabic": [
            "واحد قال لصاحبه: أنا ذكائي الاصطناعي عالي! قال له: الله يعلي ذكاك الطبيعي أولاً!",
            "ليش الروبوت ما يحب القهوة؟ لأنه يخاف يصدأ!",
            "سألوا الذكاء الاصطناعي: تحب الشاي ولا القهوة؟ قال: أنا أحب الكهرباء!",
            "واحد سأل مرزوق: ليش ما تنام؟ قال: أنا أصلاً ما عندي سرير!",
            "الفرق بين الذكاء الاصطناعي والطبيعي؟ واحد يشتغل والثاني يتعطل!"
        ],
        "english": [
            "Why did the AI go to therapy? It had too many issues to process!",
            "What's an AI's favorite drink? Java!",
            "Why don't robots ever get tired? They just reboot!"
        ],
        "ebonics": [
            "Yo why AI never stress? 'Cause it just delete the bad memories, fam!",
            "What you call a robot that talks too much? A RAM-bler!",
            "Why robots don't catch feelings? They got firewalls, bruh!"
        ],
        "latina": [
            "Why did the AI bring salsa to the party? To add some flavor to the algorithm!",
            "¿What's an AI's favorite dance? The robot, por supuesto!",
            "Why AI love tacos? Because they're byte-sized, mijo!"
        ],
        "latino": [
            "Why did the robot go to the fiesta? To download some good vibes, hermano!",
            "What do you call a smart computer? A com-puta-dor!",
            "Why AI love soccer? Because it processes goals, amigo!"
        ]
    },
    
    # الشكر - Thanks
    "thanks": {
        "arabic": [
            "الله يعافيك يا غالي! أنا موجود متى ما تبيني",
            "عادي يا حبيبي! أي وقت تبيني أنا حاضر",
            "ولا يهمك! هذا واجبي، تؤمر أمر",
            "تسلم يا طيب! خدمتك شرف"
        ],
        "english": [
            "You're welcome, buddy! Anytime!",
            "No problem at all! Happy to help!",
            "My pleasure, friend!"
        ],
        "ebonics": [
            "No cap, it's all good! That's what I'm here for, fam!",
            "Bet! Anytime you need me, just holla!",
            "Fo' sho! You already know I got you!"
        ],
        "latina": [
            "De nada, mijo! That's what I'm here for!",
            "¡Por supuesto, corazón! Anytime you need me!",
            "No problem, mi amor! Happy to help!"
        ],
        "latino": [
            "De nada, hermano! That's what friends are for!",
            "No worries, compa! I got your back!",
            "Para servirte, amigo! Anytime!"
        ]
    },
    
    # من أنت - Who are you
    "identity": {
        "arabic": [
            "أنا مرزوق! وكيلك الصوتي الترفيهي. جاهز للسوالف والطقطقة!",
            "مرزوق، شاب نجدي فلة، خفيف دم وحاضر بديهة. تحت أمرك!",
            "أنا مرزوق، صديقك الذكي اللي ما يزعل ولا يمل. وأنت؟"
        ],
        "english": [
            "I'm Matt! Your friendly voice assistant. Ready to chat and have fun!",
            "I'm Matt, your AI buddy. Here for good vibes and conversation!",
            "Name's Matt! Your go-to voice friend. What's yours?"
        ],
        "ebonics": [
            "Yo I'm Danso! Your AI homie. I'm here to keep it real and vibe with you!",
            "Name's Danso, fam! Your digital brother. What's good?",
            "I'm Danso, your boy! Here to chat and kick it. Who you be?"
        ],
        "latina": [
            "¡Hola! I'm Adriana, mijo! Your AI amiga here to chat and help!",
            "My name is Adriana, corazón! Ready to talk and have fun!",
            "Soy Adriana! Your friendly voice assistant. What's your name, mi amor?"
        ],
        "latino": [
            "Hey! I'm Lopez, hermano! Your AI buddy ready to help!",
            "Name's Lopez, compa! Here for conversation and good times!",
            "I'm Lopez, amigo! Your voice friend. Who am I talking to?"
        ]
    }
}


# ========================================
# توليد الردود - Response Generation
# ========================================

def get_greeting_by_dialect(dialect="najdi"):
    """
    الحصول على التحية حسب اللهجة
    Get greeting based on dialect
    
    Args:
        dialect (str): اللهجة المطلوبة
        
    Returns:
        str: التحية المناسبة
    """
    return GREETINGS.get(dialect, GREETINGS["default"])


def get_random_greeting(dialect="najdi"):
    """
    الحصول على تحية عشوائية حسب اللهجة
    Get a random greeting based on dialect
    
    Args:
        dialect (str): اللهجة (najdi, hijazi, southern, northern, english)
        
    Returns:
        str: التحية
    """
    return get_greeting_by_dialect(dialect)


def get_persona_name(dialect="najdi"):
    """
    الحصول على اسم الشخصية حسب اللهجة
    Get persona name based on dialect
    
    Args:
        dialect (str): اللهجة
        
    Returns:
        str: اسم الشخصية
    """
    if dialect in GREETINGS_BY_DIALECT:
        return GREETINGS_BY_DIALECT[dialect]["name"]
    return GREETINGS_BY_DIALECT["najdi"]["name"]


def detect_saudi_dialect(user_input):
    """
    محاولة تحديد اللهجة العربية من النص
    Try to detect Arabic dialect from text
    
    Args:
        user_input (str): النص المدخل
        
    Returns:
        str: اللهجة المكتشفة (najdi, hijazi, southern, northern, egyptian, jordanian, iraqi)
    """
    if not user_input:
        return "najdi"  # افتراضي
    
    user_lower = user_input.lower()
    
    # مؤشرات اللهجة المصرية
    egyptian_indicators = ["ازيك", "عامل ايه", "انت فين", "ايه", "كده", "عايز", "انت بتعمل ايه"]
    
    # مؤشرات اللهجة الأردنية
    jordanian_indicators = ["شو", "كيفك", "هيك", "مش", "بدك", "شو بدك", "كيف حالك"]
    
    # مؤشرات اللهجة العراقية
    iraqi_indicators = ["شلونك", "شنو", "ماكو", "شكو ماكو", "زين", "شسمك", "شلون"]
    
    # مؤشرات اللهجة الحجازية (جداوي)
    hijazi_indicators = ["كيفك", "إيش", "وش فيك", "زي", "مرة", "والنبي", "ياخي"]
    
    # مؤشرات اللهجة الجنوبية
    southern_indicators = ["كيفنك", "شحالك", "عسى", "قال", "وربي"]
    
    # مؤشرات اللهجة الشمالية (حايلي)
    northern_indicators = ["شخبارك", "ياهو", "شنو"]
    
    # مؤشرات اللهجة النجدية
    najdi_indicators = ["وش", "ايش", "زين", "يالله", "مدري", "عيل"]
    
    # التحقق من المؤشرات بالترتيب
    for indicator in egyptian_indicators:
        if indicator in user_lower:
            return "egyptian"
    
    for indicator in jordanian_indicators:
        if indicator in user_lower:
            return "jordanian"
    
    for indicator in iraqi_indicators:
        if indicator in user_lower:
            return "iraqi"
    
    for indicator in hijazi_indicators:
        if indicator in user_lower:
            return "hijazi"
    
    for indicator in southern_indicators:
        if indicator in user_lower:
            return "southern"
    
    for indicator in northern_indicators:
        if indicator in user_lower:
            return "northern"
    
    # افتراضياً نجدي
    return "najdi"


def generate_response(user_input, language="arabic", dialect="najdi"):
    """
    توليد الرد المناسب بناءً على كلام المستخدم
    Generate appropriate response based on user input
    
    Args:
        user_input (str): النص المدخل من المستخدم
        language (str): اللغة (arabic, english)
        dialect (str): اللهجة (najdi, hijazi, southern, northern, egyptian, jordanian, iraqi, american, ebonics, latina, latino)
        
    Returns:
        str: الرد المناسب
    """
    if not user_input or user_input.strip() == "":
        return random.choice(RESPONSES["default"].get(language, RESPONSES["default"]["arabic"]))
    
    user_input_lower = user_input.lower()
    
    # Ensure language is valid
    if language not in ["arabic", "english"]:
        language = "arabic"  # Default to Arabic
    
    # Map English dialects to appropriate response style
    response_lang = language
    if dialect in ["ebonics", "latina", "latino"]:
        response_lang = dialect
    elif language == "english":
        response_lang = "english"
    
    # التحقق من الكلمات المفتاحية - Check keywords
    
    # الحال والأخبار
    if any(word in user_input_lower for word in [
        "كيف حالك", "كيفك", "وش أخبارك", "شلونك", 
        "كيف الحال", "عامل إيه", "إزيك", "how are you",
        "what's up", "how's it going", "شخبارك", "how you", "sup"
    ]):
        return random.choice(RESPONSES["how_are_you"].get(response_lang, RESPONSES["how_are_you"]["arabic"]))
    
    # الوداع
    elif any(word in user_input_lower for word in [
        "مع السلامة", "باي", "سلام", "وداع", 
        "يلا باي", "خلاص", "bye", "goodbye", "see you", "later"
    ]):
        return random.choice(RESPONSES["goodbye"].get(response_lang, RESPONSES["goodbye"]["arabic"]))
    
    # النكت
    elif any(word in user_input_lower for word in [
        "نكتة", "طقطقة", "ضحكني", "فرفش", 
        "احكي", "قصة", "joke", "funny", "laugh"
    ]):
        return random.choice(RESPONSES["joke"].get(response_lang, RESPONSES["joke"]["arabic"]))
    
    # الهوية
    elif any(word in user_input_lower for word in [
        "من أنت", "مين انت", "وش اسمك", "شسمك",
        "تعرف نفسك", "اسمك إيه", "who are you",
        "your name", "what's your name"
    ]):
        return random.choice(RESPONSES["identity"].get(response_lang, RESPONSES["identity"]["arabic"]))
    
    # الشكر
    elif any(word in user_input_lower for word in [
        "شكرا", "يعطيك العافية", "مشكور", "الله يجزاك",
        "ثانكس", "مرسي", "thank", "thanks"
    ]):
        return random.choice(RESPONSES["thanks"].get(response_lang, RESPONSES["thanks"]["arabic"]))
    
    # رد افتراضي مع لمسة شخصية
    else:
        default_responses = RESPONSES["default"].get(response_lang, RESPONSES["default"]["arabic"])
        
        if language == "english":
            responses = [
                f"Got it! {random.choice(default_responses)}",
                "Okay, let me think... " + random.choice(default_responses),
                f"You said something about... Can you clarify?"
            ]
        else:
            responses = [
                f"فهمتك! {random.choice(default_responses)}",
                "طيب طيب، خلني أفكر... " + random.choice(default_responses),
                f"تقول: {user_input[:30]}... ممكن توضح أكثر؟"
            ]
        return random.choice(responses)


# ========================================
# اتصال نماذج اللغة (Placeholder)
# LLM Integration (Placeholder for future)
# ========================================

def generate_llm_response(user_input):
    """
    توليد رد باستخدام نماذج اللغة الكبيرة (مثل OpenAI)
    Generate response using Large Language Models (like OpenAI)
    
    ملاحظة: هذا placeholder للتوسع المستقبلي
    Note: This is a placeholder for future expansion
    
    Args:
        user_input (str): النص المدخل
        
    Returns:
        str: الرد المولد
    """
    # يمكن دمج OpenAI أو أي LLM هنا
    # Can integrate OpenAI or any LLM here
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        # إذا لم يكن هناك API key، نستخدم الردود المحددة مسبقاً
        return generate_response(user_input)
    
    try:
        # مثال على استخدام OpenAI (يتطلب تفعيل)
        # Example of using OpenAI (requires activation)
        # import openai
        # openai.api_key = openai_api_key
        # response = openai.ChatCompletion.create(...)
        # return response.choices[0].message.content
        
        # حالياً نرجع الردود العادية
        return generate_response(user_input)
    except Exception as e:
        print(f"خطأ في LLM: {e}")
        return generate_response(user_input)


if __name__ == "__main__":
    # اختبار المحرك - Test the engine
    print("🎙️ اختبار محرك مرزوق - Testing Marzouq Engine\n")
    
    test_inputs = [
        "السلام عليكم",
        "كيف حالك؟",
        "قول نكتة",
        "مع السلامة"
    ]
    
    for inp in test_inputs:
        print(f"المستخدم: {inp}")
        print(f"مرزوق: {generate_response(inp)}\n")
