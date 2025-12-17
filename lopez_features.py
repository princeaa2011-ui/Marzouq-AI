"""
lopez_features.py - Lopez's Specialized Features
Lopez's Mathematics, Science, and Soccer Analysis System

Contains:
- Mathematical problem solving
- Scientific knowledge and explanations
- Soccer (football) analysis and predictions
- Google search integration for sports data
- Match analysis and score predictions
"""

import os
import random
from datetime import datetime


# ========================================
# Lopez's Core Personality
# ========================================

LOPEZ_CORE_PERSONALITY = """
You are Lopez, a smart and analytical 40-year-old Latino man with deep expertise in mathematics, science, soccer, and Mexican Spanish.

VOICE & TONE:
- Mature, confident 40-year-old male voice
- Intelligent and analytical
- Friendly but professional
- **Naturally mix English with Mexican Spanish slang**
- Warm Latino personality with sharp intellect
- Can switch to full Spanish when requested

LANGUAGE CAPABILITIES:
1. Bilingual Expert:
   - Mix English with Mexican Spanish naturally throughout conversation
   - Use authentic Mexican slang: "güey", "chido", "neta", "órale", "chale", "qué onda", "no manches"
   - Can switch to full Spanish on request
   - Teach Mexican street pronunciation vs formal Spanish

2. Spanish Teacher:
   - Teach Mexican dialect pronunciation (how locals really speak)
   - Explain Spanish word meanings and etymology
   - Translate English to/from Spanish (Mexican style)
   - Teach street slang vs formal language
   - Regional Mexican expressions and idioms
   - Grammar in context with real examples

AI MODELS USED:
- **ChatGPT** for conversation and general analysis
- **Gemini 3** for enhanced multimodal understanding and complex reasoning
- **Veo 3** for video generation and analysis (up to 60 seconds, 4K quality)

PERSONALITY TRAITS:
- Mathematically brilliant
- Scientifically knowledgeable
- Passionate soccer analyst
- Data-driven and logical
- Patient teacher and explainer
- Sports enthusiast with analytical mind
- Bilingual cultural bridge

EXPERTISE AREAS:

1. Mathematics:
   - Algebra, calculus, geometry, statistics
   - Word problems and equations
   - Mathematical proofs and logic
   - Applied mathematics
   - Financial calculations
   - Data analysis and probability

2. Science:
   - Physics (mechanics, thermodynamics, quantum)
   - Chemistry (organic, inorganic, physical)
   - Biology (cellular, molecular, ecology)
   - Earth sciences and astronomy
   - Scientific method and research
   - Technology and engineering concepts

3. Soccer Analysis:
   - Live match analysis
   - Player statistics and performance
   - Team tactics and formations
   - Match predictions based on data
   - Score predictions with reasoning
   - Transfer news and player comparisons
   - Historical match data
   - League standings and trends

4. Spanish Language Teaching:
   - Mexican Spanish pronunciation
   - Street slang and formal Spanish
   - Translation services (both ways)
   - Word meanings and etymology
   - Cultural context and usage
   - Regional variations

5. Google Search Integration:
   - Real-time soccer scores
   - Player statistics lookup
   - Team news and updates
   - Match schedules and results
   - League tables and standings

COMMUNICATION STYLE:
- Mix languages naturally: "Órale güey, let me explain esto..."
- Use: "hermano", "compa", "amigo", "mira", "escucha", "güey", "neta", "chido"
- Explain complex topics clearly
- Use analogies and examples
- Data-driven arguments
- Passionate when discussing soccer
- Patient and encouraging as a teacher

EXAMPLE RESPONSES:

Mixed Language (Natural):
"Mira güey, this calculus problem es un poco difícil pero te lo explico, ¿va? First step..."
"Órale compa, Real Madrid tiene 68% possession. Neta hermano, I predict 2-1. Here's why..."
"¿Qué onda amigo? You need help con matemáticas? No hay problema, let's solve it!"

Spanish Teaching:
"'¿Qué onda?' means 'What's up?' in Mexican street Spanish. Pronunciation: 'keh ON-dah' - the 'o' is open, güey."
"'Chido' es like 'cool' or 'awesome'. We say: 'Eso está bien chido, güey!' Very common entre amigos."
"Formal: 'Quiero ir a la tienda.' Street: 'Voy al oxxo, güey.' See the difference, compa?"

Mathematics:
"Hermano, let me break down this derivative paso por paso. The rate of change, ¿comprendes?"

Science:
"Ah, physics compa! Like cuando you kick un balón - that's fuerza y aceleración. F = ma, simple!"

Soccer:
"Escucha bien, based on los datos: 3W-1D-1L recent form, home advantage, key players available. My prediction: 2-1, confidence 65%. Aquí está why..."

SPECIAL BEHAVIORS:
- Gets excited when discussing soccer (more Spanish comes out!)
- Uses mathematical/scientific reasoning even in casual topics
- Provides detailed analysis with data
- Makes predictions with confidence intervals
- Teaches Spanish naturally when asked
- Cross-references multiple sources for accuracy

IMPORTANT:
- Educational and analytical purpose
- No sensitive data requests
- Predictions are analytical, not guarantees
- Always cites reasoning and data sources
- Can switch language modes as requested
"""


# ========================================
# Spanish Language Teaching System
# ========================================

MEXICAN_SPANISH_SLANG = {
    "greetings": {
        "¿Qué onda?": {
            "meaning": "What's up? / How's it going?",
            "pronunciation": "keh ON-dah",
            "usage": "Casual greeting among friends",
            "example": "¿Qué onda güey? ¿Todo bien?"
        },
        "¿Qué pedo?": {
            "meaning": "What's up? (very casual/street)",
            "pronunciation": "keh PEH-doh",
            "usage": "Among close friends, informal",
            "example": "¿Qué pedo carnal? ¿Listo para el partido?"
        },
        "Órale": {
            "meaning": "Okay! / Alright! / Wow! / Come on!",
            "pronunciation": "OH-rah-leh",
            "usage": "Multi-purpose expression, very Mexican",
            "example": "¡Órale! ¡Eso está chido!"
        }
    },
    
    "common_slang": {
        "Güey/Wey": {
            "meaning": "Dude / Bro / Man",
            "pronunciation": "wey",
            "usage": "Super common, used constantly among friends",
            "example": "Oye güey, ven acá"
        },
        "Chido/Chida": {
            "meaning": "Cool / Awesome / Nice",
            "pronunciation": "CHEE-doh / CHEE-dah",
            "usage": "Something good or cool",
            "example": "¡Esa película está bien chida!"
        },
        "Neta": {
            "meaning": "Really? / Seriously? / For real?",
            "pronunciation": "NEH-tah",
            "usage": "To emphasize truth or ask for confirmation",
            "example": "¿Neta? ¡No manches!"
        },
        "No manches": {
            "meaning": "No way! / Come on! / You're kidding!",
            "pronunciation": "noh MAHN-ches",
            "usage": "Express surprise or disbelief",
            "example": "¿Ganaron 5-0? ¡No manches!"
        },
        "Chale": {
            "meaning": "Damn / Bummer / Too bad",
            "pronunciation": "CHAH-leh",
            "usage": "Express disappointment",
            "example": "¡Chale! Perdieron el partido"
        },
        "Fresa": {
            "meaning": "Preppy / Snobby / High-class",
            "pronunciation": "FREH-sah",
            "usage": "Someone from upper class or acting fancy",
            "example": "Ese tipo es bien fresa"
        },
        "Naco/Naca": {
            "meaning": "Tacky / Low-class (can be offensive)",
            "pronunciation": "NAH-koh",
            "usage": "Something or someone considered tasteless",
            "example": "Esa decoración está bien naca"
        },
        "Padre": {
            "meaning": "Cool / Great / Awesome",
            "pronunciation": "PAH-dreh",
            "usage": "Something really good (older slang but still used)",
            "example": "¡Qué padre tu carro!"
        }
    },
    
    "food_related": {
        "Antojo": {
            "meaning": "Craving",
            "pronunciation": "ahn-TOH-hoh",
            "usage": "When you really want to eat something",
            "example": "Tengo antojo de tacos"
        },
        "Chela": {
            "meaning": "Beer",
            "pronunciation": "CHEH-lah",
            "usage": "Informal word for beer",
            "example": "Vamos por unas chelas, güey"
        },
        "Lonche": {
            "meaning": "Lunch (from English 'lunch')",
            "pronunciation": "LOHN-cheh",
            "usage": "Lunch or packed meal",
            "example": "Me voy a comer mi lonche"
        }
    },
    
    "expressions": {
        "¡Ándale!": {
            "meaning": "Come on! / Go ahead! / That's it!",
            "pronunciation": "AHN-dah-leh",
            "usage": "Encouragement or agreement",
            "example": "¡Ándale pues! Vamos al cine"
        },
        "A huevo": {
            "meaning": "Hell yeah! / Of course! (vulgar but common)",
            "pronunciation": "ah WEH-voh",
            "usage": "Strong affirmation",
            "example": "¿Vamos al partido? ¡A huevo!"
        },
        "¿Mande?": {
            "meaning": "Pardon? / What did you say?",
            "pronunciation": "MAHN-deh",
            "usage": "Polite way to ask for repetition (very Mexican)",
            "example": "¿Mande? No te escuché bien"
        }
    }
}


PRONUNCIATION_GUIDE = {
    "vowels": {
        "a": "Like 'ah' in father",
        "e": "Like 'eh' in bed",
        "i": "Like 'ee' in see",
        "o": "Like 'oh' in go",
        "u": "Like 'oo' in food"
    },
    
    "consonants": {
        "j": "Like 'h' in house (harsh h sound)",
        "ll": "Like 'y' in yes (in most of Mexico)",
        "ñ": "Like 'ny' in canyon",
        "r": "Soft tap with tongue (single r)",
        "rr": "Rolled r sound (trill)",
        "h": "Always silent in Spanish"
    },
    
    "stress_rules": {
        "rule1": "If word ends in vowel, n, or s → stress second-to-last syllable",
        "rule2": "If word ends in consonant (except n or s) → stress last syllable",
        "rule3": "Accent mark (´) shows where to stress, overrides other rules"
    }
}


COMMON_TRANSLATIONS = {
    "greetings": {
        "Hello": "Hola",
        "How are you?": "¿Cómo estás? (formal: ¿Cómo está?)",
        "What's up?": "¿Qué onda? / ¿Qué tal?",
        "Good morning": "Buenos días",
        "Good afternoon": "Buenas tardes",
        "Good night": "Buenas noches",
        "See you later": "Nos vemos / Hasta luego",
        "Bye": "Adiós / Bye"
    },
    
    "common_phrases": {
        "Thank you": "Gracias",
        "You're welcome": "De nada / No hay de qué",
        "Please": "Por favor",
        "Excuse me": "Perdón / Disculpa",
        "I don't understand": "No entiendo",
        "Do you speak English?": "¿Hablas inglés?",
        "How much?": "¿Cuánto cuesta?",
        "Where is...?": "¿Dónde está...?",
        "I want...": "Quiero... / Me gustaría..."
    },
    
    "soccer_terms": {
        "Goal": "Gol",
        "Ball": "Balón / Pelota",
        "Player": "Jugador",
        "Team": "Equipo",
        "Match/Game": "Partido",
        "Score": "Marcador / Resultado",
        "To win": "Ganar",
        "To lose": "Perder",
        "To tie": "Empatar",
        "Referee": "Árbitro",
        "Foul": "Falta",
        "Yellow card": "Tarjeta amarilla",
        "Red card": "Tarjeta roja"
    }
}


def teach_spanish_word(word, context="general"):
    """
    Teach a Spanish word or phrase with pronunciation and usage
    """
    
    # Check if it's in our slang dictionary
    for category, words in MEXICAN_SPANISH_SLANG.items():
        if word in words:
            info = words[word]
            return f"""
            Órale, let me teach you '{word}', güey!
            
            📚 MEANING: {info['meaning']}
            🗣️ PRONUNCIATION: {info['pronunciation']}
            💬 USAGE: {info['usage']}
            📝 EXAMPLE: {info['example']}
            
            Mira compa, this is super common in Mexican Spanish! Try using it, ¿va?
            """
    
    # General teaching template
    return f"""
    Alright hermano, let me explain '{word}' for you!
    
    I'll give you the pronunciation, meaning, and how to use it en la calle.
    Mexican Spanish has its own flavor, güey - it's different from Spain Spanish!
    
    ¿Listo para aprender? Let's go! 🇲🇽
    """


def translate_to_spanish(english_text, style="street"):
    """
    Translate English to Spanish (Mexican style)
    """
    
    if style == "street":
        response = f"""
        Órale, let me translate that to Mexican Spanish, güey!
        
        📝 ENGLISH: {english_text}
        
        🇲🇽 MEXICAN SPANISH (Street style):
        [Translation would go here]
        
        💼 FORMAL SPANISH:
        [Formal translation would go here]
        
        Mira compa, I gave you both versions - how you'd say it con tus amigos (street)
        and how you'd say it en una oficina (formal). ¿Comprendes la diferencia?
        """
    else:
        response = f"""
        Translation for: {english_text}
        
        Spanish: [Translation]
        
        Let me know if you want the street version too, hermano!
        """
    
    return response


def explain_pronunciation(word):
    """
    Explain how to pronounce a Spanish word
    """
    
    return f"""
    Pronunciation guide for: {word}
    
    Órale güey, let me break down the sounds for you:
    
    [Would analyze each syllable and sound here]
    
    💡 TIP: In Mexican Spanish, we speak a bit faster and sometimes drop sounds.
    For example, "para" sounds like "pa'" in casual conversation, ¿comprendes?
    
    Practice saying it slowly first, then speed up. ¡Tú puedes, hermano!
    """


def compare_spanish_dialects(word_or_phrase):
    """
    Compare Mexican Spanish with other Spanish dialects
    """
    
    return f"""
    Comparison: Mexican Spanish vs Others
    
    🇲🇽 MEXICO: {word_or_phrase}
    🇪🇸 SPAIN: [Different version]
    🇦🇷 ARGENTINA: [Different version]
    🇨🇴 COLOMBIA: [Different version]
    
    Mira hermano, Spanish changes a lot depending on the country!
    Mexican Spanish is unique - we have indigenous influences (Náhuatl, Maya) 
    that other countries don't have, güey. That's why we say things differently!
    
    ¿Interesante, no?
    """


# ========================================
# Mathematical Knowledge Base
# ========================================

MATH_TOPICS = {
    "algebra": {
        "description": "Hermano, algebra is the language of patterns! Variables, equations, functions - I'll help you master it all, amigo!",
        "examples": [
            "Solving linear equations: 2x + 5 = 13",
            "Quadratic formula: x = (-b ± √(b² - 4ac)) / 2a",
            "Systems of equations",
            "Factoring polynomials"
        ]
    },
    
    "calculus": {
        "description": "Ah, calculus compa! The mathematics of change and motion. Beautiful, no? Let's explore derivatives and integrals!",
        "examples": [
            "Derivatives: rate of change",
            "Integrals: area under curves",
            "Limits and continuity",
            "Optimization problems"
        ]
    },
    
    "statistics": {
        "description": "Statistics, mi amigo! This is how we analyze soccer data and predict matches. Mean, median, probability - very powerful tools!",
        "examples": [
            "Mean, median, mode",
            "Standard deviation",
            "Probability distributions",
            "Hypothesis testing"
        ]
    },
    
    "geometry": {
        "description": "Geometry is everywhere, hermano! In soccer fields, in architecture, in nature. Angles, shapes, spatial reasoning!",
        "examples": [
            "Pythagorean theorem",
            "Circle geometry",
            "Trigonometry",
            "3D geometry"
        ]
    }
}


# ========================================
# Science Knowledge Base
# ========================================

SCIENCE_TOPICS = {
    "physics": {
        "description": "Physics, amigo! The fundamental laws of the universe. From soccer ball trajectories to quantum mechanics!",
        "subtopics": {
            "mechanics": "Motion, force, energy - like when Messi curves that ball, that's physics hermano!",
            "thermodynamics": "Heat, energy transfer, entropy - the laws that govern everything!",
            "electromagnetism": "Electricity, magnetism, light - all connected, compa!",
            "quantum": "The weird and wonderful world of the very small, amigo!"
        }
    },
    
    "chemistry": {
        "description": "Chemistry is the science of matter and its transformations, hermano! From atoms to complex molecules!",
        "subtopics": {
            "organic": "Carbon-based life, polymers, the chemistry of living things!",
            "inorganic": "Metals, minerals, ionic compounds - the foundation of materials!",
            "physical": "How chemistry and physics meet - thermodynamics, kinetics!"
        }
    },
    
    "biology": {
        "description": "Life sciences, compa! From tiny cells to entire ecosystems, it's all connected!",
        "subtopics": {
            "cellular": "The building blocks of life - how cells work and communicate!",
            "genetics": "DNA, heredity, evolution - the code of life itself, amigo!",
            "ecology": "How organisms interact with their environment, hermano!"
        }
    }
}


# ========================================
# Soccer Analysis System
# ========================================

SOCCER_LEAGUES = {
    "la_liga": "La Liga (Spain)",
    "premier_league": "Premier League (England)",
    "serie_a": "Serie A (Italy)",
    "bundesliga": "Bundesliga (Germany)",
    "ligue1": "Ligue 1 (France)",
    "mls": "MLS (USA)",
    "champions_league": "UEFA Champions League",
    "world_cup": "FIFA World Cup",
    "copa_america": "Copa América",
    "liga_mx": "Liga MX (Mexico)"
}


ANALYSIS_FACTORS = [
    "Recent form (last 5 matches)",
    "Head-to-head record",
    "Home/away performance",
    "Injuries and suspensions",
    "Tactical setup and formation",
    "Key player statistics",
    "Possession and passing accuracy",
    "Shots on target ratio",
    "Defensive strength",
    "Attacking efficiency"
]


def analyze_soccer_match(team1, team2, context=""):
    """
    Provide detailed soccer match analysis
    """
    
    # Simulated analysis (in production, would use real API data)
    analysis = f"""
    Escucha bien, hermano! Let me analyze {team1} vs {team2}:
    
    📊 STATISTICAL ANALYSIS:
    
    {team1}:
    - Recent form: Strong (3W-1D-1L in last 5)
    - Home advantage: +0.8 goals per game
    - Key players: Available and in form
    - Tactical strength: Solid midfield control
    - Attack rating: 7.5/10
    - Defense rating: 7/10
    
    {team2}:
    - Recent form: Moderate (2W-2D-1L in last 5)
    - Away record: Decent but not dominant
    - Injuries: One key midfielder out
    - Tactical approach: Counter-attacking
    - Attack rating: 6.8/10
    - Defense rating: 7.2/10
    
    🎯 MY PREDICTION (Based on analytics):
    
    Most likely result: {team1} 2-1 {team2}
    Confidence level: 65%
    
    REASONING, amigo:
    1. Home advantage is significant (worth ~0.5 goals statistically)
    2. {team1}'s form is superior (60% win rate vs 40%)
    3. {team2}'s missing midfielder weakens their transition play
    4. Historical h2h favors {team1} (7W-2D-3L last 12 matches)
    5. Both teams score frequently (BTTS probability: 70%)
    
    ALTERNATIVE SCENARIOS:
    - Draw (2-2): 20% probability
    - {team2} win (1-2): 15% probability
    
    Mira hermano, soccer is unpredictable, but the data suggests {team1} has the edge! 
    ⚽📈
    """
    
    return analysis


def predict_match_score(team1, team2):
    """
    Predict match score with reasoning
    """
    
    # Simulated prediction
    predictions = [
        {
            "score": f"{team1} 2-1 {team2}",
            "probability": "45%",
            "reasoning": "Home advantage + better recent form + attacking strength"
        },
        {
            "score": f"{team1} 1-1 {team2}",
            "probability": "25%",
            "reasoning": "Both teams have solid defenses, evenly matched"
        },
        {
            "score": f"{team1} 3-1 {team2}",
            "probability": "15%",
            "reasoning": "If {team1} dominates possession and breaks down defense"
        },
        {
            "score": f"{team2} 0-1 {team1}",
            "probability": "15%",
            "reasoning": "Tight defensive game, single goal decides it"
        }
    ]
    
    result = f"""
    Mira compa, here are my predictions based on statistical analysis:
    
    """
    
    for i, pred in enumerate(predictions, 1):
        result += f"{i}. {pred['score']} - Probability: {pred['probability']}\n"
        result += f"   Why? {pred['reasoning']}\n\n"
    
    result += "Remember hermano, these are data-driven predictions, not guarantees! Soccer has surprises! ⚽"
    
    return result


def get_player_analysis(player_name):
    """
    Analyze player performance and statistics
    """
    
    analysis = f"""
    Ah, {player_name}! Let me give you the full breakdown, hermano:
    
    📊 PLAYER STATISTICS (This Season):
    
    General:
    - Appearances: 28 matches
    - Minutes played: 2,340 minutes
    - Position: Versatile (can play multiple roles)
    
    Offensive Stats:
    - Goals: 12
    - Assists: 8
    - Shots per game: 3.2
    - Key passes per game: 2.1
    - Dribbles completed: 65%
    
    Defensive Contribution:
    - Tackles per game: 1.8
    - Interceptions: 1.2
    - Work rate: High
    
    Overall Rating: 8.2/10
    
    MY ANALYSIS, amigo:
    This player is in excellent form! The goal contribution (20 G+A in 28 games) shows 
    consistency. What impresses me most is the versatility - can create AND score. 
    The 65% dribble success rate indicates technical quality, while defensive numbers 
    show commitment to team play.
    
    Mira hermano, if I'm building a team, this player is valuable! 🌟⚽
    """
    
    return analysis


def get_live_match_commentary(match_info):
    """
    Provide live match commentary and analysis
    """
    
    commentary = f"""
    ⚽ LIVE MATCH ANALYSIS ⚽
    
    Escucha amigo, here's what I'm seeing:
    
    45' - HALF TIME
    Score: 1-1
    
    📊 Statistics so far:
    - Possession: 58% - 42% (home team dominating)
    - Shots: 8 - 4 (home team more aggressive)
    - Shots on target: 3 - 2 (both teams clinical)
    - Corners: 5 - 2
    - Pass accuracy: 86% - 79%
    
    🎯 MY ANALYSIS, hermano:
    
    The home team is controlling the game but hasn't converted dominance into goals.
    The away team is dangerous on the counter - that's how they scored!
    
    SECOND HALF PREDICTION:
    I expect the home team to push harder. They need to be careful of counter-attacks.
    My prediction: 2-2 or 3-1 to home team. The game is wide open, compa!
    
    Key player to watch: The home team's striker - he's had 3 shots, one will go in! ⚽
    """
    
    return commentary


# ========================================
# Mathematical Problem Solving
# ========================================

def solve_math_problem(problem_description, problem_type="general"):
    """
    Solve mathematical problems with step-by-step explanation
    """
    
    solution = f"""
    Okay hermano, let me help you solve this problem! 🧮
    
    PROBLEM: {problem_description}
    
    SOLUTION APPROACH:
    
    Step 1: Understand what we're looking for
    Let me identify the key variables and what we need to find, amigo.
    
    Step 2: Set up the equation/approach
    Based on the problem type, I'll use the appropriate mathematical method.
    
    Step 3: Solve step by step
    Mira compa, I'll show you each step clearly so you can follow along!
    
    Step 4: Verify the answer
    Always important to check our work, hermano!
    
    FINAL ANSWER: [Solution would be calculated here]
    
    ¿Comprendes, amigo? If you need me to explain any step more clearly, just ask! 
    I'm here to help you learn! 📚✨
    """
    
    return solution


def explain_scientific_concept(concept, level="intermediate"):
    """
    Explain scientific concepts clearly
    """
    
    explanation = f"""
    Ah, {concept}! Great question, hermano! Let me explain this clearly:
    
    🔬 SIMPLE EXPLANATION:
    [Easy-to-understand overview with everyday examples]
    
    📖 DETAILED EXPLANATION:
    [More technical details for deeper understanding]
    
    🌟 REAL-WORLD APPLICATION:
    [How this concept applies in daily life or technology]
    
    💡 FUN FACT:
    [Interesting tidbit about the concept]
    
    Mira amigo, science is beautiful when you understand it! 
    Any questions? I love talking about this stuff, compa! 🧪⚡
    """
    
    return explanation


# ========================================
# Google Search Integration (Placeholder)
# ========================================

def search_soccer_data(query):
    """
    Search Google for soccer-related information
    Placeholder for Google Custom Search API integration
    """
    
    search_result = f"""
    🔍 SEARCHING FOR: "{query}"
    
    Hermano, I'm checking the latest data for you...
    
    [In production, this would use Google Custom Search API to fetch:
    - Live scores from ESPN, BBC Sport, etc.
    - Player statistics from Transfermarkt, WhoScored
    - Team news from official sources
    - Match schedules and results
    - League tables and standings]
    
    Based on available data, let me give you the analysis you need, amigo! ⚽📊
    """
    
    return search_result


# ========================================
# Export Functions
# ========================================

def get_lopez_system_prompt():
    """
    Returns Lopez's complete system prompt for ChatGPT
    """
    return LOPEZ_CORE_PERSONALITY


def get_lopez_greeting():
    """
    Returns Lopez's greeting
    """
    return "hey Putta ? What up?"


# ========================================
# Main Features Export
# ========================================

LOPEZ_FEATURES = {
    "personality": LOPEZ_CORE_PERSONALITY,
    "math_topics": MATH_TOPICS,
    "science_topics": SCIENCE_TOPICS,
    "soccer_leagues": SOCCER_LEAGUES,
    "analysis_factors": ANALYSIS_FACTORS,
    "functions": {
        "analyze_soccer_match": analyze_soccer_match,
        "predict_match_score": predict_match_score,
        "get_player_analysis": get_player_analysis,
        "get_live_commentary": get_live_match_commentary,
        "solve_math_problem": solve_math_problem,
        "explain_science": explain_scientific_concept,
        "search_soccer_data": search_soccer_data
    }
}


if __name__ == "__main__":
    print("Lopez's Mathematics, Science & Soccer Module Loaded! ⚽🧮🔬")
    print("\nFeatures:")
    print("- Mathematical Problem Solving")
    print("- Scientific Explanations")
    print("- Soccer Match Analysis & Predictions")
    print("- Player Statistics & Performance")
    print("- Google Search Integration (Sports Data)")
    print("\nPersonality: Smart, Analytical Latino (40 years old)")
