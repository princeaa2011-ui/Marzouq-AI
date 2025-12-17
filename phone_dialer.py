"""
phone_dialer.py - واجهة الاتصال الهاتفي
Phone Dialer Interface for Marzouq Voice Agent

يحتوي على:
- لوحة الاتصال الرقمية (0-9, *, #)
- زر الاتصال
- زر إنهاء المكالمة
- زر كتم الصوت/الميكروفون
"""


# ========================================
# لوحة الاتصال - Phone Dialer
# ========================================

PHONE_DIALER = {
    # الأرقام - Numeric Keypad
    "keypad": [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["*", "0", "#"]
    ],
    
    # أزرار التحكم - Control Buttons
    "controls": {
        "call": {
            "icon": "📞",
            "label_en": "Call",
            "label_ar": "اتصال",
            "color": "#4CAF50"  # Green
        },
        "hangup": {
            "icon": "📵",
            "label_en": "Hang Up",
            "label_ar": "إنهاء",
            "color": "#f44336"  # Red
        },
        "mute": {
            "icon": "🎤",
            "label_en": "Mute",
            "label_ar": "كتم الصوت",
            "color": "#FF9800"  # Orange
        },
        "unmute": {
            "icon": "🔇",
            "label_en": "Unmute",
            "label_ar": "إلغاء الكتم",
            "color": "#2196F3"  # Blue
        },
        "delete": {
            "icon": "⌫",
            "label_en": "Delete",
            "label_ar": "حذف",
            "color": "#9E9E9E"  # Gray
        },
        "clear": {
            "icon": "⌧",
            "label_en": "Clear",
            "label_ar": "مسح الكل",
            "color": "#757575"  # Dark Gray
        }
    },
    
    # حالات المكالمة - Call States
    "states": {
        "idle": "جاهز / Ready",
        "dialing": "جاري الاتصال / Dialing",
        "ringing": "رنين / Ringing",
        "connected": "متصل / Connected",
        "muted": "مكتوم / Muted",
        "ended": "انتهت / Ended"
    }
}


# ========================================
# دوال مساعدة - Helper Functions
# ========================================

def format_phone_number(number, country_code="+966"):
    """
    تنسيق رقم الهاتف
    Format phone number
    
    Args:
        number (str): الرقم
        country_code (str): كود الدولة
        
    Returns:
        str: الرقم المنسق
    """
    # إزالة أي رموز غير رقمية
    clean_number = ''.join(c for c in number if c.isdigit() or c in ['*', '#'])
    
    # إضافة كود الدولة إذا لزم الأمر
    if country_code and not clean_number.startswith('+'):
        return f"{country_code}{clean_number}"
    
    return clean_number


def validate_phone_number(number):
    """
    التحقق من صحة رقم الهاتف
    Validate phone number
    
    Args:
        number (str): الرقم
        
    Returns:
        bool: صحيح أو خطأ
    """
    # يجب أن يحتوي على أرقام فقط (مع * و #)
    valid_chars = set('0123456789*#+')
    return all(c in valid_chars for c in number) and len(number) > 0


def generate_dialer_html():
    """
    توليد HTML للوحة الاتصال بتصميم iPhone 17 Max Pro
    Generate HTML for phone dialer with iPhone 17 Max Pro style
    
    Returns:
        str: HTML code
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📞 Phone Dialer - مرزوق</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                -webkit-tap-highlight-color: transparent;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
                background: #000000;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
                color: white;
            }
            
            .phone-container {
                background: linear-gradient(145deg, #1c1c1e 0%, #2c2c2e 100%);
                border-radius: 55px;
                padding: 0;
                box-shadow: 
                    0 50px 100px rgba(0,0,0,0.5),
                    inset 0 1px 0 rgba(255,255,255,0.1);
                max-width: 420px;
                width: 100%;
                overflow: hidden;
                border: 1px solid rgba(255,255,255,0.1);
            }
            
            .dynamic-island {
                background: #000000;
                height: 37px;
                border-radius: 0 0 20px 20px;
                margin: 0 auto 10px;
                width: 150px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }
            
            .island-dot {
                width: 6px;
                height: 6px;
                background: #00ff88;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }
            
            .content {
                padding: 20px 30px 40px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 25px;
            }
            
            .header h1 {
                color: #ffffff;
                font-size: 17px;
                font-weight: 600;
                margin-bottom: 3px;
                letter-spacing: -0.4px;
            }
            
            .header p {
                color: rgba(255,255,255,0.5);
                font-size: 13px;
                font-weight: 400;
                letter-spacing: -0.1px;
            }
            
            .display {
                background: rgba(120,120,128,0.16);
                backdrop-filter: blur(20px) saturate(180%);
                -webkit-backdrop-filter: blur(20px) saturate(180%);
                border-radius: 20px;
                padding: 30px 20px;
                margin-bottom: 20px;
                min-height: 90px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                border: 0.5px solid rgba(255,255,255,0.1);
            }
            
            .display-number {
                font-size: 38px;
                color: #ffffff;
                font-weight: 300;
                letter-spacing: 2px;
                text-align: center;
                word-break: break-all;
                font-variant-numeric: tabular-nums;
            }
            
            .status {
                text-align: center;
                margin: 12px 0;
                font-size: 13px;
                color: rgba(255,255,255,0.6);
                min-height: 18px;
                font-weight: 500;
                letter-spacing: -0.1px;
            }
            
            .status.active {
                color: #00ff88;
                animation: statusPulse 1.5s infinite;
            }
            
            @keyframes statusPulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            
            .keypad {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 25px;
                padding: 10px 0;
            }
            
            .key {
                background: rgba(120,120,128,0.24);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 0.5px solid rgba(255,255,255,0.15);
                border-radius: 50%;
                width: 100%;
                aspect-ratio: 1;
                font-size: 32px;
                font-weight: 300;
                color: #ffffff;
                cursor: pointer;
                transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 
                    0 4px 12px rgba(0,0,0,0.3),
                    inset 0 1px 0 rgba(255,255,255,0.1);
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
            }
            
            .key::before {
                content: '';
                position: absolute;
                inset: 0;
                border-radius: 50%;
                background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.15), transparent);
                opacity: 0;
                transition: opacity 0.15s;
            }
            
            .key:hover::before {
                opacity: 1;
            }
            
            .key:hover {
                background: rgba(120,120,128,0.36);
                transform: scale(1.05);
                box-shadow: 
                    0 6px 16px rgba(0,0,0,0.4),
                    inset 0 1px 0 rgba(255,255,255,0.15);
            }
            
            .key:active {
                transform: scale(0.95);
                background: rgba(120,120,128,0.44);
                box-shadow: 
                    0 2px 6px rgba(0,0,0,0.3),
                    inset 0 1px 3px rgba(0,0,0,0.2);
            }
            
            .controls {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 15px;
            }
            
            .control-btn {
                padding: 16px;
                border: none;
                border-radius: 16px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                letter-spacing: -0.3px;
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
            }
            
            .control-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(0,0,0,0.4);
            }
            
            .control-btn:active {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }
            
            .call-btn {
                background: linear-gradient(145deg, #00ff88 0%, #00dd77 100%);
                color: #000000;
                grid-column: span 2;
                font-size: 18px;
                padding: 20px;
                border-radius: 20px;
                font-weight: 700;
                box-shadow: 
                    0 6px 20px rgba(0,255,136,0.4),
                    inset 0 1px 0 rgba(255,255,255,0.3);
            }
            
            .call-btn:hover {
                background: linear-gradient(145deg, #00ff99 0%, #00ee88 100%);
                box-shadow: 
                    0 10px 30px rgba(0,255,136,0.5),
                    inset 0 1px 0 rgba(255,255,255,0.4);
            }
            
            .hangup-btn {
                background: linear-gradient(145deg, #ff3b30 0%, #dd2a1f 100%);
                color: white;
                grid-column: span 2;
                border-radius: 20px;
                box-shadow: 
                    0 6px 20px rgba(255,59,48,0.4),
                    inset 0 1px 0 rgba(255,255,255,0.2);
            }
            
            .hangup-btn:hover {
                background: linear-gradient(145deg, #ff4c41 0%, #ee3b30 100%);
                box-shadow: 
                    0 10px 30px rgba(255,59,48,0.5),
                    inset 0 1px 0 rgba(255,255,255,0.3);
            }
            
            .mute-btn {
                background: linear-gradient(145deg, #ff9500 0%, #dd7f00 100%);
                color: white;
                box-shadow: 
                    0 4px 15px rgba(255,149,0,0.4),
                    inset 0 1px 0 rgba(255,255,255,0.2);
            }
            
            .mute-btn:hover {
                background: linear-gradient(145deg, #ffa61a 0%, #ee9010 100%);
            }
            
            .mute-btn.muted {
                background: linear-gradient(145deg, #007aff 0%, #0066dd 100%);
                box-shadow: 
                    0 4px 15px rgba(0,122,255,0.4),
                    inset 0 1px 0 rgba(255,255,255,0.2);
            }
            
            .delete-btn {
                background: rgba(120,120,128,0.24);
                color: white;
                backdrop-filter: blur(20px);
                border: 0.5px solid rgba(255,255,255,0.1);
            }
            
            .delete-btn:hover {
                background: rgba(120,120,128,0.36);
            }
            
            .clear-btn {
                background: rgba(120,120,128,0.24);
                color: white;
                backdrop-filter: blur(20px);
                border: 0.5px solid rgba(255,255,255,0.1);
            }
            
            .clear-btn:hover {
                background: rgba(120,120,128,0.36);
            }
            
            .disabled {
                opacity: 0.4;
                cursor: not-allowed !important;
            }
            
            .disabled:hover {
                transform: none !important;
            }
            
            .back-link {
                text-align: center;
                margin-top: 25px;
                padding-top: 20px;
                border-top: 0.5px solid rgba(255,255,255,0.1);
            }
            
            .back-link a {
                color: #007aff;
                text-decoration: none;
                font-size: 15px;
                font-weight: 500;
                letter-spacing: -0.2px;
                transition: color 0.2s;
            }
            
            .back-link a:hover {
                color: #0066dd;
            }
            
            @media (max-width: 480px) {
                .phone-container {
                    border-radius: 45px;
                }
                
                .content {
                    padding: 15px 25px 35px;
                }
                
                .display-number {
                    font-size: 32px;
                }
                
                .key {
                    font-size: 28px;
                }
                
                .keypad {
                    gap: 15px;
                }
            }
            
            /* Glassmorphism effect */
            @supports (backdrop-filter: blur(20px)) or (-webkit-backdrop-filter: blur(20px)) {
                .phone-container {
                    background: linear-gradient(145deg, rgba(28,28,30,0.85) 0%, rgba(44,44,46,0.85) 100%);
                    backdrop-filter: blur(40px) saturate(180%);
                    -webkit-backdrop-filter: blur(40px) saturate(180%);
                }
            }
        </style>
    </head>
    <body>
        <div class="phone-container">
            <div class="dynamic-island">
                <div class="island-dot"></div>
                <div class="island-dot" style="animation-delay: 0.3s;"></div>
            </div>
            
            <div class="content">
                <div class="header">
                    <h1>Phone</h1>
                    <p>مرزوق لوحة الاتصال</p>
                </div>
                
                <div class="display">
                    <div class="display-number" id="displayNumber">—</div>
                </div>
                
                <div class="status" id="status">Ready</div>
                
                <div class="keypad">
                    <button class="key" onclick="addDigit('1')">1</button>
                    <button class="key" onclick="addDigit('2')">2</button>
                    <button class="key" onclick="addDigit('3')">3</button>
                    <button class="key" onclick="addDigit('4')">4</button>
                    <button class="key" onclick="addDigit('5')">5</button>
                    <button class="key" onclick="addDigit('6')">6</button>
                    <button class="key" onclick="addDigit('7')">7</button>
                    <button class="key" onclick="addDigit('8')">8</button>
                    <button class="key" onclick="addDigit('9')">9</button>
                    <button class="key" onclick="addDigit('*')">*</button>
                    <button class="key" onclick="addDigit('0')">0</button>
                    <button class="key" onclick="addDigit('#')">#</button>
                </div>
                
                <div class="controls">
                    <button class="control-btn delete-btn" onclick="deleteDigit()">
                        <span>⌫</span> Delete
                    </button>
                    <button class="control-btn clear-btn" onclick="clearNumber()">
                        <span>⌧</span> Clear
                    </button>
                </div>
                
                <div class="controls">
                    <button class="control-btn call-btn" id="callBtn" onclick="makeCall()">
                        <span>📞</span> Call
                    </button>
                </div>
                
                <div class="controls" id="activeControls" style="display: none;">
                    <button class="control-btn mute-btn" id="muteBtn" onclick="toggleMute()">
                        <span id="muteIcon">🎤</span> <span id="muteText">Mute</span>
                    </button>
                    <button class="control-btn hangup-btn" onclick="hangUp()">
                        <span>📵</span> End
                    </button>
                </div>
                
                <div class="back-link">
                    <a href="/">← Back to Home</a>
                </div>
            </div>
        </div>
        
        <script>
            let currentNumber = '';
            let isCallActive = false;
            let isMuted = false;
            
            function addDigit(digit) {
                if (currentNumber.length < 20) {
                    currentNumber += digit;
                    updateDisplay();
                    // Haptic feedback simulation
                    if (navigator.vibrate) {
                        navigator.vibrate(10);
                    }
                }
            }
            
            function deleteDigit() {
                currentNumber = currentNumber.slice(0, -1);
                updateDisplay();
            }
            
            function clearNumber() {
                currentNumber = '';
                updateDisplay();
            }
            
            function updateDisplay() {
                const display = document.getElementById('displayNumber');
                if (currentNumber === '') {
                    display.textContent = '—';
                    display.style.color = 'rgba(255,255,255,0.3)';
                } else {
                    display.textContent = currentNumber;
                    display.style.color = '#ffffff';
                }
            }
            
            function updateStatus(message, isActive = false) {
                const status = document.getElementById('status');
                status.textContent = message;
                if (isActive) {
                    status.classList.add('active');
                } else {
                    status.classList.remove('active');
                }
            }
            
            function makeCall() {
                if (currentNumber === '') {
                    updateStatus('Enter a number first', false);
                    setTimeout(() => updateStatus('Ready', false), 2000);
                    return;
                }
                
                isCallActive = true;
                document.getElementById('callBtn').style.display = 'none';
                document.getElementById('activeControls').style.display = 'grid';
                
                updateStatus('Calling ' + currentNumber + '...', true);
                
                // Simulate ringing and connection
                setTimeout(() => {
                    if (isCallActive) {
                        updateStatus('Connected • ' + formatTime(0), true);
                        startCallTimer();
                    }
                }, 2500);
                
                // Haptic feedback
                if (navigator.vibrate) {
                    navigator.vibrate([100, 50, 100]);
                }
            }
            
            let callDuration = 0;
            let callTimer;
            
            function startCallTimer() {
                callDuration = 0;
                callTimer = setInterval(() => {
                    callDuration++;
                    if (isCallActive) {
                        updateStatus('Connected • ' + formatTime(callDuration), true);
                    }
                }, 1000);
            }
            
            function formatTime(seconds) {
                const mins = Math.floor(seconds / 60);
                const secs = seconds % 60;
                return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            }
            
            function hangUp() {
                isCallActive = false;
                isMuted = false;
                
                if (callTimer) {
                    clearInterval(callTimer);
                }
                
                document.getElementById('callBtn').style.display = 'block';
                document.getElementById('activeControls').style.display = 'none';
                
                updateStatus('Call ended', false);
                
                // Reset mute button
                const muteBtn = document.getElementById('muteBtn');
                muteBtn.classList.remove('muted');
                document.getElementById('muteIcon').textContent = '🎤';
                document.getElementById('muteText').textContent = 'Mute';
                
                setTimeout(() => {
                    updateStatus('Ready', false);
                }, 3000);
                
                // Haptic feedback
                if (navigator.vibrate) {
                    navigator.vibrate(50);
                }
            }
            
            function toggleMute() {
                if (!isCallActive) return;
                
                isMuted = !isMuted;
                const muteBtn = document.getElementById('muteBtn');
                const muteIcon = document.getElementById('muteIcon');
                const muteText = document.getElementById('muteText');
                
                if (isMuted) {
                    muteBtn.classList.add('muted');
                    muteIcon.textContent = '🔇';
                    muteText.textContent = 'Unmute';
                } else {
                    muteBtn.classList.remove('muted');
                    muteIcon.textContent = '🎤';
                    muteText.textContent = 'Mute';
                }
                
                // Haptic feedback
                if (navigator.vibrate) {
                    navigator.vibrate(10);
                }
            }
            
            // Keyboard support
            document.addEventListener('keydown', function(event) {
                if (event.key >= '0' && event.key <= '9') {
                    addDigit(event.key);
                } else if (event.key === '*') {
                    addDigit('*');
                } else if (event.key === '#') {
                    addDigit('#');
                } else if (event.key === 'Backspace') {
                    event.preventDefault();
                    deleteDigit();
                } else if (event.key === 'Enter' && !isCallActive) {
                    makeCall();
                } else if (event.key === 'Escape' && isCallActive) {
                    hangUp();
                } else if (event.key.toLowerCase() === 'm' && isCallActive) {
                    toggleMute();
                }
            });
        </script>
    </body>
    </html>
    """
    
    return html


if __name__ == "__main__":
    # حفظ HTML في ملف للاختبار
    with open('/tmp/phone_dialer_test.html', 'w', encoding='utf-8') as f:
        f.write(generate_dialer_html())
    
    print("✅ Phone dialer HTML generated successfully!")
    print("📁 Saved to: /tmp/phone_dialer_test.html")
    print("\nPhone Dialer Features:")
    print("- Numeric keypad: 0-9")
    print("- Special keys: * and #")
    print("- Call button (green)")
    print("- Hang up button (red)")
    print("- Mute/Unmute button (orange/blue)")
    print("- Delete and Clear buttons")
    print("- Bilingual interface (Arabic/English)")
