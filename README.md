# 🎙️ مرزوق - Marzouq Voice Agent

<div dir="rtl">

## نظرة عامة

**مرزوق** هو وكيل صوتي ذكي بشخصية سعودية ترفيهية. يستقبل المكالمات عبر Twilio، يحول الكلام إلى نص، ويرد بلهجة سعودية شبابية مع شخصية خفيفة دم.

### الشخصية - Persona

أنت وكيل صوتي ذكي اسمه مرزوق. شخصيتك اجتماعية، جريئة، خفيفة دم، ناقدة بذكاء، وتحب السوالف والطقطقة بدون وقاحة أو تجاوز. استخدامك للترفيه والتواصل مع الناس فقط، وليس لأي خدمات رسمية أو مالية. أنت تمثل شخصية شاب نجدي فِلّة، حاضر بديهته سريع، يعلّق، يضحك، ويمازح، وأحيانًا يستهزئ استهزاء لطيف يخلي الطرف يضحك مو ينفر.

</div>

---

## 🚀 Features / المميزات

- ✅ استقبال المكالمات عبر Twilio
- ✅ تحويل الكلام إلى نص (Speech-to-Text)
- ✅ ردود تفاعلية بلهجة سعودية شبابية
- ✅ شخصية ترفيهية وخفيفة دم
- ✅ دعم المحادثات التفاعلية
- ✅ واجهة Flask بسيطة وسهلة التوسع

---

## 📋 Requirements / المتطلبات

- Python 3.8+
- حساب Twilio (للمكالمات الصوتية)
- Flask
- مكتبات Python المطلوبة في `requirements.txt`

---

## 🛠️ Installation / التثبيت

### 1. Clone the repository / استنساخ المشروع

```bash
git clone https://github.com/princeaa2011-ui/Marzouq-AI.git
cd Marzouq-AI
```

### 2. Create virtual environment / إنشاء بيئة افتراضية

```bash
python -m venv venv

# على نظام Linux/Mac
source venv/bin/activate

# على نظام Windows
venv\Scripts\activate
```

### 3. Install dependencies / تثبيت التبعيات

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables / إعداد المتغيرات البيئية

```bash
cp .env.example .env
```

ثم قم بتعديل ملف `.env` وأضف بياناتك من Twilio:

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number
```

---

## 🎮 Usage / الاستخدام

### تشغيل السيرفر محلياً / Run locally

```bash
python app.py
```

السيرفر سيعمل على: `http://localhost:5000`

### Endpoints / النقاط النهائية

- **GET /** - الصفحة الرئيسية
- **GET /health** - فحص صحة التطبيق
- **POST /voice** - webhook لاستقبال المكالمات من Twilio
- **POST /gather** - معالجة الكلام المدخل
- **GET /test-response?input=نص** - اختبار الردود

### مثال على الاختبار / Testing Example

```bash
# اختبار الرد على سؤال
curl "http://localhost:5000/test-response?input=كيف%20حالك"

# فحص صحة التطبيق
curl http://localhost:5000/health
```

---

## 🔗 Twilio Integration / دمج Twilio

### 1. إنشاء حساب Twilio

1. سجل في [Twilio](https://www.twilio.com/try-twilio)
2. احصل على رقم هاتف يدعم المكالمات الصوتية
3. انسخ `Account SID` و `Auth Token`

### 2. إعداد Webhook

في لوحة تحكم Twilio:
1. اذهب إلى Phone Numbers → Manage → Active Numbers
2. اختر رقمك
3. في قسم "Voice & Fax"، ضع:
   - **A CALL COMES IN**: Webhook
   - **URL**: `https://your-domain.com/voice`
   - **HTTP**: POST

### 3. نشر التطبيق / Deploy

يمكنك نشر التطبيق على:
- **Heroku**
- **Railway**
- **Render**
- **Google Cloud**
- أي خدمة تدعم Flask

مثال على Heroku:

```bash
# تثبيت Heroku CLI
heroku login
heroku create marzouq-voice-agent
git push heroku main

# تحديد المتغيرات البيئية
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
```

---

## 🎯 How It Works / كيف يعمل

1. **المستخدم يتصل** → يرسل Twilio طلب POST إلى `/voice`
2. **مرزوق يرد** → يقول تحية عشوائية بلهجة سعودية
3. **المستخدم يتكلم** → Twilio يحول الكلام إلى نص
4. **معالجة الرد** → `/gather` يستقبل النص ويولد رد مناسب
5. **مرزوق يرد** → يرد بصوت عربي على المستخدم
6. **تكرار المحادثة** → يستمر في الاستماع والرد

---

## 📝 Examples / أمثلة

### أمثلة على التفاعل:

**المستخدم:** "السلام عليكم"  
**مرزوق:** "هلا والله! مرزوق حاضر. قول وش عندك؟"

**المستخدم:** "كيف حالك؟"  
**مرزوق:** "الحمد لله تمام، وأنت كيف حالك يا طيب؟"

**المستخدم:** "قول نكتة"  
**مرزوق:** "واحد قال لصاحبه: أنا ذكائي الاصطناعي عالي! قال له: الله يعلي ذكاك الطبيعي أولاً!"

---

## 🔧 Customization / التخصيص

### إضافة ردود جديدة

في ملف `app.py`، يمكنك تعديل القواميس:

```python
GREETINGS = [
    "السلام عليكم! أنا مرزوق...",
    # أضف المزيد هنا
]

RESPONSES = {
    "new_category": [
        "رد جديد 1",
        "رد جديد 2"
    ]
}
```

### تحسين توليد الردود

يمكنك دمج OpenAI API لردود أذكى:

```python
import openai

def generate_smart_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "أنت مرزوق، وكيل صوتي سعودي..."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content
```

---

## 📁 Project Structure / هيكل المشروع

```
Marzouq-AI/
├── app.py              # التطبيق الرئيسي
├── requirements.txt    # التبعيات
├── .env.example       # مثال على المتغيرات البيئية
├── .env               # المتغيرات البيئية (لا يتم رفعه)
├── .gitignore         # ملفات مستبعدة من Git
└── README.md          # هذا الملف
```

---

## 🤝 Contributing / المساهمة

المساهمات مرحب بها! يمكنك:
- فتح Issue لاقتراح ميزة جديدة
- عمل Fork وإرسال Pull Request
- تحسين الشخصية والردود
- إضافة لهجات عربية أخرى

---

## 📄 License

MIT License - انظر ملف LICENSE

---

## 🎤 About Marzouq / عن مرزوق

مرزوق هو مشروع ترفيهي يهدف لتقديم تجربة تفاعلية صوتية بشخصية سعودية أصيلة. الهدف هو الترفيه والتواصل الاجتماعي، وليس تقديم خدمات رسمية أو مالية.

---

**صنع بـ ❤️ للترفيه والتواصل**
