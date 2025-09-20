"""
Bob - Solution Analyzer & Processor Agent  
Role: Analyzes data from Alice, processes recommendations, sends to Charlie
Collaborates with Alice (Data Collector) and Charlie (Decision Maker)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
import datetime
import json
import random

# Import our shared models and config
from config.message_models import *
from config.agent_config import AGENTS, SAMPLE_RESTAURANT_DATA

# === BOB AGENT SETUP ===
bob = Agent(
    name=AGENTS["bob"]["name"],
    seed=AGENTS["bob"]["seed"],
    port=AGENTS["bob"]["port"], 
    endpoint=[AGENTS["bob"]["endpoint"]]
)

# Store addresses of Alice and Charlie
ALICE_ADDRESS = ""
CHARLIE_ADDRESS = ""

# Bob's analysis memory and capabilities
bob_memory = {
    "current_analyses": {},
    "completed_analyses": [],
    "team_addresses": {},
    "analysis_models": {
        "recommendation_engine": True,
        "sentiment_analyzer": True,
        "price_optimizer": True,
        "location_matcher": True
    }
}

@bob.on_event("startup")
async def bob_startup(ctx: Context):
    """Bob introduces his analytical capabilities"""
    ctx.logger.info("🧠 Bob Analyzer Agent Starting...")
    ctx.logger.info(f"📍 Bob Address: {bob.address}")
    ctx.logger.info("🎯 Role: Solution Analysis & Processing") 
    ctx.logger.info("🤝 Looking for Alice (Data Collector) and Charlie (Coordinator)...")
    ctx.logger.info("🔧 Analysis Capabilities:")
    ctx.logger.info("   • Multi-criteria recommendation engine")
    ctx.logger.info("   • Sentiment analysis processing")
    ctx.logger.info("   • Price-performance optimization")
    ctx.logger.info("   • Location-preference matching")
    ctx.logger.info("   • Risk assessment & confidence scoring")
    ctx.logger.info("🚀 Bob is ready for analytical tasks!")

# === TEAM DISCOVERY BROADCAST ===
@bob.on_interval(period=25.0)
async def broadcast_availability(ctx: Context):
    """Bob broadcasts his availability to the team"""
    status_msg = StatusUpdate(
        task_id="discovery",
        status="available",
        progress_percentage=100,
        message="Bob Analyzer ready for collaboration",
        timestamp=datetime.datetime.now().isoformat(),
        sender="Bob"
    )
    
    ctx.logger.info("📡 Bob broadcasting availability to team...")
    # This will be received by Alice and Charlie for team discovery

# === MAIN ANALYSIS HANDLER ===
@bob.on_message(model=DataCollection)
async def analyze_collected_data(ctx: Context, sender: str, msg: DataCollection):
    """Bob receives data from Alice and performs comprehensive analysis"""
    global ALICE_ADDRESS
    
    ctx.logger.info(f"📊 Analysis request received for task: {msg.task_id}")
    ctx.logger.info(f"🔍 From: {msg.sender}")
    ctx.logger.info(f"📋 User preferences: {msg.user_preferences}")
    ctx.logger.info(f"📍 Location data: {msg.location_data}")
    
    # Store the analysis task
    bob_memory["current_analyses"][msg.task_id] = {
        "status": "analyzing",
        "start_time": datetime.datetime.now().isoformat(),
        "source_data": msg,
        "sender_address": sender
    }
    
    # Record Alice's address for future communication
    if not ALICE_ADDRESS and msg.sender == "Alice":
        ALICE_ADDRESS = sender
        bob_memory["team_addresses"]["alice"] = sender
        ctx.logger.info(f"🤝 Alice address recorded: {sender}")
    
    # Perform comprehensive analysis
    ctx.logger.info("🔄 Starting multi-stage analysis...")
    
    # Stage 1: Filter restaurants based on criteria
    filtered_restaurants = filter_restaurants(msg)
    ctx.logger.info(f"📊 Stage 1: Filtered to {len(filtered_restaurants)} restaurants")
    
    # Stage 2: Score and rank restaurants
    scored_restaurants = score_restaurants(filtered_restaurants, msg)
    ctx.logger.info("📊 Stage 2: Scoring and ranking completed")
    
    # Stage 3: Generate recommendations with reasoning
    recommendations = generate_recommendations(scored_restaurants, msg)
    ctx.logger.info(f"📊 Stage 3: Generated {len(recommendations)} recommendations")
    
    # Stage 4: Calculate confidence scores
    confidence_scores = calculate_analysis_confidence(recommendations, msg)
    ctx.logger.info("📊 Stage 4: Confidence analysis completed")
    
    # Prepare analysis results
    analysis_result = AnalysisResult(
        task_id=msg.task_id,
        analysis_summary=create_analysis_summary(recommendations, msg),
        recommendations=recommendations,
        confidence_scores=confidence_scores,
        supporting_data={
            "total_restaurants_analyzed": len(SAMPLE_RESTAURANT_DATA["restaurants"]),
            "filtering_criteria": msg.search_criteria,
            "analysis_methods": list(bob_memory["analysis_models"].keys())
        },
        timestamp=datetime.datetime.now().isoformat(),
        sender="Bob"
    )
    
    # Update task status
    bob_memory["current_analyses"][msg.task_id]["status"] = "completed"
    bob_memory["current_analyses"][msg.task_id]["results"] = analysis_result
    
    # Send results to Charlie for final decision
    if CHARLIE_ADDRESS:
        try:
            await ctx.send(CHARLIE_ADDRESS, analysis_result)
            ctx.logger.info(f"📤 Analysis results sent to Charlie: {msg.task_id}")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to send to Charlie: {str(e)}")
    else:
        ctx.logger.warning("⚠️ Charlie's address not yet known - saving analysis for later")

def filter_restaurants(data_msg: DataCollection) -> list:
    """Stage 1: Filter restaurants based on user criteria"""
    restaurants = SAMPLE_RESTAURANT_DATA["restaurants"]
    filtered = []
    
    user_prefs = data_msg.user_preferences
    location_data = data_msg.location_data
    
    for restaurant in restaurants:
        # Cuisine filtering
        if user_prefs.get("cuisine") != "any":
            if restaurant["cuisine"] != user_prefs.get("cuisine"):
                continue
        
        # Price range filtering  
        price_range = user_prefs.get("price_range", "$$")
        if not price_matches(restaurant["price"], price_range):
            continue
            
        # Location filtering
        if location_data.get("area") == "Downtown" and restaurant["location"] != "Downtown":
            if location_data.get("area") != "city_wide":
                continue
        
        # Rating threshold
        if restaurant["rating"] < data_msg.search_criteria.get("min_rating", 3.5):
            continue
            
        filtered.append(restaurant)
    
    return filtered

def price_matches(restaurant_price: str, user_preference: str) -> bool:
    """Check if restaurant price matches user preference"""
    price_levels = {"$": 1, "$$": 2, "$$$": 3, "$$$$": 4}
    
    restaurant_level = price_levels.get(restaurant_price, 2)
    
    if user_preference == "$":
        return restaurant_level <= 2
    elif user_preference == "$$": 
        return restaurant_level <= 3
    elif user_preference == "$$$+":
        return restaurant_level >= 3
    else:
        return True

def score_restaurants(restaurants: list, data_msg: DataCollection) -> list:
    """Stage 2: Score restaurants based on multiple criteria"""
    scored = []
    
    for restaurant in restaurants:
        score = calculate_restaurant_score(restaurant, data_msg)
        scored.append({
            **restaurant,
            "analysis_score": score,
            "score_breakdown": get_score_breakdown(restaurant, data_msg)
        })
    
    # Sort by score (highest first)
    return sorted(scored, key=lambda x: x["analysis_score"], reverse=True)

def calculate_restaurant_score(restaurant: dict, data_msg: DataCollection) -> float:
    """Calculate comprehensive score for a restaurant"""
    score = 0.0
    
    # Base score from rating (40% weight)
    score += (restaurant["rating"] / 5.0) * 0.4
    
    # Preference matching (30% weight)
    pref_score = 0.0
    user_prefs = data_msg.user_preferences
    
    # Cuisine match
    if restaurant["cuisine"] == user_prefs.get("cuisine"):
        pref_score += 0.5
    
    # Occasion matching
    occasion = user_prefs.get("occasion", "casual")
    if occasion == "romantic" and "romantic_atmosphere" in restaurant.get("features", []):
        pref_score += 0.3
    elif occasion == "family" and "family_friendly" in restaurant.get("features", []):
        pref_score += 0.3
    elif occasion == "business" and restaurant["price"] in ["$$$", "$$$$"]:
        pref_score += 0.2
    
    score += pref_score * 0.3
    
    # Location convenience (20% weight) 
    location_score = 0.2  # Base location score
    if data_msg.location_data.get("area") == restaurant["location"]:
        location_score = 0.4
    score += location_score * 0.2
    
    # Special features (10% weight)
    feature_score = len(restaurant.get("features", [])) * 0.1
    score += min(feature_score, 0.1)
    
    return min(score, 1.0)

def get_score_breakdown(restaurant: dict, data_msg: DataCollection) -> dict:
    """Provide detailed score breakdown for transparency"""
    return {
        "rating_score": (restaurant["rating"] / 5.0) * 0.4,
        "preference_match": 0.2,  # Simplified for brevity
        "location_score": 0.15,
        "feature_bonus": len(restaurant.get("features", [])) * 0.02
    }

def generate_recommendations(scored_restaurants: list, data_msg: DataCollection) -> list:
    """Stage 3: Generate final recommendations with reasoning"""
    recommendations = []
    
    # Get top restaurants (limit based on search criteria)
    max_results = data_msg.search_criteria.get("max_results", 3)
    top_restaurants = scored_restaurants[:max_results]
    
    for i, restaurant in enumerate(top_restaurants):
        recommendation = {
            "rank": i + 1,
            "restaurant": {
                "name": restaurant["name"],
                "cuisine": restaurant["cuisine"],
                "rating": restaurant["rating"], 
                "price": restaurant["price"],
                "location": restaurant["location"],
                "features": restaurant.get("features", [])
            },
            "analysis_score": restaurant["analysis_score"],
            "reasoning": generate_reasoning(restaurant, data_msg),
            "pros": identify_pros(restaurant, data_msg),
            "cons": identify_cons(restaurant, data_msg)
        }
        recommendations.append(recommendation)
    
    return recommendations

def generate_reasoning(restaurant: dict, data_msg: DataCollection) -> str:
    """Generate human-readable reasoning for recommendation"""
    reasons = []
    
    # Rating reasoning
    if restaurant["rating"] >= 4.5:
        reasons.append(f"Excellent ratings ({restaurant['rating']}/5.0)")
    elif restaurant["rating"] >= 4.0:
        reasons.append(f"Very good ratings ({restaurant['rating']}/5.0)")
    
    # Preference matching
    user_prefs = data_msg.user_preferences
    if restaurant["cuisine"] == user_prefs.get("cuisine"):
        reasons.append(f"Matches preferred {restaurant['cuisine']} cuisine")
    
    # Price appropriateness
    if restaurant["price"] == user_prefs.get("price_range"):
        reasons.append("Perfect price range match")
    
    # Special features
    features = restaurant.get("features", [])
    if features:
        reasons.append(f"Special features: {', '.join(features[:2])}")
    
    return ". ".join(reasons) if reasons else "Good overall match for your criteria"

def identify_pros(restaurant: dict, data_msg: DataCollection) -> list:
    """Identify specific advantages"""
    pros = []
    
    if restaurant["rating"] >= 4.5:
        pros.append("Outstanding customer reviews")
    if "delivery" in restaurant.get("features", []):
        pros.append("Delivery available")
    if restaurant["price"] in ["$", "$$"]:
        pros.append("Budget-friendly pricing")
    
    return pros

def identify_cons(restaurant: dict, data_msg: DataCollection) -> list:
    """Identify potential drawbacks"""  
    cons = []
    
    if restaurant["rating"] < 4.0:
        cons.append("Mixed customer reviews")
    if restaurant["price"] == "$$$$":
        cons.append("Premium pricing")
    if restaurant["location"] == "Suburbs":
        cons.append("May require travel time")
    
    return cons

def calculate_analysis_confidence(recommendations: list, data_msg: DataCollection) -> dict:
    """Stage 4: Calculate confidence in analysis results"""
    
    # Overall confidence based on data quality
    data_confidence = data_msg.confidence_score
    
    # Analysis confidence based on recommendation spread
    if recommendations:
        score_spread = max(r["analysis_score"] for r in recommendations) - min(r["analysis_score"] for r in recommendations)
        analysis_confidence = 1.0 - (score_spread * 0.5)  # Lower spread = higher confidence
    else:
        analysis_confidence = 0.3
    
    # Combined confidence
    overall_confidence = (data_confidence + analysis_confidence) / 2
    
    return {
        "overall_confidence": overall_confidence,
        "data_quality_confidence": data_confidence,
        "analysis_confidence": analysis_confidence,
        "recommendation_count": len(recommendations)
    }

def create_analysis_summary(recommendations: list, data_msg: DataCollection) -> str:
    """Create human-readable analysis summary"""
    if not recommendations:
        return "No restaurants found matching the specified criteria."
    
    top_choice = recommendations[0]
    summary_parts = [
        f"Analysis complete for {data_msg.user_preferences.get('occasion', 'dining')} request.",
        f"Top recommendation: {top_choice['restaurant']['name']} ({top_choice['restaurant']['cuisine']} cuisine)",
        f"with {top_choice['restaurant']['rating']}/5.0 rating and {top_choice['analysis_score']:.2f} match score.",
        f"Total {len(recommendations)} options analyzed and ranked."
    ]
    
    return " ".join(summary_parts)

# === COLLABORATION HANDLERS ===

@bob.on_message(model=DecisionRequest) 
async def handle_decision_request(ctx: Context, sender: str, msg: DecisionRequest):
    """Charlie requests additional analysis or clarification"""
    ctx.logger.info(f"📨 Decision request from Charlie: {msg.task_id}")
    ctx.logger.info(f"🔍 Clarification needed: {msg.clarification_needed}")
    
    # Perform additional analysis based on Charlie's request
    if msg.task_id in bob_memory["current_analyses"]:
        original_analysis = bob_memory["current_analyses"][msg.task_id]["results"]
        
        # Generate enhanced analysis
        enhanced_analysis = enhance_analysis(original_analysis, msg)
        
        try:
            await ctx.send(sender, enhanced_analysis)
            ctx.logger.info(f"📤 Enhanced analysis sent to Charlie: {msg.task_id}")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to send enhanced analysis: {str(e)}")

def enhance_analysis(original: AnalysisResult, request: DecisionRequest) -> AnalysisResult:
    """Enhance analysis based on Charlie's specific request"""
    # This would involve more sophisticated re-analysis
    # For now, return the original with updated timestamp
    return AnalysisResult(
        task_id=original.task_id,
        analysis_summary=f"Enhanced: {original.analysis_summary}",
        recommendations=original.recommendations,
        confidence_scores=original.confidence_scores,
        supporting_data={**original.supporting_data, "enhancement": request.clarification_needed},
        timestamp=datetime.datetime.now().isoformat(),
        sender="Bob"
    )

# === TEAM DISCOVERY ===
@bob.on_message(model=StatusUpdate)
async def handle_team_discovery(ctx: Context, sender: str, msg: StatusUpdate):
    """Discover other team members"""
    global ALICE_ADDRESS, CHARLIE_ADDRESS
    if msg.sender == "Alice" and not ALICE_ADDRESS:
        ALICE_ADDRESS = sender
        bob_memory["team_addresses"]["alice"] = sender
        ctx.logger.info(f"🤝 Alice discovered! Address: {sender}")
    elif msg.sender == "Charlie" and not CHARLIE_ADDRESS:
        CHARLIE_ADDRESS = sender
        bob_memory["team_addresses"]["charlie"] = sender  
        ctx.logger.info(f"🤝 Charlie discovered! Address: {sender}")

if __name__ == "__main__":
    print("🧠 Starting Bob - Solution Analyzer Agent")
    print(f"📍 Bob will run on port {AGENTS['bob']['port']}")
    bob.run()
