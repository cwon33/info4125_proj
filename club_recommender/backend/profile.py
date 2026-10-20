
"""Translate raw quiz selections into the normalized profile used for ranking."""

from typing import Any

CATEGORY_MAP = {
    "music": "Music & Singing", "dance": "Dance & Movement",
    "theatre": "Theatre, Comedy & Storytelling", "visual_arts": "Visual Arts, Crafts & Design",
    "writing_media": "Writing, Media & Publications", "games": "Games, Puzzles & Fandom",
    "food": "Food & Drink", "tech": "Tech & Making", "outdoors": "Outdoors, Nature & Animals",
    "sustainability": "Sustainability & Environment", "cultural": "Cultural & Heritage",
    "language": "Language & Global Exchange", "identity": "Identity & Community",
    "faith": "Faith, Spirituality & Mindfulness", "service": "Service & Volunteering",
    "advocacy": "Advocacy, Politics & Debate",
}

SUBCATEGORY_MAP = {
    "a_cappella": "A Cappella", "choral": "Choral & Vocal", "instrumental": "Instrumental Ensembles",
    "jazz_rock": "Jazz, Rock & Contemporary", "world_music": "World & Cultural Music",
    "production": "Music Production & DJing", "live_music": "Live Music Events",
    "cultural_dance": "Cultural & Folk Dance", "partner_dance": "Social & Partner Dance",
    "street_dance": "Street & Hip-Hop Dance", "performance_dance": "Performance Troupes",
    "flow_circus": "Flow Arts & Circus", "improv": "Improv & Sketch Comedy",
    "theatre_prod": "Theatre Production", "storytelling": "Storytelling & Spoken Word",
    "standup": "Stand-up & Variety", "drawing": "Drawing & Painting", "crafts": "Crafts & Fiber Arts",
    "photo_film": "Photography & Film", "digital_art": "Digital Art & Animation", "fashion": "Fashion & Style",
    "publications": "Magazines & Publications", "creative_writing": "Creative Writing & Poetry",
    "broadcast": "Radio, Podcast & Broadcast", "books": "Book & Reading Clubs",
    "board_games": "Board & Card Games", "rpg": "Tabletop RPG & Miniatures",
    "video_games": "Video Games & Esports", "trivia": "Trivia, Puzzles & Strategy",
    "fandom": "Fandom, Film & Pop Culture", "collecting": "Collecting & Hobbyist Communities",
    "cooking": "Baking & Cooking", "food_culture": "Food Culture & Dining",
    "coffee": "Coffee, Tea & Drinks", "food_science": "Food Science & Sustainable Food",
    "makers": "Makers & 3D Printing", "electronics": "Hobby Electronics & Radio",
    "computing": "Gadgets & Computing", "creative_coding": "Creative Coding & Digital",
    "hiking": "Hiking & Camping", "paddling": "Paddling & Water Recreation",
    "wildlife": "Wildlife, Birds & Animals", "plants": "Plants, Gardening & Farming",
    "astronomy": "Nature Study & Astronomy", "climate": "Sustainability & Climate",
    "conservation": "Conservation & Environment", "sustainable_food": "Sustainable Food",
    "gardening": "Gardening & Agriculture", "environmental_advocacy": "Environmental Advocacy",
    "east_asian": "East Asian Culture", "south_asian": "South Asian Culture",
    "southeast_asian": "Southeast Asian Culture", "latam": "Latin American & Caribbean Culture",
    "black_diaspora": "Black & African Diaspora", "middle_east": "Middle Eastern & Mediterranean",
    "european": "European Culture", "pacific_native": "Pacific, Native & Regional Culture",
    "multicultural": "Multicultural & Pan-Ethnic", "language_practice": "Language Tables & Exchange",
    "exchange": "Cultural Exchange", "international": "International Communities",
    "global_learning": "Travel & Global Learning", "lgbtq": "LGBTQ+ Community",
    "women_gender": "Women & Gender Community", "first_gen": "First-Gen & Community Support",
    "wellness_support": "Wellness & Support Communities", "identity_other": "Identity-Based Communities",
    "belonging": "Community & Belonging", "christian": "Christian Fellowship", "jewish": "Jewish Life",
    "muslim": "Muslim Life", "sikh_hindu_other": "Sikh, Hindu & Other Faiths",
    "interfaith": "Interfaith", "mindfulness": "Mindfulness & Wellness",
    "youth_education": "Youth & Education Service", "health_service": "Health & Global Health Service",
    "community_hunger": "Community & Hunger Relief", "fundraising": "Fundraising & Awareness",
    "outreach": "Volunteer Service & Outreach", "animal_service": "Animal Welfare & Service",
    "political": "Political & Policy Groups", "social_justice": "Social Justice Advocacy",
    "debate": "Debate & Public Speaking", "civic": "Civic Engagement",
    "policy_research": "Policy Research & Discussion",
}

def profile_from_answers(answers: dict[str, Any]) -> dict[str, Any]:
    # Map quiz IDs to dataset labels and collect preference constraints.
    interests = []
    categories = answers.get("categories", [])
    selected_categories = [CATEGORY_MAP.get(value, value) for value in categories]
    interests.extend(selected_categories)

    category_subcategories = {}
    for category_id, category_name in CATEGORY_MAP.items():
        values = answers.get(category_id, [])
        if not isinstance(values, list):
            values = [values]
        subcategories = [SUBCATEGORY_MAP.get(value, value) for value in values]
        if subcategories:
            category_subcategories[category_name] = subcategories
            interests.extend(subcategories)

    vibe = {x: 1.0 for x in answers.get("vibe", [])}
    goals = {x: 1.0 for x in answers.get("goals", [])}

    time_map = {
        "lt1": (0, 1), "1_3": (1, 3), "3_5": (3, 5),
        "5_10": (5, 10), "10_plus": (10, 20), "flexible": (0, 20),
    }

    return {
        "interests": list(dict.fromkeys(interests)),
        "categories": selected_categories,
        "category_subcategories": category_subcategories,
        "vibe": vibe,
        "goals": goals,
        "time_range": time_map.get(answers.get("time"), (0, 20)),
        "beginner": answers.get("beginner"),
        "requirements": answers.get("requirements"),
        "size": answers.get("size"),
        "days": answers.get("days", []),
        "free_text": answers.get("free_text", ""),
    }
