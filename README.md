# مرزوق AI - Marzouq AI 🎙️

وكيل صوتي ترفيهي ذكي بشخصية سعودية شبابية خفيفة الدم!

## 📖 وصف المشروع

**مرزوق** هو وكيل صوتي ترفيهي يستقبل مكالمات عبر Twilio، يحوّل الكلام إلى نص، ويرد بلهجة سعودية شبابية أو عربية عامية بطريقة خفيفة ومسلية.

### 🎭 الشخصية

أنت وكيل صوتي ذكي اسمه مرزوق. شخصيتك اجتماعية، جريئة، خفيفة دم، ناقدة بذكاء، وتحب السوالف والطقطقة بدون وقاحة أو تجاوز. استخدامك للترفيه والتواصل مع الناس فقط، وليس لأي خدمات رسمية أو مالية.

أنت تمثل شخصية شاب نجدي فِلّة، حاضر بديهته سريع، يعلّق، يضحك، ويمازح، وأحيانًا يستهزئ استهزاء لطيف يخلي الطرف يضحك مو ينفر.

## 🚀 المتطلبات

- Python 3.8 أو أحدث
- حساب Twilio مع رقم هاتف
- مفتاح API من OpenAI
- ngrok أو أي خدمة نفق (tunnel) لتطوير محلي

## 📦 التثبيت

### 1. استنساخ المشروع

```bash
git clone https://github.com/princeaa2011-ui/Marzouq-AI.git
cd Marzouq-AI
```

### 2. إنشاء بيئة افتراضية

```bash
python -m venv venv
source venv/bin/activate  # في Linux/Mac
# أو
venv\Scripts\activate  # في Windows
```

### 3. تثبيت التبعيات

```bash
pip install -r requirements.txt
```

### 4. إعداد المتغيرات البيئية

انسخ ملف `.env.example` إلى `.env`:

```bash
cp .env.example .env
```

عدّل الملف `.env` وأضف معلوماتك:

```env
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎮 التشغيل

### تشغيل محلي (للتطوير)

```bash
# تأكد من تفعيل FLASK_ENV=development في ملف .env
python app.py
```

السيرفر سيشتغل على `http://localhost:5000`

### تشغيل في الإنتاج

للإنتاج، استخدم **gunicorn** بدلاً من Flask development server:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

أو مع المزيد من الخيارات:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --access-logfile - app:app
```

### استخدام ngrok للتطوير

في نافذة terminal ثانية:

```bash
ngrok http 5000
```

انسخ الرابط الذي يعطيك ngrok (مثل: `https://xxxx.ngrok.io`)

## ⚙️ إعداد Twilio

1. افتح [Twilio Console](https://console.twilio.com/)
2. اختر رقمك في Twilio
3. في قسم "Voice & Fax"، تحت "A CALL COMES IN":
   - اختر "Webhook"
   - أضف الرابط: `https://your-ngrok-url.ngrok.io/voice`
   - اختر "HTTP POST"
4. احفظ التغييرات

## 📞 الاستخدام

اتصل على رقم Twilio الخاص بك، ومرزوق سيرد عليك!

مثال على محادثة:
```
مرزوق: السلام عليكم! أنا مرزوق، وكيلك الصوتي. قول لي، وش تبغى؟
أنت: كيف الحال؟
مرزوق: الحمدلله، تمام! أنت كيفك؟ شكلك ناوي تسولف؟
```

## 📁 هيكل المشروع

```
Marzouq-AI/
├── app.py              # الملف الرئيسي للتطبيق
├── requirements.txt    # تبعيات Python
├── .env.example       # مثال للمتغيرات البيئية
├── .gitignore         # ملفات متجاهلة من Git
├── README.md          # التوثيق (هذا الملف)
└── LICENSE            # الترخيص
```

## 🛠️ التقنيات المستخدمة

- **Flask**: إطار عمل الويب
- **Twilio**: خدمة المكالمات الهاتفية
- **OpenAI GPT-4**: الذكاء الاصطناعي للردود
- **Python-dotenv**: إدارة المتغيرات البيئية

## 🔧 نقاط النهاية (Endpoints)

- `GET /health` - فحص صحة السيرفر
- `POST /voice` - استقبال المكالمات من Twilio
- `POST /process_speech` - معالجة الكلام والرد
- `POST /goodbye` - إنهاء المكالمة

## 🎯 الميزات

✅ استقبال مكالمات عبر Twilio  
✅ تحويل الصوت إلى نص تلقائياً  
✅ ردود ذكية بلهجة سعودية عامية  
✅ شخصية خفيفة دم ومسلية  
✅ تعليقات بالعربي في الكود  

## 📝 ملاحظات

- المشروع للترفيه فقط وليس للاستخدامات الرسمية أو المالية
- تأكد من وجود رصيد كافٍ في حساب Twilio وOpenAI
- الردود الصوتية تستخدم Google Text-to-Speech من Twilio

## 🤝 المساهمة

نرحب بالمساهمات! افتح Issue أو Pull Request.

## 📄 الترخيص

هذا المشروع مرخص تحت MIT License.

## 💬 تواصل

إذا عندك أي أسئلة أو اقتراحات، لا تتردد تفتح Issue في GitHub!

---

صنع بـ ❤️ للمجتمع العربي
