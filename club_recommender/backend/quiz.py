
from typing import Any

QUESTIONS = {
    "categories": {
        "question": "What kinds of clubs are you interested in?",
        "type": "multi",
        "options": [
            ("music", "Music & Singing"), ("dance", "Dance & Movement"),
            ("theatre", "Theatre, Comedy & Storytelling"),
            ("visual_arts", "Visual Arts, Crafts & Design"),
            ("writing_media", "Writing, Media & Publications"),
            ("games", "Games, Puzzles & Fandom"), ("food", "Food & Drink"),
            ("tech", "Tech & Making"), ("outdoors", "Outdoors, Nature & Animals"),
            ("sustainability", "Sustainability & Environment"),
            ("cultural", "Cultural & Heritage"),
            ("language", "Language & Global Exchange"),
            ("identity", "Identity & Community"),
            ("faith", "Faith, Spirituality & Mindfulness"),
            ("service", "Service & Volunteering"),
            ("advocacy", "Advocacy, Politics & Debate"),
        ],
    },
    "music": {
        "question": "What sounds most interesting?",
        "type": "multi",
        "options": [
            ("a_cappella", "A Cappella"), ("choral", "Choral & Vocal"),
            ("instrumental", "Instrumental Ensembles"), ("jazz_rock", "Jazz, Rock & Contemporary"),
            ("world_music", "World & Cultural Music"), ("production", "Music Production & DJing"),
            ("live_music", "Live Music Events"),
        ],
    },
    "dance": {
        "question": "What kind of dance interests you?",
        "type": "multi",
        "options": [
            ("cultural_dance", "Cultural & Folk Dance"), ("partner_dance", "Social & Partner Dance"),
            ("street_dance", "Street & Hip-Hop Dance"), ("performance_dance", "Performance Troupes"),
            ("flow_circus", "Flow Arts & Circus"),
        ],
    },
    "theatre": {
        "question": "What interests you most?",
        "type": "multi",
        "options": [
            ("improv", "Improv & Sketch Comedy"), ("theatre_prod", "Theatre Production"),
            ("storytelling", "Storytelling & Spoken Word"), ("standup", "Stand-up & Variety"),
        ],
    },
    "visual_arts": {
        "question": "What would you like to do?",
        "type": "multi",
        "options": [
            ("drawing", "Drawing & Painting"), ("crafts", "Crafts & Fiber Arts"),
            ("photo_film", "Photography & Film"), ("digital_art", "Digital Art & Animation"),
            ("fashion", "Fashion & Style"),
        ],
    },
    "writing_media": {
        "question": "What sounds most interesting?",
        "type": "multi",
        "options": [
            ("publications", "Magazines & Publications"), ("creative_writing", "Creative Writing & Poetry"),
            ("broadcast", "Radio, Podcast & Broadcast"), ("books", "Book & Reading Clubs"),
        ],
    },
    "games": {
        "question": "What do you enjoy?",
        "type": "multi",
        "options": [
            ("board_games", "Board & Card Games"), ("rpg", "Tabletop RPG & Miniatures"),
            ("video_games", "Video Games & Esports"), ("trivia", "Trivia, Puzzles & Strategy"),
            ("fandom", "Fandom, Film & Pop Culture"), ("collecting", "Collecting & Hobbyist Communities"),
        ],
    },
    "food": {
        "question": "What interests you?",
        "type": "multi",
        "options": [
            ("cooking", "Baking & Cooking"), ("food_culture", "Food Culture & Dining"),
            ("coffee", "Coffee, Tea & Drinks"), ("food_science", "Food Science & Sustainable Food"),
        ],
    },
    "tech": {
        "question": "What sounds most interesting?",
        "type": "multi",
        "options": [
            ("makers", "Makers & 3D Printing"), ("electronics", "Hobby Electronics & Radio"),
            ("computing", "Gadgets & Computing"), ("creative_coding", "Creative Coding & Digital"),
        ],
    },
    "outdoors": {
        "question": "What would you like to do?",
        "type": "multi",
        "options": [
            ("hiking", "Hiking & Camping"), ("paddling", "Paddling & Water Recreation"),
            ("wildlife", "Wildlife, Birds & Animals"), ("plants", "Plants, Gardening & Farming"),
            ("astronomy", "Nature Study & Astronomy"),
        ],
    },
    "sustainability": {
        "question": "What interests you most?",
        "type": "multi",
        "options": [
            ("climate", "Sustainability & Climate"), ("conservation", "Conservation & Environment"),
            ("sustainable_food", "Sustainable Food"), ("gardening", "Gardening & Agriculture"),
            ("environmental_advocacy", "Environmental Advocacy"),
        ],
    },
    "cultural": {
        "question": "What communities or cultures would you like to explore?",
        "type": "multi",
        "options": [
            ("east_asian", "East Asian"), ("south_asian", "South Asian"),
            ("southeast_asian", "Southeast Asian"), ("latam", "Latin American & Caribbean"),
            ("black_diaspora", "Black & African Diaspora"), ("middle_east", "Middle Eastern & Mediterranean"),
            ("european", "European"), ("pacific_native", "Pacific, Native & Regional"),
            ("multicultural", "Multicultural & Pan-Ethnic"),
        ],
    },
    "language": {
        "question": "What interests you?",
        "type": "multi",
        "options": [
            ("language_practice", "Language Tables & Practice"), ("exchange", "Cultural Exchange"),
            ("international", "International Communities"), ("global_learning", "Travel & Global Learning"),
        ],
    },
    "identity": {
        "question": "What kind of community are you interested in?",
        "type": "multi",
        "options": [
            ("lgbtq", "LGBTQ+ Community"), ("women_gender", "Women & Gender Community"),
            ("first_gen", "First-Gen & Community Support"), ("wellness_support", "Wellness & Support Communities"),
            ("identity_other", "Other Identity-Based Communities"), ("belonging", "General Community & Belonging"),
        ],
    },
    "faith": {
        "question": "What interests you?",
        "type": "multi",
        "options": [
            ("christian", "Christian Fellowship"), ("jewish", "Jewish Life"),
            ("muslim", "Muslim Life"), ("sikh_hindu_other", "Sikh, Hindu & Other Faiths"),
            ("interfaith", "Interfaith"), ("mindfulness", "Mindfulness & Wellness"),
        ],
    },
    "service": {
        "question": "What kind of service interests you?",
        "type": "multi",
        "options": [
            ("youth_education", "Youth & Education"), ("health_service", "Health & Global Health"),
            ("community_hunger", "Community & Hunger Relief"), ("fundraising", "Fundraising & Awareness"),
            ("outreach", "Volunteer Service & Outreach"), ("animal_service", "Animal Welfare & Service"),
        ],
    },
    "advocacy": {
        "question": "What interests you?",
        "type": "multi",
        "options": [
            ("political", "Political & Policy Groups"), ("social_justice", "Social Justice Advocacy"),
            ("debate", "Debate & Public Speaking"), ("civic", "Civic Engagement"),
            ("policy_research", "Policy Research & Discussion"),
        ],
    },
    "vibe": {
        "question": "What kind of club experience are you looking for?",
        "type": "multi",
        "max_selections": 3,
        "options": [
            ("social", "Social"), ("relaxed", "Relaxed"), ("creative", "Creative"),
            ("intellectual", "Intellectual"), ("competitive", "Competitive"),
            ("physical", "Physical / Active"), ("performance", "Performance-Oriented"),
            ("service", "Service-Oriented"),
        ],
    },
    "goals": {
        "question": "What are you hoping to get out of a club?",
        "type": "multi",
        "options": [
            ("meet_people", "Meet new people"), ("learn", "Learn a skill"),
            ("fun", "Have fun"), ("resume", "Build my resume"), ("active", "Stay active"),
            ("community", "Find a community"), ("compete", "Compete"),
            ("create", "Create / perform"), ("give_back", "Give back"),
            ("explore", "Explore a new interest"),
        ],
    },
    "time": {
        "question": "How much time do you want to spend on a club?",
        "type": "single",
        "options": [
            ("lt1", "Less than 1 hour/week"), ("1_3", "1–3 hours/week"),
            ("3_5", "3–5 hours/week"), ("5_10", "5–10 hours/week"),
            ("10_plus", "10+ hours/week"), ("flexible", "Flexible"),
        ],
    },
    "beginner": {
        "question": "How important is it that the club is beginner-friendly?",
        "type": "single",
        "options": [
            ("very", "Very important"), ("somewhat", "Somewhat important"),
            ("not", "Not important"), ("experienced", "I prefer experienced groups"),
        ],
    },
    "requirements": {
        "question": "How do you feel about auditions or applications?",
        "type": "single",
        "options": [
            ("avoid", "I want to avoid them"), ("application", "I'm okay with an application"),
            ("audition", "I'm okay with an audition"), ("either", "Either is fine"),
        ],
    },
    "size": {
        "question": "What club size do you prefer?",
        "type": "single",
        "options": [
            ("small", "Small"), ("medium", "Medium"), ("large", "Large"),
            ("any", "No preference"),
        ],
    },
    "days": {
        "question": "When are you generally available?",
        "type": "multi",
        "options": [
            ("monday", "Monday"), ("tuesday", "Tuesday"), ("wednesday", "Wednesday"),
            ("thursday", "Thursday"), ("friday", "Friday"), ("saturday", "Saturday"),
            ("sunday", "Sunday"),
        ],
    },
    "free_text": {
        "question": "In your own words, what would your ideal club experience look like?",
        "type": "text",
        "options": [],
    },
}

CATEGORY_TO_KEY = {
    "Music & Singing": "music", "Dance & Movement": "dance",
    "Theatre, Comedy & Storytelling": "theatre", "Visual Arts, Crafts & Design": "visual_arts",
    "Writing, Media & Publications": "writing_media", "Games, Puzzles & Fandom": "games",
    "Food & Drink": "food", "Tech & Making": "tech", "Outdoors, Nature & Animals": "outdoors",
    "Sustainability & Environment": "sustainability", "Cultural & Heritage": "cultural",
    "Language & Global Exchange": "language", "Identity & Community": "identity",
    "Faith, Spirituality & Mindfulness": "faith", "Service & Volunteering": "service",
    "Advocacy, Politics & Debate": "advocacy",
}

def next_questions(answers: dict[str, Any]) -> list[str]:
    selected = answers.get("categories", [])
    result = []
    for category in selected:
        key = CATEGORY_TO_KEY.get(category, category)
        if key in QUESTIONS:
            result.append(key)
    result.extend(["vibe", "goals", "time", "beginner", "requirements", "size", "days", "free_text"])
    # De-duplicate while preserving order and cap adaptive quiz length.
    return list(dict.fromkeys(result))[:12]

def get_question(question_id: str) -> dict[str, Any]:
    q = QUESTIONS[question_id]
    return {
        "id": question_id,
        "question": q["question"],
        "type": q["type"],
        "max_selections": q.get("max_selections"),
        "options": [{"id": x, "label": y} for x, y in q["options"]],
    }
