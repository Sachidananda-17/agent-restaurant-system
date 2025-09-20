"""
Agent Configuration for 3-Agent Collaborative System
"""

# === AGENT ADDRESSES (will be generated) ===
AGENTS = {
    "alice": {
        "name": "alice_data_collector",
        "seed": "alice_collaborative_seed_2024",
        "port": 8000,
        "role": "Data Collector & Problem Identifier",
        "endpoint": "http://localhost:8000/submit"
    },
    "bob": {
        "name": "bob_analyzer", 
        "seed": "bob_analysis_seed_2024",
        "port": 8001,
        "role": "Solution Analyzer & Processor",
        "endpoint": "http://localhost:8001/submit"
    },
    "charlie": {
        "name": "charlie_coordinator",
        "seed": "charlie_decision_seed_2024", 
        "port": 8002,
        "role": "Final Decision Maker & Coordinator",
        "endpoint": "http://localhost:8002/submit"
    }
}

# === SYSTEM CONFIGURATION ===
SYSTEM_CONFIG = {
    "task_timeout": 60,  # seconds
    "max_retries": 3,
    "decision_threshold": 0.7,  # minimum confidence for decisions
    "collaboration_mode": "restaurant_recommendation"
}

# === SAMPLE DATA FOR TESTING ===
SAMPLE_RESTAURANT_DATA = {
    "restaurants": [
        {
            "name": "Pizza Palace",
            "cuisine": "Italian", 
            "rating": 4.2,
            "price": "$$",
            "location": "Downtown",
            "features": ["delivery", "outdoor_seating"]
        },
        {
            "name": "Sushi Zen",
            "cuisine": "Japanese",
            "rating": 4.7,
            "price": "$$$", 
            "location": "Uptown",
            "features": ["fresh_fish", "sake_bar"]
        },
        {
            "name": "Burger Barn",
            "cuisine": "American",
            "rating": 4.0,
            "price": "$",
            "location": "Suburbs", 
            "features": ["family_friendly", "drive_through"]
        },
        {
            "name": "Spice Garden",
            "cuisine": "Indian",
            "rating": 4.5,
            "price": "$$",
            "location": "City Center",
            "features": ["vegetarian_options", "spicy_levels"]
        },
        {
            "name": "French Bistro",
            "cuisine": "French",
            "rating": 4.8,
            "price": "$$$$",
            "location": "Historic District",
            "features": ["wine_pairing", "romantic_atmosphere"]
        }
    ]
}
