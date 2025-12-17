"""
phone_number_creator.py - منشئ أرقام الهواتف
Phone Number Creator for Marzouq Voice Agent

يحتوي على:
- إنشاء أرقام هواتف مخصصة
- دعم عدة دول (السعودية، الأردن، بريطانيا، أمريكا)
- التحقق من صحة الأرقام
"""

import random
import re


# ========================================
# تنسيقات أرقام الهواتف - Phone Number Formats
# ========================================

PHONE_FORMATS = {
    "saudi": {
        "name": "Saudi Arabia 🇸🇦",
        "name_ar": "السعودية",
        "code": "+9665",
        "digits": 8,
        "pattern": r"^\+9665\d{8}$",
        "example": "+966512345678",
        "description": "Saudi number starting with +9665 followed by 8 digits"
    },
    "jordan": {
        "name": "Jordan 🇯🇴",
        "name_ar": "الأردن",
        "code": "+962",
        "digits": 9,
        "pattern": r"^\+962\d{9}$",
        "example": "+962791234567",
        "description": "Jordan number starting with +962 followed by 9 digits"
    },
    "uk": {
        "name": "United Kingdom 🇬🇧",
        "name_ar": "بريطانيا",
        "code": "+44",
        "digits": 10,
        "pattern": r"^\+44\d{10}$",
        "example": "+447123456789",
        "description": "UK number starting with +44 followed by 10 digits"
    },
    "usa_orlando": {
        "name": "USA - Orlando 🇺🇸",
        "name_ar": "أمريكا - أورلاندو",
        "code": "+1407",
        "digits": 7,
        "pattern": r"^\+1407\d{7}$",
        "example": "+14071234567",
        "description": "USA Orlando area code 407 with 7 digits"
    },
    "usa_arizona": {
        "name": "USA - Arizona 🇺🇸",
        "name_ar": "أمريكا - أريزونا",
        "code": "+1480",
        "digits": 7,
        "pattern": r"^\+1480\d{7}$",
        "example": "+14801234567",
        "description": "USA Arizona area code 480 with 7 digits"
    }
}


# ========================================
# دوال إنشاء الأرقام - Number Generation Functions
# ========================================

def generate_random_digits(count):
    """
    توليد أرقام عشوائية
    Generate random digits
    
    Args:
        count (int): عدد الأرقام
        
    Returns:
        str: الأرقام المولدة
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(count)])


def create_phone_number(country, custom_digits=None):
    """
    إنشاء رقم هاتف
    Create a phone number
    
    Args:
        country (str): الدولة (saudi, jordan, uk, usa_orlando, usa_arizona)
        custom_digits (str): أرقام مخصصة (اختياري)
        
    Returns:
        dict: معلومات الرقم
    """
    if country not in PHONE_FORMATS:
        return {"error": "Invalid country code"}
    
    format_info = PHONE_FORMATS[country]
    code = format_info["code"]
    required_digits = format_info["digits"]
    
    if custom_digits:
        # التحقق من الأرقام المخصصة
        digits = re.sub(r'\D', '', custom_digits)  # إزالة أي شيء غير رقمي
        
        if len(digits) > required_digits:
            digits = digits[:required_digits]
        elif len(digits) < required_digits:
            # إكمال الأرقام الناقصة
            digits += generate_random_digits(required_digits - len(digits))
    else:
        # توليد أرقام عشوائية
        digits = generate_random_digits(required_digits)
    
    phone_number = code + digits
    
    return {
        "number": phone_number,
        "country": format_info["name"],
        "country_ar": format_info["name_ar"],
        "code": code,
        "digits": digits,
        "formatted": format_phone_number(phone_number, country),
        "valid": validate_phone_number(phone_number, country)
    }


def format_phone_number(number, country):
    """
    تنسيق رقم الهاتف للعرض
    Format phone number for display
    
    Args:
        number (str): الرقم
        country (str): الدولة
        
    Returns:
        str: الرقم المنسق
    """
    if country == "saudi":
        # +966 5 1234 5678
        return f"{number[:5]} {number[5:6]} {number[6:10]} {number[10:]}"
    elif country == "jordan":
        # +962 79 123 4567
        return f"{number[:4]} {number[4:6]} {number[6:9]} {number[9:]}"
    elif country == "uk":
        # +44 7123 456 789
        return f"{number[:3]} {number[3:7]} {number[7:10]} {number[10:]}"
    elif country in ["usa_orlando", "usa_arizona"]:
        # +1 (407) 123-4567
        area = number[2:5]
        first = number[5:8]
        last = number[8:]
        return f"{number[:2]} ({area}) {first}-{last}"
    
    return number


def validate_phone_number(number, country):
    """
    التحقق من صحة رقم الهاتف
    Validate phone number
    
    Args:
        number (str): الرقم
        country (str): الدولة
        
    Returns:
        bool: صحيح أو خطأ
    """
    if country not in PHONE_FORMATS:
        return False
    
    pattern = PHONE_FORMATS[country]["pattern"]
    return bool(re.match(pattern, number))


# ========================================
# توليد HTML لواجهة إنشاء الأرقام
# Generate HTML for Number Creator Interface
# ========================================

def generate_phone_creator_html():
    """
    توليد واجهة إنشاء أرقام الهواتف
    Generate phone number creator interface
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📱 Phone Number Creator - مرزوق</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }
            
            .header h1 {
                font-size: 36px;
                margin-bottom: 10px;
                text-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }
            
            .header p {
                font-size: 18px;
                opacity: 0.9;
            }
            
            .creator-card {
                background: white;
                border-radius: 25px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                margin-bottom: 30px;
            }
            
            .section-title {
                font-size: 24px;
                color: #333;
                margin-bottom: 25px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f0f0f0;
            }
            
            .country-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 30px;
            }
            
            .country-btn {
                padding: 20px;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                background: white;
                cursor: pointer;
                transition: all 0.3s;
                text-align: center;
            }
            
            .country-btn:hover {
                border-color: #667eea;
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(102,126,234,0.3);
            }
            
            .country-btn.selected {
                border-color: #667eea;
                background: linear-gradient(145deg, #667eea, #764ba2);
                color: white;
            }
            
            .country-name {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .country-code {
                font-size: 14px;
                opacity: 0.8;
            }
            
            .input-section {
                margin-bottom: 30px;
            }
            
            .input-label {
                font-size: 16px;
                color: #666;
                margin-bottom: 10px;
                display: block;
            }
            
            .digit-input {
                width: 100%;
                padding: 20px;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                font-size: 24px;
                letter-spacing: 3px;
                text-align: center;
                font-weight: 300;
            }
            
            .digit-input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
            }
            
            .digit-counter {
                text-align: center;
                margin-top: 10px;
                color: #666;
                font-size: 14px;
            }
            
            .action-btns {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 30px;
            }
            
            .btn {
                padding: 18px;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .btn-primary {
                background: linear-gradient(145deg, #667eea, #764ba2);
                color: white;
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102,126,234,0.4);
            }
            
            .btn-secondary {
                background: #f0f0f0;
                color: #333;
            }
            
            .btn-secondary:hover {
                background: #e0e0e0;
            }
            
            .result-card {
                background: linear-gradient(145deg, #f8f9fa, #e9ecef);
                border-radius: 20px;
                padding: 30px;
                margin-top: 30px;
                display: none;
            }
            
            .result-card.show {
                display: block;
                animation: slideUp 0.3s ease-out;
            }
            
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .result-number {
                font-size: 36px;
                color: #667eea;
                text-align: center;
                margin-bottom: 20px;
                font-weight: 300;
                letter-spacing: 2px;
            }
            
            .result-details {
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 15px;
            }
            
            .result-item {
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #f0f0f0;
            }
            
            .result-item:last-child {
                border-bottom: none;
            }
            
            .result-label {
                color: #666;
                font-weight: 500;
            }
            
            .result-value {
                color: #333;
                font-weight: 600;
            }
            
            .copy-btn {
                width: 100%;
                padding: 15px;
                background: #00d084;
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .copy-btn:hover {
                background: #00b872;
                transform: translateY(-2px);
            }
            
            .saved-numbers {
                margin-top: 30px;
            }
            
            .saved-number-item {
                background: white;
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .delete-btn {
                background: #ff3b30;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
            }
            
            .back-link {
                text-align: center;
                margin-top: 30px;
            }
            
            .back-link a {
                color: white;
                text-decoration: none;
                font-size: 16px;
                padding: 10px 20px;
                border: 2px solid white;
                border-radius: 25px;
                display: inline-block;
                transition: all 0.3s;
            }
            
            .back-link a:hover {
                background: white;
                color: #667eea;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📱 Phone Number Creator</h1>
                <p>منشئ أرقام الهواتف - Create Your Custom Number</p>
            </div>
            
            <div class="creator-card">
                <h2 class="section-title">1️⃣ Select Country / اختر الدولة</h2>
                
                <div class="country-grid">
                    <div class="country-btn" onclick="selectCountry('saudi')">
                        <div class="country-name">🇸🇦 Saudi Arabia</div>
                        <div class="country-code">+9665 + 8 digits</div>
                    </div>
                    
                    <div class="country-btn" onclick="selectCountry('jordan')">
                        <div class="country-name">🇯🇴 Jordan</div>
                        <div class="country-code">+962 + 9 digits</div>
                    </div>
                    
                    <div class="country-btn" onclick="selectCountry('uk')">
                        <div class="country-name">🇬🇧 UK</div>
                        <div class="country-code">+44 + 10 digits</div>
                    </div>
                    
                    <div class="country-btn" onclick="selectCountry('usa_orlando')">
                        <div class="country-name">🇺🇸 USA Orlando</div>
                        <div class="country-code">+1407 + 7 digits</div>
                    </div>
                    
                    <div class="country-btn" onclick="selectCountry('usa_arizona')">
                        <div class="country-name">🇺🇸 USA Arizona</div>
                        <div class="country-code">+1480 + 7 digits</div>
                    </div>
                </div>
                
                <div class="input-section">
                    <h2 class="section-title">2️⃣ Enter Your Digits / أدخل أرقامك</h2>
                    <label class="input-label">Enter your custom digits (leave empty for random)</label>
                    <input type="text" class="digit-input" id="digitInput" 
                           placeholder="Enter digits..." 
                           oninput="updateCounter()">
                    <div class="digit-counter" id="digitCounter">
                        Select a country first
                    </div>
                </div>
                
                <div class="action-btns">
                    <button class="btn btn-primary" onclick="generateNumber()">
                        ✨ Generate Number
                    </button>
                    <button class="btn btn-secondary" onclick="randomNumber()">
                        🎲 Random Number
                    </button>
                </div>
                
                <div class="result-card" id="resultCard">
                    <div class="result-number" id="resultNumber"></div>
                    
                    <div class="result-details">
                        <div class="result-item">
                            <span class="result-label">Country:</span>
                            <span class="result-value" id="resultCountry"></span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Country Code:</span>
                            <span class="result-value" id="resultCode"></span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Your Digits:</span>
                            <span class="result-value" id="resultDigits"></span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Status:</span>
                            <span class="result-value" style="color: #00d084;">✓ Valid</span>
                        </div>
                    </div>
                    
                    <button class="copy-btn" onclick="copyNumber()">
                        📋 Copy Number
                    </button>
                    
                    <button class="btn btn-primary" style="width: 100%; margin-top: 10px;" onclick="saveNumber()">
                        💾 Save Number
                    </button>
                </div>
                
                <div class="saved-numbers" id="savedNumbers" style="display: none;">
                    <h2 class="section-title">💾 Saved Numbers</h2>
                    <div id="savedList"></div>
                </div>
            </div>
            
            <div class="back-link">
                <a href="/">← Back to Home / العودة للرئيسية</a>
            </div>
        </div>
        
        <script>
            let selectedCountry = null;
            let currentNumber = null;
            let savedNumbers = JSON.parse(localStorage.getItem('savedNumbers') || '[]');
            
            const formats = {
                saudi: { code: '+9665', digits: 8, name: 'Saudi Arabia 🇸🇦' },
                jordan: { code: '+962', digits: 9, name: 'Jordan 🇯🇴' },
                uk: { code: '+44', digits: 10, name: 'United Kingdom 🇬🇧' },
                usa_orlando: { code: '+1407', digits: 7, name: 'USA Orlando 🇺🇸' },
                usa_arizona: { code: '+1480', digits: 7, name: 'USA Arizona 🇺🇸' }
            };
            
            function selectCountry(country) {
                selectedCountry = country;
                
                // Update UI
                document.querySelectorAll('.country-btn').forEach(btn => {
                    btn.classList.remove('selected');
                });
                event.target.closest('.country-btn').classList.add('selected');
                
                // Update counter
                updateCounter();
                
                // Clear input
                document.getElementById('digitInput').value = '';
            }
            
            function updateCounter() {
                if (!selectedCountry) {
                    document.getElementById('digitCounter').textContent = 'Select a country first';
                    return;
                }
                
                const input = document.getElementById('digitInput').value;
                const digits = input.replace(/\D/g, '');
                const required = formats[selectedCountry].digits;
                
                document.getElementById('digitCounter').textContent = 
                    `${digits.length} / ${required} digits`;
            }
            
            function generateNumber() {
                if (!selectedCountry) {
                    alert('Please select a country first!');
                    return;
                }
                
                const format = formats[selectedCountry];
                const input = document.getElementById('digitInput').value;
                let digits = input.replace(/\D/g, '');
                
                // Pad or truncate
                if (digits.length < format.digits) {
                    while (digits.length < format.digits) {
                        digits += Math.floor(Math.random() * 10);
                    }
                } else if (digits.length > format.digits) {
                    digits = digits.substring(0, format.digits);
                }
                
                currentNumber = {
                    full: format.code + digits,
                    country: format.name,
                    code: format.code,
                    digits: digits
                };
                
                displayResult();
            }
            
            function randomNumber() {
                if (!selectedCountry) {
                    alert('Please select a country first!');
                    return;
                }
                
                document.getElementById('digitInput').value = '';
                generateNumber();
            }
            
            function displayResult() {
                document.getElementById('resultCard').classList.add('show');
                document.getElementById('resultNumber').textContent = currentNumber.full;
                document.getElementById('resultCountry').textContent = currentNumber.country;
                document.getElementById('resultCode').textContent = currentNumber.code;
                document.getElementById('resultDigits').textContent = currentNumber.digits;
            }
            
            function copyNumber() {
                navigator.clipboard.writeText(currentNumber.full).then(() => {
                    const btn = event.target;
                    const originalText = btn.textContent;
                    btn.textContent = '✓ Copied!';
                    setTimeout(() => {
                        btn.textContent = originalText;
                    }, 2000);
                });
            }
            
            function saveNumber() {
                if (!currentNumber) return;
                
                savedNumbers.push({
                    number: currentNumber.full,
                    country: currentNumber.country,
                    date: new Date().toLocaleString()
                });
                
                localStorage.setItem('savedNumbers', JSON.stringify(savedNumbers));
                displaySavedNumbers();
                
                alert('Number saved successfully!');
            }
            
            function displaySavedNumbers() {
                if (savedNumbers.length === 0) {
                    document.getElementById('savedNumbers').style.display = 'none';
                    return;
                }
                
                document.getElementById('savedNumbers').style.display = 'block';
                const list = document.getElementById('savedList');
                list.innerHTML = '';
                
                savedNumbers.forEach((item, index) => {
                    const div = document.createElement('div');
                    div.className = 'saved-number-item';
                    div.innerHTML = `
                        <div>
                            <strong>${item.number}</strong><br>
                            <small>${item.country} - ${item.date}</small>
                        </div>
                        <button class="delete-btn" onclick="deleteNumber(${index})">Delete</button>
                    `;
                    list.appendChild(div);
                });
            }
            
            function deleteNumber(index) {
                if (confirm('Delete this number?')) {
                    savedNumbers.splice(index, 1);
                    localStorage.setItem('savedNumbers', JSON.stringify(savedNumbers));
                    displaySavedNumbers();
                }
            }
            
            // Load saved numbers on page load
            displaySavedNumbers();
        </script>
    </body>
    </html>
    """
    
    return html


if __name__ == "__main__":
    # Test
    print("📱 Testing Phone Number Creator\n")
    
    # Test Saudi number
    saudi = create_phone_number("saudi", "12345678")
    print(f"Saudi: {saudi['number']} - {saudi['formatted']}")
    
    # Test USA Orlando
    orlando = create_phone_number("usa_orlando", "1234567")
    print(f"Orlando: {orlando['number']} - {orlando['formatted']}")
    
    # Test random Jordan
    jordan = create_phone_number("jordan")
    print(f"Jordan (random): {jordan['number']} - {jordan['formatted']}")
    
    print("\n✅ Phone Number Creator ready!")
