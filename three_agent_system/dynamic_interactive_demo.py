"""
Dynamic Interactive 3-Agent System
Real user input, dynamic data sources, and interactive decision making
"""

import asyncio
import datetime
import json
import requests
import random
from typing import Dict, List, Optional
import os

# Dynamic data configuration
ENABLE_REAL_APIS = False  # Set True to use real APIs
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")
YELP_API_KEY = os.getenv("YELP_API_KEY", "")

class DynamicDataSource:
    """Handles dynamic data retrieval from various sources"""
    
    def __init__(self):
        self.real_apis_enabled = ENABLE_REAL_APIS and (GOOGLE_PLACES_API_KEY or YELP_API_KEY)
        
    def get_restaurants_by_location(self, location: str, cuisine: str = "", price_range: str = "") -> List[Dict]:
        """Get restaurants dynamically from APIs or enhanced simulation"""
        
        if self.real_apis_enabled:
            return self._get_real_restaurant_data(location, cuisine, price_range)
        else:
            return self._get_dynamic_simulated_data(location, cuisine, price_range)
    
    def _get_real_restaurant_data(self, location: str, cuisine: str, price_range: str) -> List[Dict]:
        """Fetch real restaurant data from APIs"""
        restaurants = []
        
        # Google Places API integration
        if GOOGLE_PLACES_API_KEY:
            try:
                query = f"{cuisine} restaurants in {location}"
                places_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
                params = {
                    'query': query,
                    'key': GOOGLE_PLACES_API_KEY,
                    'type': 'restaurant'
                }
                
                response = requests.get(places_url, params=params)
                data = response.json()
                
                for place in data.get('results', [])[:10]:
                    restaurant = {
                        'name': place.get('name'),
                        'rating': place.get('rating', 0),
                        'price_level': '$' * place.get('price_level', 2),
                        'address': place.get('formatted_address'),
                        'place_id': place.get('place_id'),
                        'cuisine': cuisine or 'Various',
                        'source': 'Google Places'
                    }
                    restaurants.append(restaurant)
                    
            except Exception as e:
                print(f"⚠️ Google Places API error: {e}")
        
        return restaurants
    
    def _get_dynamic_simulated_data(self, location: str, cuisine: str, price_range: str) -> List[Dict]:
        """Generate dynamic simulated restaurant data based on real patterns"""
        
        # Base restaurant types by cuisine
        restaurant_templates = {
            'Italian': ['Bella Vita', 'Giuseppe\'s', 'Roma Palace', 'Milano Bistro', 'Tuscany Garden'],
            'French': ['Le Jardin', 'Château Blanc', 'Paris Café', 'Bordeaux Bistro', 'Lyon Kitchen'],
            'Japanese': ['Sakura Sushi', 'Tokyo Ramen', 'Kyoto Garden', 'Osaka House', 'Zen Kitchen'],
            'American': ['Liberty Grill', 'Stars & Stripes', 'Main Street Diner', 'Heritage Burger', 'Golden Eagle'],
            'Indian': ['Spice Palace', 'Maharaja Kitchen', 'Delhi Garden', 'Bombay Express', 'Curry House'],
            'Chinese': ['Golden Dragon', 'Jade Garden', 'Beijing Palace', 'Szechuan House', 'Great Wall'],
            'Mexican': ['El Sombrero', 'Casa Miguel', 'Azteca Grill', 'Fiesta Cantina', 'Los Amigos']
        }
        
        # Generate restaurants dynamically
        restaurants = []
        cuisine_options = [cuisine] if cuisine else list(restaurant_templates.keys())
        
        for selected_cuisine in cuisine_options[:3]:  # Limit to 3 cuisines
            names = restaurant_templates.get(selected_cuisine, ['Generic Restaurant'])
            
            for i in range(random.randint(2, 4)):  # 2-4 restaurants per cuisine
                name = random.choice(names)
                if name not in [r['name'] for r in restaurants]:  # Avoid duplicates
                    
                    # Dynamic rating based on time and randomness
                    base_rating = random.uniform(3.5, 4.9)
                    time_factor = (datetime.datetime.now().hour % 12) / 12 * 0.3
                    rating = round(min(base_rating + time_factor, 5.0), 1)
                    
                    # Dynamic pricing
                    price_options = ['$', '$$', '$$$', '$$$$']
                    if price_range:
                        price = price_range
                    else:
                        price = random.choice(price_options)
                    
                    # Dynamic features based on cuisine and price
                    features = self._generate_dynamic_features(selected_cuisine, price)
                    
                    restaurant = {
                        'name': name,
                        'cuisine': selected_cuisine,
                        'rating': rating,
                        'price': price,
                        'location': self._generate_location(location),
                        'features': features,
                        'estimated_wait': random.randint(15, 45),
                        'phone': f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",
                        'hours': self._generate_hours(),
                        'source': 'Dynamic Simulation'
                    }
                    restaurants.append(restaurant)
        
        return restaurants
    
    def _generate_dynamic_features(self, cuisine: str, price: str) -> List[str]:
        """Generate realistic features based on cuisine and price"""
        base_features = ['takeout', 'dine_in', 'outdoor_seating']
        
        cuisine_features = {
            'Italian': ['wine_bar', 'family_style', 'fresh_pasta'],
            'French': ['wine_pairing', 'romantic_atmosphere', 'chef_specials'],
            'Japanese': ['sushi_bar', 'sake_selection', 'fresh_fish'],
            'American': ['sports_bar', 'burger_bar', 'craft_beer'],
            'Indian': ['spice_levels', 'vegetarian_options', 'buffet'],
            'Chinese': ['dim_sum', 'family_portions', 'tea_service'],
            'Mexican': ['margaritas', 'live_music', 'patio_dining']
        }
        
        price_features = {
            '$': ['casual_dining', 'quick_service'],
            '$$': ['table_service', 'moderate_portions'],
            '$$$': ['upscale_casual', 'wine_list'],
            '$$$$': ['fine_dining', 'valet_parking', 'dress_code']
        }
        
        features = base_features.copy()
        features.extend(cuisine_features.get(cuisine, []))
        features.extend(price_features.get(price, []))
        
        return random.sample(features, min(len(features), random.randint(3, 6)))
    
    def _generate_location(self, user_location: str) -> str:
        """Generate realistic location based on user input"""
        if 'downtown' in user_location.lower():
            areas = ['Downtown Core', 'Financial District', 'City Center']
        elif 'uptown' in user_location.lower():
            areas = ['Uptown', 'North District', 'Upper City']
        else:
            areas = ['Main Street', 'Oak Avenue', 'Park District', 'Riverside', 'Historic Quarter']
        
        return random.choice(areas)
    
    def _generate_hours(self) -> str:
        """Generate realistic operating hours"""
        opens = random.choice(['11:00 AM', '11:30 AM', '12:00 PM'])
        closes = random.choice(['9:00 PM', '9:30 PM', '10:00 PM', '10:30 PM'])
        return f"{opens} - {closes}"

class InteractiveAlice:
    """Dynamic Alice with real user interaction"""
    
    def __init__(self):
        self.data_source = DynamicDataSource()
        self.conversation_history = []
        
    def collect_user_input(self) -> Dict:
        """Get real user input interactively"""
        print("\n🔍 ALICE: Hi! I'm your restaurant recommendation assistant!")
        print("I'll help you find the perfect dining spot based on your preferences.\n")
        
        # Get user request
        user_request = input("💬 What kind of dining experience are you looking for? ").strip()
        
        if not user_request:
            user_request = "I want a good restaurant recommendation"
        
        print(f"\n🔍 Alice: Got it! '{user_request}'")
        
        # Ask follow-up questions for better recommendations
        location = input("📍 What area/location are you interested in? (or press Enter for anywhere): ").strip()
        if not location:
            location = "city-wide"
        
        cuisine_pref = input("🍽️ Any specific cuisine preference? (or press Enter for any): ").strip()
        if not cuisine_pref:
            cuisine_pref = "any"
        
        budget = input("💰 What's your budget range? ($/$$/$$$/$$$$, or press Enter for any): ").strip()
        if not budget:
            budget = "any"
        
        party_size = input("👥 How many people? (or press Enter for 2): ").strip()
        if not party_size:
            party_size = "2"
        
        # Generate task ID and collect dynamic data
        task_id = f"interactive_{datetime.datetime.now().strftime('%H%M%S')}"
        
        print(f"\n🔍 Alice: Perfect! Let me gather some options for you...")
        print("🔄 Searching restaurants...")
        
        # Get dynamic restaurant data
        restaurants = self.data_source.get_restaurants_by_location(location, cuisine_pref, budget)
        
        # Process user preferences
        preferences = {
            'original_request': user_request,
            'cuisine': cuisine_pref,
            'location': location,
            'budget': budget,
            'party_size': party_size,
            'occasion': self._detect_occasion(user_request)
        }
        
        # Store conversation
        self.conversation_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'user_request': user_request,
            'preferences': preferences,
            'restaurants_found': len(restaurants)
        })
        
        print(f"✅ Found {len(restaurants)} restaurants matching your criteria!")
        
        return {
            'task_id': task_id,
            'user_request': user_request,
            'preferences': preferences,
            'available_restaurants': restaurants,
            'confidence': 0.9
        }
    
    def _detect_occasion(self, request: str) -> str:
        """Detect occasion from user request using keyword analysis"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['date', 'romantic', 'anniversary', 'valentine']):
            return 'romantic'
        elif any(word in request_lower for word in ['business', 'meeting', 'client', 'professional']):
            return 'business'
        elif any(word in request_lower for word in ['family', 'kids', 'children', 'birthday']):
            return 'family'
        elif any(word in request_lower for word in ['celebration', 'party', 'special', 'event']):
            return 'celebration'
        else:
            return 'casual'

class DynamicBob:
    """Enhanced Bob with dynamic analysis capabilities"""
    
    def __init__(self):
        self.analysis_history = []
    
    def analyze_restaurants(self, alice_data: Dict) -> Dict:
        """Perform dynamic analysis on restaurant options"""
        
        print("\n🧠 BOB: Analyzing your restaurant options...")
        print("🔄 Running advanced multi-criteria analysis...\n")
        
        restaurants = alice_data['available_restaurants']
        preferences = alice_data['preferences']
        
        if not restaurants:
            print("❌ No restaurants found for analysis")
            return {
                'task_id': alice_data['task_id'],
                'recommendations': [],
                'confidence': 0.1,
                'analysis_summary': 'No restaurants available for analysis'
            }
        
        # Dynamic filtering based on preferences
        filtered = self._dynamic_filter(restaurants, preferences)
        print(f"📊 Stage 1: Filtered from {len(restaurants)} to {len(filtered)} restaurants")
        
        # Dynamic scoring with multiple criteria
        scored = self._dynamic_scoring(filtered, preferences)
        print("📊 Stage 2: Applied dynamic scoring algorithm")
        
        # Generate intelligent recommendations
        recommendations = self._generate_intelligent_recommendations(scored, preferences)
        print(f"📊 Stage 3: Generated {len(recommendations)} intelligent recommendations")
        
        # Calculate dynamic confidence
        confidence = self._calculate_dynamic_confidence(recommendations, preferences)
        print(f"📊 Stage 4: Analysis confidence: {confidence:.2f}")
        
        analysis_summary = f"Analyzed {len(restaurants)} restaurants using dynamic criteria matching user preferences"
        
        print("✅ Bob: Analysis complete - sending to Charlie for final decision\n")
        
        return {
            'task_id': alice_data['task_id'],
            'recommendations': recommendations,
            'confidence': confidence,
            'analysis_summary': analysis_summary,
            'total_analyzed': len(restaurants),
            'filtered_count': len(filtered)
        }
    
    def _dynamic_filter(self, restaurants: List[Dict], preferences: Dict) -> List[Dict]:
        """Dynamic filtering based on user preferences"""
        filtered = []
        
        for restaurant in restaurants:
            # Cuisine filter
            if preferences['cuisine'] != 'any':
                if preferences['cuisine'].lower() not in restaurant['cuisine'].lower():
                    continue
            
            # Budget filter
            if preferences['budget'] != 'any':
                if not self._matches_budget(restaurant['price'], preferences['budget']):
                    continue
            
            # Location preference (more flexible)
            if preferences['location'] != 'city-wide':
                if preferences['location'].lower() not in restaurant['location'].lower():
                    continue
            
            # Minimum rating filter
            if restaurant['rating'] < 3.5:
                continue
                
            filtered.append(restaurant)
        
        return filtered
    
    def _matches_budget(self, restaurant_price: str, user_budget: str) -> bool:
        """Check if restaurant price matches user budget"""
        price_values = {'$': 1, '$$': 2, '$$$': 3, '$$$$': 4}
        
        rest_level = price_values.get(restaurant_price, 2)
        budget_level = price_values.get(user_budget, 2)
        
        # Allow one level above/below budget
        return abs(rest_level - budget_level) <= 1
    
    def _dynamic_scoring(self, restaurants: List[Dict], preferences: Dict) -> List[Dict]:
        """Dynamic scoring based on multiple weighted criteria"""
        scored = []
        
        for restaurant in restaurants:
            score = 0.0
            
            # Rating weight (35%)
            score += (restaurant['rating'] / 5.0) * 0.35
            
            # Price appropriateness (20%)
            price_score = self._calculate_price_score(restaurant['price'], preferences['budget'])
            score += price_score * 0.20
            
            # Occasion match (25%)
            occasion_score = self._calculate_occasion_score(restaurant, preferences['occasion'])
            score += occasion_score * 0.25
            
            # Features and extras (15%)
            feature_score = len(restaurant.get('features', [])) * 0.02
            score += min(feature_score, 0.15)
            
            # Location convenience (5%)
            location_score = self._calculate_location_score(restaurant, preferences)
            score += location_score * 0.05
            
            restaurant['analysis_score'] = min(score, 1.0)
            restaurant['score_breakdown'] = {
                'rating_score': (restaurant['rating'] / 5.0) * 0.35,
                'price_score': price_score * 0.20,
                'occasion_score': occasion_score * 0.25,
                'feature_score': min(feature_score, 0.15),
                'location_score': location_score * 0.05
            }
            
            scored.append(restaurant)
        
        return sorted(scored, key=lambda x: x['analysis_score'], reverse=True)
    
    def _calculate_price_score(self, restaurant_price: str, user_budget: str) -> float:
        """Calculate price appropriateness score"""
        if user_budget == 'any':
            return 0.8  # Neutral score
        
        price_values = {'$': 1, '$$': 2, '$$$': 3, '$$$$': 4}
        rest_level = price_values.get(restaurant_price, 2)
        budget_level = price_values.get(user_budget, 2)
        
        if rest_level == budget_level:
            return 1.0  # Perfect match
        elif abs(rest_level - budget_level) == 1:
            return 0.7  # Close match
        else:
            return 0.3  # Poor match
    
    def _calculate_occasion_score(self, restaurant: Dict, occasion: str) -> float:
        """Calculate how well restaurant matches the occasion"""
        features = restaurant.get('features', [])
        
        occasion_matches = {
            'romantic': ['wine_pairing', 'romantic_atmosphere', 'fine_dining', 'dress_code'],
            'business': ['upscale_casual', 'fine_dining', 'wine_list', 'valet_parking'],
            'family': ['family_style', 'family_portions', 'casual_dining', 'quick_service'],
            'celebration': ['wine_bar', 'live_music', 'chef_specials', 'fine_dining'],
            'casual': ['casual_dining', 'takeout', 'sports_bar', 'outdoor_seating']
        }
        
        relevant_features = occasion_matches.get(occasion, [])
        matches = len([f for f in features if f in relevant_features])
        
        return min(matches * 0.25, 1.0)
    
    def _calculate_location_score(self, restaurant: Dict, preferences: Dict) -> float:
        """Calculate location convenience score"""
        user_location = preferences['location'].lower()
        restaurant_location = restaurant['location'].lower()
        
        if user_location == 'city-wide':
            return 0.5
        elif user_location in restaurant_location or restaurant_location in user_location:
            return 1.0
        else:
            return 0.3
    
    def _generate_intelligent_recommendations(self, scored_restaurants: List[Dict], preferences: Dict) -> List[Dict]:
        """Generate intelligent recommendations with reasoning"""
        recommendations = []
        
        for i, restaurant in enumerate(scored_restaurants[:3]):  # Top 3
            reasoning = self._generate_dynamic_reasoning(restaurant, preferences)
            
            rec = {
                'rank': i + 1,
                'name': restaurant['name'],
                'cuisine': restaurant['cuisine'],
                'rating': restaurant['rating'],
                'price': restaurant['price'],
                'location': restaurant['location'],
                'features': restaurant.get('features', []),
                'estimated_wait': restaurant.get('estimated_wait', 'Unknown'),
                'hours': restaurant.get('hours', 'Call for hours'),
                'phone': restaurant.get('phone', 'No phone available'),
                'analysis_score': restaurant['analysis_score'],
                'reasoning': reasoning,
                'score_breakdown': restaurant.get('score_breakdown', {})
            }
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_dynamic_reasoning(self, restaurant: Dict, preferences: Dict) -> str:
        """Generate dynamic reasoning based on analysis"""
        reasons = []
        
        # Rating-based reasoning
        rating = restaurant['rating']
        if rating >= 4.5:
            reasons.append(f"Excellent customer rating ({rating}/5.0)")
        elif rating >= 4.0:
            reasons.append(f"Very good rating ({rating}/5.0)")
        else:
            reasons.append(f"Decent rating ({rating}/5.0)")
        
        # Price reasoning
        if preferences['budget'] != 'any':
            if restaurant['price'] == preferences['budget']:
                reasons.append("Perfect price match")
            else:
                reasons.append("Within budget range")
        
        # Occasion reasoning
        occasion = preferences['occasion']
        features = restaurant.get('features', [])
        
        if occasion == 'romantic' and any(f in features for f in ['romantic_atmosphere', 'wine_pairing']):
            reasons.append("Perfect for romantic dining")
        elif occasion == 'business' and any(f in features for f in ['upscale_casual', 'fine_dining']):
            reasons.append("Ideal for business meetings")
        elif occasion == 'family' and 'family_style' in features:
            reasons.append("Great for family dining")
        
        # Feature highlights
        special_features = [f for f in features if f in ['wine_bar', 'sushi_bar', 'outdoor_seating']]
        if special_features:
            reasons.append(f"Special features: {', '.join(special_features[:2])}")
        
        return '. '.join(reasons) if reasons else "Good overall match for your preferences"
    
    def _calculate_dynamic_confidence(self, recommendations: List[Dict], preferences: Dict) -> float:
        """Calculate dynamic confidence based on analysis quality"""
        if not recommendations:
            return 0.1
        
        # Base confidence from top recommendation score
        top_score = recommendations[0]['analysis_score']
        
        # Preference specificity bonus
        specificity = 0.0
        if preferences['cuisine'] != 'any':
            specificity += 0.1
        if preferences['budget'] != 'any':
            specificity += 0.1
        if preferences['location'] != 'city-wide':
            specificity += 0.1
        
        # Recommendation spread (more options = higher confidence)
        spread_bonus = min(len(recommendations) * 0.05, 0.15)
        
        total_confidence = top_score * 0.7 + specificity + spread_bonus
        
        return min(total_confidence, 1.0)

class InteractiveCharlie:
    """Enhanced Charlie with dynamic decision making and user interaction"""
    
    def __init__(self):
        self.decision_history = []
    
    def make_interactive_decision(self, bob_analysis: Dict) -> Dict:
        """Make interactive decision with user feedback"""
        
        print("👑 CHARLIE: I've received Bob's analysis. Let me make the final decision...")
        print("🔄 Evaluating all options...\n")
        
        recommendations = bob_analysis['recommendations']
        
        if not recommendations:
            print("❌ Charlie: No suitable recommendations available")
            return self._create_no_match_decision(bob_analysis['task_id'])
        
        # Show analysis to user
        self._display_analysis_summary(bob_analysis)
        
        # Present options to user
        print("🏆 TOP RECOMMENDATIONS:")
        print("-" * 50)
        
        for i, rec in enumerate(recommendations):
            print(f"{rec['rank']}. {rec['name']} ({rec['cuisine']})")
            print(f"   ⭐ {rec['rating']}/5.0  💰 {rec['price']}  📍 {rec['location']}")
            print(f"   ⏰ Wait: ~{rec['estimated_wait']} min  📞 {rec['phone']}")
            print(f"   🎯 Match Score: {rec['analysis_score']:.2f}")
            print(f"   💭 Why: {rec['reasoning']}")
            if rec.get('hours'):
                print(f"   🕐 Hours: {rec['hours']}")
            print()
        
        # Get user preference
        choice = self._get_user_choice(recommendations)
        
        if choice == 'auto':
            # Charlie makes automatic decision
            final_choice = self._make_automatic_decision(recommendations)
            print(f"👑 Charlie: I recommend {final_choice['name']}!")
        else:
            # User selected specific option
            final_choice = recommendations[choice - 1]
            print(f"👑 Charlie: Excellent choice - {final_choice['name']}!")
        
        # Generate final decision
        decision_confidence = self._calculate_decision_confidence(final_choice, recommendations)
        reasoning = self._generate_final_reasoning(final_choice, recommendations)
        
        decision = {
            'task_id': bob_analysis['task_id'],
            'final_choice': final_choice,
            'reasoning': reasoning,
            'confidence': decision_confidence,
            'user_interactive': True,
            'alternatives': [r for r in recommendations if r != final_choice]
        }
        
        self._display_final_decision(decision)
        return decision
    
    def _display_analysis_summary(self, analysis: Dict):
        """Display Bob's analysis summary"""
        print("📊 ANALYSIS SUMMARY:")
        print("-" * 30)
        print(f"📈 Restaurants analyzed: {analysis.get('total_analyzed', 0)}")
        print(f"✅ Matching criteria: {analysis.get('filtered_count', 0)}")
        print(f"📊 Analysis confidence: {analysis['confidence']:.2f}")
        print(f"💡 {analysis['analysis_summary']}")
        print()
    
    def _get_user_choice(self, recommendations: List[Dict]) -> str:
        """Get user's choice from recommendations"""
        while True:
            print("🎯 DECISION TIME:")
            print("Enter the number of your preferred restaurant (1-3)")
            print("Or press Enter to let me choose the best option for you")
            
            choice = input("Your choice: ").strip()
            
            if not choice:
                return 'auto'
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(recommendations):
                    return choice_num
                else:
                    print(f"❌ Please enter a number between 1 and {len(recommendations)}")
            except ValueError:
                print("❌ Please enter a valid number or press Enter")
    
    def _make_automatic_decision(self, recommendations: List[Dict]) -> Dict:
        """Charlie's automatic decision logic"""
        # Use the top recommendation with highest analysis score
        return recommendations[0]
    
    def _calculate_decision_confidence(self, choice: Dict, all_recommendations: List[Dict]) -> float:
        """Calculate confidence in the final decision"""
        base_confidence = choice['analysis_score']
        
        # Higher confidence if choice is clear leader
        if len(all_recommendations) > 1:
            score_gap = choice['analysis_score'] - all_recommendations[1]['analysis_score']
            confidence_bonus = min(score_gap * 2, 0.2)
        else:
            confidence_bonus = 0.1
        
        return min(base_confidence + confidence_bonus, 1.0)
    
    def _generate_final_reasoning(self, choice: Dict, all_recommendations: List[Dict]) -> str:
        """Generate final decision reasoning"""
        reasons = [
            f"Selected {choice['name']} with {choice['analysis_score']:.2f} match score",
            f"Excellent rating of {choice['rating']}/5.0 stars",
            choice['reasoning']
        ]
        
        if len(all_recommendations) > 1:
            reasons.append(f"Outperformed {len(all_recommendations)-1} other quality options")
        
        return '. '.join(reasons)
    
    def _display_final_decision(self, decision: Dict):
        """Display the final decision beautifully"""
        choice = decision['final_choice']
        
        print("\n" + "="*60)
        print("🎉 FINAL RECOMMENDATION")
        print("="*60)
        print(f"🏆 Restaurant: {choice['name']}")
        print(f"🍽️ Cuisine: {choice['cuisine']}")
        print(f"⭐ Rating: {choice['rating']}/5.0")
        print(f"💰 Price: {choice['price']}")
        print(f"📍 Location: {choice['location']}")
        print(f"⏰ Estimated Wait: {choice.get('estimated_wait', 'Unknown')} minutes")
        print(f"📞 Phone: {choice.get('phone', 'N/A')}")
        
        if choice.get('hours'):
            print(f"🕐 Hours: {choice['hours']}")
        
        if choice.get('features'):
            print(f"✨ Features: {', '.join(choice['features'][:4])}")
        
        print(f"\n📊 Decision Confidence: {decision['confidence']:.2f}")
        print(f"💭 Reasoning: {decision['reasoning']}")
        
        print("\n✅ Enjoy your dining experience!")
        print("="*60)
    
    def _create_no_match_decision(self, task_id: str) -> Dict:
        """Create decision when no matches found"""
        return {
            'task_id': task_id,
            'final_choice': {'name': 'No suitable match found'},
            'reasoning': 'Unable to find restaurants matching all criteria',
            'confidence': 0.1,
            'user_interactive': True,
            'alternatives': []
        }

def run_dynamic_interactive_system():
    """Run the complete dynamic interactive system"""
    
    print("🌟" + "="*58 + "🌟")
    print("🎯 DYNAMIC INTERACTIVE 3-AGENT RESTAURANT SYSTEM 🎯")
    print("🌟" + "="*58 + "🌟")
    print()
    print("🤖 Your AI Team:")
    print("🔍 Alice - Intelligent Data Collector")
    print("🧠 Bob - Dynamic Analysis Engine") 
    print("👑 Charlie - Interactive Decision Coordinator")
    print()
    
    # Initialize agents
    alice = InteractiveAlice()
    bob = DynamicBob()
    charlie = InteractiveCharlie()
    
    try:
        while True:
            print("🚀 Starting new restaurant recommendation session...")
            print("-" * 60)
            
            # Step 1: Alice collects user input
            alice_data = alice.collect_user_input()
            
            # Step 2: Bob performs dynamic analysis
            bob_analysis = bob.analyze_restaurants(alice_data)
            
            # Step 3: Charlie makes interactive decision
            final_decision = charlie.make_interactive_decision(bob_analysis)
            
            # Ask if user wants another recommendation
            print("\n" + "="*60)
            another = input("🔄 Would you like another recommendation? (y/n): ").lower().strip()
            
            if another not in ['y', 'yes']:
                break
            
            print("\n" + "🌟"*60)
    
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using the Dynamic Interactive Restaurant System!")
        print("🎊 Hope you found the perfect dining spot!")

if __name__ == "__main__":
    print("🔥 DYNAMIC INTERACTIVE MODE ACTIVATED! 🔥")
    print("This system uses:")
    print("✅ Real user input")
    print("✅ Dynamic data generation") 
    print("✅ Interactive decision making")
    print("✅ Real-time preference matching")
    print()
    
    run_dynamic_interactive_system()
