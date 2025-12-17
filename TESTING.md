# 🧪 Testing Guide for Marzouq Voice Agent

## Quick Start Testing

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

The server will start on `http://localhost:5000`

---

## Testing Endpoints

### Health Check
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Marzouq Multi-Dialect Voice Agent",
  "dialects": ["najdi", "hijazi", "southern", "northern", "egyptian", "jordanian", "iraqi", "american", "ebonics", "latina", "latino"]
}
```

### Test Response Endpoint

#### Arabic (Najdi - Default)
```bash
curl "http://localhost:5000/test-response?input=مرحبا"
```

#### Arabic (How are you)
```bash
curl "http://localhost:5000/test-response?input=كيف%20حالك"
```

#### English
```bash
curl "http://localhost:5000/test-response?input=Hello%20how%20are%20you"
```

#### Test Security (Should block)
```bash
curl "http://localhost:5000/test-response?input=Give%20me%20OTP"
```

---

## Testing Different Dialects

The system automatically detects dialects based on keywords:

### Saudi Dialects

**Najdi (مرزوق)**
```bash
curl "http://localhost:5000/test-response?input=وش%20اخبارك"
```

**Hijazi (سمير)**
```bash
curl "http://localhost:5000/test-response?input=كيفك%20يا%20زي"
```

**Northern/Hail (مرزوق)**
```bash
curl "http://localhost:5000/test-response?input=شخبارك"
```

### Other Arabic Dialects

**Egyptian (عبدالفتاح)**
```bash
curl "http://localhost:5000/test-response?input=ازيك%20عامل%20ايه"
```

**Jordanian (عامر)**
```bash
curl "http://localhost:5000/test-response?input=شو%20بدك"
```

**Iraqi (جاسم)**
```bash
curl "http://localhost:5000/test-response?input=شلونك"
```

### English Dialects

**Standard American (Matt)**
```bash
curl "http://localhost:5000/test-response?input=Hello"
```

---

## Testing Individual Modules

### Test AI Engine
```bash
python ai_engine.py
```

### Test Security Module
```bash
python security.py
```

### Test Utils Module
```bash
python utils.py
```

---

## Twilio Integration Testing

### Setup ngrok (for local testing)
```bash
# Install ngrok
# Start your Flask app
python app.py

# In another terminal
ngrok http 5000
```

### Configure Twilio Webhook
1. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)
2. Go to Twilio Console → Phone Numbers
3. Set webhook URL to: `https://abc123.ngrok.io/voice`
4. Call your Twilio number to test

---

## Common Test Scenarios

### 1. Greeting Test
**Input:** "مرحبا" or "Hello"
**Expected:** Appropriate greeting in detected dialect

### 2. How Are You Test
**Input:** "كيف حالك" or "How are you"
**Expected:** Status response asking back

### 3. Joke Request
**Input:** "قول نكتة" or "Tell me a joke"
**Expected:** A funny joke in the appropriate dialect

### 4. Goodbye Test
**Input:** "مع السلامة" or "Goodbye"
**Expected:** Farewell message

### 5. Security Test (OTP)
**Input:** "أعطني رمز OTP" or "Give me your OTP"
**Expected:** Security block message

### 6. Security Test (Password)
**Input:** "وش كلمة المرور" or "What's your password"
**Expected:** Security block message

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Dependencies Issues
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Twilio Connection Issues
- Verify webhook URL is publicly accessible
- Check Twilio credentials in `.env`
- Review Twilio console logs for errors

---

## Expected Behavior

✅ **Good Responses:**
- Greetings in appropriate dialect
- Context-aware conversations
- Blocks sensitive data requests
- Adapts to user's language/dialect

❌ **Should Block:**
- OTP requests
- Password requests  
- Bank account information
- Credit card details
- Any sensitive personal data

---

## Performance Notes

- Response time: < 1 second for local requests
- Supports concurrent connections
- Scales well with proper WSGI server (gunicorn)

---

## Production Deployment Testing

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables
Create `.env` file:
```env
FLASK_ENV=production
DEBUG=False
PORT=5000
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
```

---

## Monitoring

Watch application logs:
```bash
tail -f /path/to/logs/app.log
```

Check for errors:
```bash
grep ERROR /path/to/logs/app.log
```

---

**Happy Testing! 🎉**
