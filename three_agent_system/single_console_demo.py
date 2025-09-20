"""
Single Console Demo - All Three Agents in One Terminal
Shows clear collaboration between Alice, Bob, and Charlie in real-time
"""

import asyncio
import datetime
import random
import time
from typing import Dict, List

# Simulate the message models
class TaskData:
    def __init__(self, task_id: str, user_request: str, preferences: dict, location: dict, confidence: float):
        self.task_id = task_id
        self.user_request = user_request
        self.preferences = preferences
        self.location = location
        self.confidence = confidence

class AnalysisResult:
    def __init__(self, task_id: str, recommendations: list, confidence: float, summary: str):
        self.task_id = task_id
        self.recommendations = recommendations
        self.confidence = confidence
        self.summary = summary

class FinalDecision:
    def __init__(self, task_id: str, choice: dict, reasoning: str, confidence: float):
        self.task_id = task_id
        self.choice = choice
        self.reasoning = reasoning
        self.confidence = confidence

# Sample restaurant data
RESTAURANTS = [
    {"name": "Pizza Palace", "cuisine": "Italian", "rating": 4.2, "price": "$$", "location": "Downtown", "features": ["delivery", "family_friendly"]},
    {"name": "Sushi Zen", "cuisine": "Japanese", "rating": 4.7, "price": "$$$", "location": "Uptown", "features": ["fresh_fish", "sake_bar"]},
    {"name": "French Bistro", "cuisine": "French", "rating": 4.8, "price": "$$$$", "location": "Historic District", "features": ["wine_pairing", "romantic_atmosphere"]},
    {"name": "Burger Barn", "cuisine": "American", "rating": 4.0, "price": "$", "location": "Suburbs", "features": ["drive_through", "family_friendly"]},
    {"name": "Spice Garden", "cuisine": "Indian", "rating": 4.5, "price": "$$", "location": "City Center", "features": ["vegetarian_options", "spicy_levels"]}
]

# Sample user requests
USER_REQUESTS = [
    "Find me a romantic restaurant for date night",
    "I want family-friendly pizza place nearby", 
    "Looking for authentic sushi with good ratings",
    "Need a budget-friendly lunch spot downtown",
    "Find upscale French restaurant for business dinner"
]

def print_separator(title: str):
    """Print a clear separator for each agent"""
    print("\n" + "="*60)
    print(f"🤖 {title}")
    print("="*60)

def print_step(step: str, agent: str, message: str):
    """Print a formatted step"""
    icons = {"Alice": "🔍", "Bob": "🧠", "Charlie": "👑"}
    print(f"{icons.get(agent, '🤖')} {agent}: {message}")

class AliceAgent:
    """Simulated Alice - Data Collector"""
    
    def __init__(self):
        self.agent_name = "Alice"
        self.address = "agent1qalice123..."
        
    def collect_user_data(self, user_request: str) -> TaskData:
        """Alice collects and processes user data"""
        task_id = f"task_{datetime.datetime.now().strftime('%H%M%S')}"
        
        print_separator("ALICE - DATA COLLECTION PHASE")
        print_step("STARTING", "Alice", f"New task initiated: {task_id}")
        print_step("INPUT", "Alice", f"User request: '{user_request}'")
        
        # Simulate Alice's analysis
        preferences = {}
        location = {}
        
        # Analyze request
        request_lower = user_request.lower()
        if "romantic" in request_lower:
            preferences = {"cuisine": "French", "occasion": "romantic", "price_range": "$$$$"}
            location = {"area": "Historic District"}
        elif "family" in request_lower or "pizza" in request_lower:
            preferences = {"cuisine": "Italian", "occasion": "family", "price_range": "$$"}
            location = {"area": "nearby"}
        elif "sushi" in request_lower:
            preferences = {"cuisine": "Japanese", "occasion": "casual", "price_range": "$$$"}
            location = {"area": "city_wide"}
        elif "budget" in request_lower or "lunch" in request_lower:
            preferences = {"cuisine": "American", "occasion": "casual", "price_range": "$"}
            location = {"area": "Downtown"}
        else:
            preferences = {"cuisine": "any", "occasion": "casual", "price_range": "$$"}
            location = {"area": "city_wide"}
        
        confidence = 0.85
        
        print_step("ANALYSIS", "Alice", f"Extracted preferences: {preferences}")
        print_step("LOCATION", "Alice", f"Location data: {location}")
        print_step("CONFIDENCE", "Alice", f"Data collection confidence: {confidence}")
        print_step("SUCCESS", "Alice", f"✅ Data collection complete - sending to Bob")
        
        return TaskData(task_id, user_request, preferences, location, confidence)

class BobAgent:
    """Simulated Bob - Solution Analyzer"""
    
    def __init__(self):
        self.agent_name = "Bob"
        self.address = "agent1qbob456..."
        
    def analyze_data(self, task_data: TaskData) -> AnalysisResult:
        """Bob performs comprehensive analysis"""
        
        print_separator("BOB - ANALYSIS PHASE")
        print_step("RECEIVED", "Bob", f"Analysis request for {task_data.task_id}")
        print_step("DATA", "Bob", f"From Alice - User wants: {task_data.user_request}")
        
        # Stage 1: Filter restaurants
        print_step("STAGE 1", "Bob", "🔄 Filtering restaurants based on criteria...")
        filtered = self.filter_restaurants(task_data.preferences, task_data.location)
        print_step("STAGE 1", "Bob", f"📊 Filtered to {len(filtered)} restaurants")
        
        # Stage 2: Score restaurants  
        print_step("STAGE 2", "Bob", "🔄 Scoring and ranking restaurants...")
        scored = self.score_restaurants(filtered, task_data.preferences)
        print_step("STAGE 2", "Bob", "📊 Scoring completed")
        
        # Stage 3: Generate recommendations
        print_step("STAGE 3", "Bob", "🔄 Generating recommendations...")
        recommendations = self.create_recommendations(scored)
        print_step("STAGE 3", "Bob", f"📊 Generated {len(recommendations)} recommendations")
        
        # Stage 4: Calculate confidence
        confidence = 0.88
        print_step("STAGE 4", "Bob", f"📊 Analysis confidence: {confidence}")
        
        if recommendations:
            summary = f"Analyzed {len(RESTAURANTS)} restaurants, filtered to {len(filtered)}, top choice: {recommendations[0]['name']}"
        else:
            summary = f"Analyzed {len(RESTAURANTS)} restaurants, filtered to {len(filtered)}, no suitable matches found"
        print_step("COMPLETE", "Bob", f"✅ Analysis complete - sending to Charlie")
        
        return AnalysisResult(task_data.task_id, recommendations, confidence, summary)
    
    def filter_restaurants(self, preferences: dict, location: dict) -> List[dict]:
        """Filter restaurants based on preferences"""
        filtered = []
        for restaurant in RESTAURANTS:
            # Cuisine filter (more flexible)
            if preferences.get("cuisine", "any") != "any":
                if restaurant["cuisine"] != preferences.get("cuisine"):
                    continue
            
            # Price filter (more inclusive)
            price_range = preferences.get("price_range", "$$")
            if price_range == "$":
                if restaurant["price"] not in ["$", "$$"]:
                    continue
            elif price_range == "$$$":
                if restaurant["price"] not in ["$$", "$$$", "$$$$"]:
                    continue
                    
            filtered.append(restaurant)
        
        # Return at least 2-3 restaurants, fallback to all if needed
        if len(filtered) < 2:
            return RESTAURANTS[:3]
        return filtered[:3]
    
    def score_restaurants(self, restaurants: List[dict], preferences: dict) -> List[dict]:
        """Score and rank restaurants"""
        scored = []
        for restaurant in restaurants:
            # Simple scoring algorithm
            score = restaurant["rating"] / 5.0  # Base score from rating
            
            # Bonus for occasion match
            occasion = preferences.get("occasion", "casual")
            if occasion == "romantic" and "romantic_atmosphere" in restaurant.get("features", []):
                score += 0.2
            elif occasion == "family" and "family_friendly" in restaurant.get("features", []):
                score += 0.2
                
            restaurant["analysis_score"] = min(score, 1.0)
            scored.append(restaurant)
        
        return sorted(scored, key=lambda x: x["analysis_score"], reverse=True)
    
    def create_recommendations(self, scored_restaurants: List[dict]) -> List[dict]:
        """Create final recommendations"""
        recommendations = []
        for i, restaurant in enumerate(scored_restaurants):
            rec = {
                "rank": i + 1,
                "name": restaurant["name"],
                "cuisine": restaurant["cuisine"],
                "rating": restaurant["rating"],
                "price": restaurant["price"],
                "location": restaurant["location"],
                "analysis_score": restaurant["analysis_score"],
                "reasoning": f"High rating ({restaurant['rating']}/5.0) and good feature match"
            }
            recommendations.append(rec)
        return recommendations

class CharlieAgent:
    """Simulated Charlie - Decision Coordinator"""
    
    def __init__(self):
        self.agent_name = "Charlie"
        self.address = "agent1qcharlie789..."
        
    def make_decision(self, analysis_result: AnalysisResult) -> FinalDecision:
        """Charlie makes the final decision"""
        
        print_separator("CHARLIE - DECISION PHASE")
        print_step("RECEIVED", "Charlie", f"Decision request for {analysis_result.task_id}")
        print_step("SUMMARY", "Charlie", f"Bob's analysis: {analysis_result.summary}")
        print_step("OPTIONS", "Charlie", f"🏆 {len(analysis_result.recommendations)} options to evaluate")
        
        # Decision process
        print_step("STAGE 1", "Charlie", f"🔄 Validating analysis quality...")
        quality_score = analysis_result.confidence
        print_step("STAGE 1", "Charlie", f"📊 Analysis quality: {quality_score:.2f}")
        
        print_step("STAGE 2", "Charlie", "🔄 Applying decision criteria...")
        
        # Choose top recommendation
        if not analysis_result.recommendations:
            # Fallback decision
            final_choice = {"name": "No Match Found", "cuisine": "N/A", "rating": 0, "price": "N/A", "location": "N/A"}
            reasoning = "No suitable restaurants found matching the criteria. Consider broadening search parameters."
            decision_confidence = 0.3
            print_step("STAGE 3", "Charlie", "🔄 No suitable matches found")
        else:
            top_choice = analysis_result.recommendations[0]
            print_step("STAGE 3", "Charlie", f"🔄 Final decision: {top_choice['name']}")
            decision_confidence = 0.92
            reasoning = f"Selected {top_choice['name']} due to excellent rating ({top_choice['rating']}/5.0) and strong analysis score ({top_choice['analysis_score']:.2f})"
            
            final_choice = {
                "name": top_choice["name"],
                "cuisine": top_choice["cuisine"],
                "rating": top_choice["rating"],
                "price": top_choice["price"],
                "location": top_choice["location"]
            }
        
        print_step("CONFIDENCE", "Charlie", f"📊 Decision confidence: {decision_confidence}")
        print_step("REASONING", "Charlie", f"💭 {reasoning}")
        
        print_step("BROADCAST", "Charlie", "📢 Broadcasting final decision to team...")
        
        return FinalDecision(analysis_result.task_id, final_choice, reasoning, decision_confidence)

def print_final_summary(decision: FinalDecision):
    """Print the final decision summary"""
    print_separator("FINAL DECISION SUMMARY")
    print(f"🎉 COLLABORATION COMPLETE FOR {decision.task_id}")
    print()
    print(f"🏆 CHOSEN RESTAURANT: {decision.choice['name']}")
    print(f"🍽️ Cuisine: {decision.choice['cuisine']}")
    print(f"⭐ Rating: {decision.choice['rating']}/5.0")
    print(f"💰 Price: {decision.choice['price']}")
    print(f"📍 Location: {decision.choice['location']}")
    print(f"📊 Confidence: {decision.confidence:.2f}")
    print(f"💭 Reasoning: {decision.reasoning}")
    print()
    print("✅ Task completed successfully!")
    print("🔄 Ready for next collaboration...")

def run_collaboration_demo():
    """Run a complete collaboration demo"""
    print("🎯 3-AGENT COLLABORATIVE SYSTEM - SINGLE CONSOLE DEMO")
    print("Current Time:", datetime.datetime.now().strftime("%H:%M:%S"))
    print()
    print("🤖 AGENTS:")
    print("🔍 Alice - Data Collector & Problem Identifier")
    print("🧠 Bob - Solution Analyzer & Processor")  
    print("👑 Charlie - Final Decision Maker & Coordinator")
    print()
    print("🚀 Starting collaboration workflow...")
    
    # Initialize agents
    alice = AliceAgent()
    bob = BobAgent()
    charlie = CharlieAgent()
    
    # Run collaboration
    user_request = random.choice(USER_REQUESTS)
    
    # Step 1: Alice collects data
    task_data = alice.collect_user_data(user_request)
    time.sleep(1)
    
    # Step 2: Bob analyzes  
    analysis = bob.analyze_data(task_data)
    time.sleep(1)
    
    # Step 3: Charlie decides
    decision = charlie.make_decision(analysis)
    time.sleep(1)
    
    # Step 4: Final summary
    print_final_summary(decision)

def main():
    """Main demo function"""
    try:
        while True:
            run_collaboration_demo()
            
            print("\n" + "="*60)
            print("⏳ Next collaboration in 10 seconds...")
            print("🛑 Press Ctrl+C to stop")
            print("="*60)
            
            time.sleep(10)
            print("\n" * 2)  # Clear space
            
    except KeyboardInterrupt:
        print("\n\n👋 Collaboration demo stopped")
        print("🎊 Thank you for watching the 3-agent system in action!")

if __name__ == "__main__":
    main()
