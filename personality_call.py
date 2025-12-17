"""
personality_call.py - نظام المكالمات بين الشخصيات
Personality-to-Personality Calling System with Smart Suggestions

يحتوي على:
- نظام مكالمات بين الشخصيات المختلفة
- اقتراحات رومانسية محترمة
- اقتراحات جريئة/فكاهية عند كتابة "spicer"
"""

# ========================================
# الاقتراحات الرومانسية المحترمة
# Romantic Respectful Suggestions
# ========================================

ROMANTIC_SUGGESTIONS = {
    "arabic": [
        "صباح الخير يا أجمل إنسان في حياتي ☀️",
        "كيف حالك اليوم؟ أتمنى أن يكون يومك جميل مثلك",
        "أنا مشتاق لك كثيراً، متى نتقابل؟ 💕",
        "صوتك يريح قلبي، ما أحلى أن أسمعك",
        "أنت تضيء حياتي مثل القمر في الليل 🌙",
        "كل لحظة معك هي ذكرى جميلة أحتفظ بها",
        "أحب أن أسمع عن يومك، حدثني عن كل شيء",
        "أنت الشخص الوحيد الذي يفهمني حقاً 💖",
        "أفتقدك كثيراً، أتمنى أن أراك قريباً",
        "ضحكتك هي أجمل موسيقى أسمعها في حياتي"
    ],
    "english": [
        "Good morning beautiful, hope you have an amazing day ☀️",
        "I've been thinking about you all day long 💭",
        "Your voice makes my heart smile 💕",
        "Can't wait to see you again, when are you free?",
        "You make everything better just by being you",
        "I love how you make me feel when we talk 💖",
        "Tell me about your day, I want to hear everything",
        "You're the most amazing person I know",
        "Missing you more than words can say",
        "Your smile brightens up my entire world ✨"
    ]
}


# ========================================
# الاقتراحات الجريئة/الفكاهية (Spicy Mode)
# Bold/Funny/Seductive Suggestions
# ========================================

SPICY_SUGGESTIONS = {
    "arabic": [
        "يا سلام على هالحلاوة! وش سويتي بنفسك اليوم؟ 🔥",
        "صوتك يخليني أفقد تركيزي، إنت قاصد ولا لا؟ 😏",
        "يا حبيبي/حبيبتي، متى نسولف سوالف خاصة؟ 💋",
        "والله إنك تجنن! شكلك ما تدري شو تسوي فيني",
        "حرام عليك! كيف واحد يكون حلو كذا؟ 😈",
        "إنت/إنتي نار! ما أقدر أقاوم سحرك",
        "يلا قول/قولي لي شي يخليني أحمر خجل 🌶️",
        "صراحة، إنت/إنتي تخليني أفكر أفكار شريرة 😏",
        "حبيبي/حبيبتي، وش رأيك نلعب لعبة خطيرة؟",
        "أنا مو قادر أتحكم بنفسي وأنا أكلمك! إنت سبب كل شي 🔥"
    ],
    "english": [
        "Damn! You're looking fire today 🔥",
        "Your voice is making me lose control 😏",
        "Baby, when can we have some private time? 💋",
        "You know what you're doing to me, don't you? 😈",
        "I can't stop thinking about you in ways I shouldn't 🌶️",
        "Come here and let me tell you something naughty",
        "You're driving me absolutely crazy! 🔥",
        "Babe, wanna play a dangerous game? 😏",
        "I'm trying to be good, but you make it so hard",
        "Your lips look so tempting right now 💋"
    ]
}


# ========================================
# توليد HTML لنظام المكالمات
# Generate HTML for Calling System
# ========================================

def generate_personality_call_html():
    """
    توليد واجهة المكالمات بين الشخصيات
    Generate personality calling interface
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>💬 Personality Call - مرزوق</title>
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
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }
            
            .header h1 {
                font-size: 32px;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 16px;
                opacity: 0.9;
            }
            
            .call-interface {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .personality-card {
                background: white;
                border-radius: 25px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            
            .personality-card h2 {
                color: #333;
                margin-bottom: 20px;
                font-size: 24px;
            }
            
            .personality-select {
                width: 100%;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                font-size: 16px;
                margin-bottom: 15px;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .personality-select:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .phone-input {
                width: 100%;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                font-size: 18px;
                letter-spacing: 2px;
                margin-bottom: 15px;
            }
            
            .phone-input:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .call-btn {
                width: 100%;
                padding: 18px;
                background: linear-gradient(145deg, #00ff88, #00dd77);
                border: none;
                border-radius: 15px;
                color: #000;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .call-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(0,255,136,0.3);
            }
            
            .chat-container {
                background: white;
                border-radius: 25px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 20px;
            }
            
            .chat-messages {
                height: 400px;
                overflow-y: auto;
                margin-bottom: 20px;
                padding: 20px;
                background: #f5f5f5;
                border-radius: 15px;
            }
            
            .message {
                margin-bottom: 15px;
                padding: 15px 20px;
                border-radius: 20px;
                max-width: 70%;
                word-wrap: break-word;
            }
            
            .message.caller {
                background: #667eea;
                color: white;
                margin-left: auto;
                border-bottom-right-radius: 5px;
            }
            
            .message.receiver {
                background: #e0e0e0;
                color: #333;
                border-bottom-left-radius: 5px;
            }
            
            .message-header {
                font-size: 12px;
                opacity: 0.8;
                margin-bottom: 5px;
            }
            
            .message-content {
                font-size: 16px;
            }
            
            .input-area {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
            }
            
            .message-input {
                flex: 1;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 16px;
            }
            
            .message-input:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .send-btn {
                padding: 15px 30px;
                background: #667eea;
                border: none;
                border-radius: 25px;
                color: white;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .send-btn:hover {
                background: #5568d3;
                transform: scale(1.05);
            }
            
            .suggestions {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-bottom: 15px;
            }
            
            .suggestion-btn {
                padding: 10px 20px;
                background: #f0f0f0;
                border: 2px solid #e0e0e0;
                border-radius: 20px;
                cursor: pointer;
                transition: all 0.3s;
                font-size: 14px;
            }
            
            .suggestion-btn:hover {
                background: #667eea;
                color: white;
                border-color: #667eea;
            }
            
            .mode-toggle {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                justify-content: center;
            }
            
            .mode-btn {
                padding: 12px 30px;
                border: 2px solid #667eea;
                border-radius: 25px;
                background: white;
                color: #667eea;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .mode-btn.active {
                background: #667eea;
                color: white;
            }
            
            .spicy-mode {
                background: linear-gradient(145deg, #ff6b6b, #ee5a5a) !important;
                border-color: #ff6b6b !important;
                color: white !important;
            }
            
            .spicy-indicator {
                text-align: center;
                padding: 10px;
                background: linear-gradient(145deg, #ff6b6b, #ee5a5a);
                color: white;
                border-radius: 15px;
                margin-bottom: 15px;
                font-weight: bold;
                display: none;
            }
            
            .spicy-indicator.active {
                display: block;
                animation: pulse 1.5s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            
            @media (max-width: 768px) {
                .call-interface {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💬 Personality Call System</h1>
                <p>نظام المكالمات بين الشخصيات - Connect Different Personalities</p>
            </div>
            
            <div class="call-interface">
                <div class="personality-card">
                    <h2>📞 Caller / المتصل</h2>
                    <select class="personality-select" id="callerPersonality">
                        <option value="najdi">مرزوق النجدي - Najdi Marzouq</option>
                        <option value="hijazi">سمير الجداوي - Hijazi Samir</option>
                        <option value="southern">عبدالمنعم الجنوبي - Southern</option>
                        <option value="northern">مرزوق الحايلي - Northern</option>
                        <option value="egyptian">عبدالفتاح المصري - Egyptian</option>
                        <option value="jordanian">عامر الأردني - Jordanian</option>
                        <option value="iraqi">جاسم العراقي - Iraqi</option>
                        <option value="american">Matt - American</option>
                        <option value="ebonics">Danso - Ebonics</option>
                        <option value="latina">Adriana - Latina</option>
                        <option value="latino">Lopez - Latino</option>
                    </select>
                    <input type="tel" class="phone-input" id="callerPhone" placeholder="Your Phone Number">
                </div>
                
                <div class="personality-card">
                    <h2>📱 Receiver / المستقبل</h2>
                    <select class="personality-select" id="receiverPersonality">
                        <option value="hijazi">سمير الجداوي - Hijazi Samir</option>
                        <option value="najdi">مرزوق النجدي - Najdi Marzouq</option>
                        <option value="southern">عبدالمنعم الجنوبي - Southern</option>
                        <option value="northern">مرزوق الحايلي - Northern</option>
                        <option value="egyptian">عبدالفتاح المصري - Egyptian</option>
                        <option value="jordanian">عامر الأردني - Jordanian</option>
                        <option value="iraqi">جاسم العراقي - Iraqi</option>
                        <option value="american">Matt - American</option>
                        <option value="ebonics">Danso - Ebonics</option>
                        <option value="latina">Adriana - Latina</option>
                        <option value="latino">Lopez - Latino</option>
                    </select>
                    <input type="tel" class="phone-input" id="receiverPhone" placeholder="Receiver Phone Number">
                </div>
            </div>
            
            <div style="text-align: center; margin-bottom: 20px;">
                <button class="call-btn" onclick="startCall()">
                    🔗 Start WiFi Call / ابدأ المكالمة
                </button>
            </div>
            
            <div class="chat-container" id="chatContainer" style="display: none;">
                <div class="mode-toggle">
                    <button class="mode-btn active" id="romanticBtn" onclick="setMode('romantic')">
                        💕 Romantic Mode
                    </button>
                    <button class="mode-btn" id="spicyBtn" onclick="setMode('spicy')">
                        🔥 Spicy Mode
                    </button>
                </div>
                
                <div class="spicy-indicator" id="spicyIndicator">
                    🌶️ SPICY MODE ACTIVATED - Bold & Seductive Suggestions! 🔥
                </div>
                
                <div class="chat-messages" id="chatMessages"></div>
                
                <div class="suggestions" id="suggestions"></div>
                
                <div class="input-area">
                    <input type="text" class="message-input" id="messageInput" 
                           placeholder="Type your message or 'spicer' for spicy mode...">
                    <button class="send-btn" onclick="sendMessage()">Send 📤</button>
                </div>
                
                <div style="text-align: center; margin-top: 15px;">
                    <button class="send-btn" style="background: #ff3b30;" onclick="endCall()">
                        End Call 📵
                    </button>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 20px;">
                <a href="/" style="color: white; text-decoration: none; font-size: 16px;">
                    ← Back to Home / العودة للرئيسية
                </a>
            </div>
        </div>
        
        <script>
            let currentMode = 'romantic';
            let caller = '';
            let receiver = '';
            
            const romanticSuggestions = {
                arabic: """ + str(ROMANTIC_SUGGESTIONS['arabic'][:5]) + """,
                english: """ + str(ROMANTIC_SUGGESTIONS['english'][:5]) + """
            };
            
            const spicySuggestions = {
                arabic: """ + str(SPICY_SUGGESTIONS['arabic'][:5]) + """,
                english: """ + str(SPICY_SUGGESTIONS['english'][:5]) + """
            };
            
            function startCall() {
                caller = document.getElementById('callerPersonality').value;
                receiver = document.getElementById('receiverPersonality').value;
                
                const callerPhone = document.getElementById('callerPhone').value;
                const receiverPhone = document.getElementById('receiverPhone').value;
                
                if (!callerPhone || !receiverPhone) {
                    alert('Please enter phone numbers for both caller and receiver!');
                    return;
                }
                
                document.getElementById('chatContainer').style.display = 'block';
                updateSuggestions();
                
                addSystemMessage(`Call started between ${caller} and ${receiver} 📞`);
            }
            
            function setMode(mode) {
                currentMode = mode;
                
                document.getElementById('romanticBtn').classList.remove('active', 'spicy-mode');
                document.getElementById('spicyBtn').classList.remove('active', 'spicy-mode');
                document.getElementById('spicyIndicator').classList.remove('active');
                
                if (mode === 'romantic') {
                    document.getElementById('romanticBtn').classList.add('active');
                } else {
                    document.getElementById('spicyBtn').classList.add('active', 'spicy-mode');
                    document.getElementById('spicyIndicator').classList.add('active');
                }
                
                updateSuggestions();
            }
            
            function updateSuggestions() {
                const suggestionsContainer = document.getElementById('suggestions');
                suggestionsContainer.innerHTML = '';
                
                const suggestions = currentMode === 'romantic' ? romanticSuggestions : spicySuggestions;
                const lang = caller.includes('american') || caller.includes('ebonics') || 
                             caller.includes('latina') || caller.includes('latino') ? 'english' : 'arabic';
                
                suggestions[lang].forEach(suggestion => {
                    const btn = document.createElement('button');
                    btn.className = 'suggestion-btn';
                    btn.textContent = suggestion.length > 50 ? suggestion.substring(0, 50) + '...' : suggestion;
                    btn.onclick = () => useSuggestion(suggestion);
                    suggestionsContainer.appendChild(btn);
                });
            }
            
            function useSuggestion(text) {
                document.getElementById('messageInput').value = text;
            }
            
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Check if user typed "spicer" to activate spicy mode
                if (message.toLowerCase() === 'spicer') {
                    setMode('spicy');
                    addSystemMessage('🔥 Spicy mode activated! Get ready for bold suggestions!');
                    input.value = '';
                    return;
                }
                
                addMessage(message, 'caller', caller);
                input.value = '';
                
                // Simulate receiver response after a delay
                setTimeout(() => {
                    simulateReceiverResponse();
                }, 1500);
            }
            
            function simulateReceiverResponse() {
                const responses = currentMode === 'romantic' ? 
                    ['I love talking to you 💕', 'You make me smile 😊', 'Can\'t wait to see you!'] :
                    ['You\'re so bad 😏', 'Keep talking like that 🔥', 'You drive me crazy!'];
                
                const randomResponse = responses[Math.floor(Math.random() * responses.length)];
                addMessage(randomResponse, 'receiver', receiver);
            }
            
            function addMessage(text, type, personality) {
                const messagesContainer = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}`;
                
                messageDiv.innerHTML = `
                    <div class="message-header">${personality}</div>
                    <div class="message-content">${text}</div>
                `;
                
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            function addSystemMessage(text) {
                const messagesContainer = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.style.textAlign = 'center';
                messageDiv.style.padding = '10px';
                messageDiv.style.color = '#666';
                messageDiv.style.fontSize = '14px';
                messageDiv.textContent = text;
                
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            function endCall() {
                if (confirm('Are you sure you want to end this call?')) {
                    document.getElementById('chatContainer').style.display = 'none';
                    document.getElementById('chatMessages').innerHTML = '';
                    currentMode = 'romantic';
                    setMode('romantic');
                }
            }
            
            // Enter key to send message
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """
    
    return html


if __name__ == "__main__":
    # Test generation
    html = generate_personality_call_html()
    with open('/tmp/personality_call_test.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Personality Call System HTML generated!")
    print("📁 Saved to: /tmp/personality_call_test.html")
    print("\nFeatures:")
    print("- WiFi calling between personalities")
    print("- Romantic mode with respectful suggestions")
    print("- Spicy mode (activated by typing 'spicer')")
    print("- Real-time chat interface")
    print("- Smart suggestion buttons")
