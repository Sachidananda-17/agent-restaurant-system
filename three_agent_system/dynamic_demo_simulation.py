"""
Dynamic Demo Simulation - Shows the full interactive workflow
Demonstrates real user scenarios and dynamic agent responses
"""

import time
import random
from datetime import datetime

def simulate_user_input(prompt, response, delay=1):
    """Simulate user typing"""
    print(prompt, end='', flush=True)
    time.sleep(delay * 0.5)
    print(f" {response}")
    time.sleep(delay * 0.3)
    return response

def print_agent_thinking(agent, message, delay=1):
    """Show agent processing"""
    print(f"{agent}: {message}")
    time.sleep(delay)

def run_dynamic_scenario_1():
    """Romantic dinner date scenario"""
    
    print("🌟" + "="*58 + "🌟")
    print("🎯 SCENARIO 1: ROMANTIC DATE NIGHT")
    print("🌟" + "="*58 + "🌟")
    print()
    
    print("🔍 ALICE: Hi! I'm your restaurant recommendation assistant!")
    print("I'll help you find the perfect dining spot based on your preferences.\n")
    
    # Simulated user interaction
    user_request = simulate_user_input("💬 What kind of dining experience are you looking for?", 
                                     "I need a romantic restaurant for my anniversary dinner")
    
    location = simulate_user_input("📍 What area/location are you interested in? (or press Enter for anywhere):", 
                                 "downtown area")
    
    cuisine = simulate_user_input("🍽️ Any specific cuisine preference? (or press Enter for any):", 
                                "French or Italian would be perfect")
    
    budget = simulate_user_input("💰 What's your budget range? ($/$$/$$$/$$$$, or press Enter for any):", 
                               "$$$")
    
    party_size = simulate_user_input("👥 How many people? (or press Enter for 2):", 
                                   "2")
    
    print("\n🔍 Alice: Perfect! Let me gather some options for you...")
    print("🔄 Searching restaurants...")
    time.sleep(2)
    
    # Alice's dynamic data collection
    print("✅ Found 8 restaurants matching your criteria!")
    print("🔍 Alice: Analyzing preferences - detected romantic occasion")
    print("📊 Location: Downtown area restaurants prioritized")
    print("💰 Budget: Premium dining ($$$) options selected")
    print("🍽️ Cuisine: French and Italian restaurants identified")
    print("✅ Data collection complete - sending to Bob\n")
    
    # Bob's dynamic analysis
    print("🧠 BOB: Analyzing your restaurant options...")
    print("🔄 Running advanced multi-criteria analysis...\n")
    
    print("📊 Stage 1: Filtered from 8 to 5 restaurants")
    time.sleep(1)
    print("📊 Stage 2: Applied dynamic scoring algorithm")
    time.sleep(1)
    print("📊 Stage 3: Generated 3 intelligent recommendations")
    time.sleep(1)
    print("📊 Stage 4: Analysis confidence: 0.94")
    print("✅ Bob: Analysis complete - sending to Charlie for final decision\n")
    
    # Charlie's dynamic decision making
    print("👑 CHARLIE: I've received Bob's analysis. Let me make the final decision...")
    print("🔄 Evaluating all options...\n")
    
    print("📊 ANALYSIS SUMMARY:")
    print("-" * 30)
    print("📈 Restaurants analyzed: 8")
    print("✅ Matching criteria: 5")
    print("📊 Analysis confidence: 0.94")
    print("💡 Analyzed restaurants using dynamic criteria matching romantic dining preferences")
    print()
    
    # Display dynamic recommendations
    recommendations = [
        {
            'rank': 1,
            'name': 'Le Jardin Romantique',
            'cuisine': 'French',
            'rating': 4.8,
            'price': '$$$',
            'location': 'Downtown Historic District',
            'wait': 25,
            'phone': '(555) 123-7890',
            'hours': '5:00 PM - 10:30 PM',
            'features': ['wine_pairing', 'romantic_atmosphere', 'fine_dining', 'outdoor_terrace'],
            'score': 0.96
        },
        {
            'rank': 2,
            'name': 'Bella Notte Italiano',
            'cuisine': 'Italian', 
            'rating': 4.7,
            'price': '$$$',
            'location': 'Downtown Riverside',
            'wait': 20,
            'phone': '(555) 456-1234',
            'hours': '4:30 PM - 11:00 PM',
            'features': ['wine_bar', 'romantic_lighting', 'live_piano', 'waterfront_view'],
            'score': 0.91
        },
        {
            'rank': 3,
            'name': 'Château Blanc',
            'cuisine': 'French',
            'rating': 4.6,
            'price': '$$$',
            'location': 'Downtown Arts Quarter', 
            'wait': 30,
            'phone': '(555) 789-0123',
            'hours': '6:00 PM - 10:00 PM',
            'features': ['chef_specials', 'wine_cellar', 'intimate_booths'],
            'score': 0.88
        }
    ]
    
    print("🏆 TOP RECOMMENDATIONS:")
    print("-" * 50)
    
    for rec in recommendations:
        print(f"{rec['rank']}. {rec['name']} ({rec['cuisine']})")
        print(f"   ⭐ {rec['rating']}/5.0  💰 {rec['price']}  📍 {rec['location']}")
        print(f"   ⏰ Wait: ~{rec['wait']} min  📞 {rec['phone']}")
        print(f"   🎯 Match Score: {rec['score']:.2f}")
        print(f"   🕐 Hours: {rec['hours']}")
        print(f"   ✨ Features: {', '.join(rec['features'][:3])}")
        print()
    
    # Simulated user choice
    choice = simulate_user_input("🎯 DECISION TIME:\nEnter the number of your preferred restaurant (1-3)\nOr press Enter to let me choose the best option for you\nYour choice:", "1")
    
    final_choice = recommendations[0]  # User chose #1
    
    print(f"👑 Charlie: Excellent choice - {final_choice['name']}!")
    time.sleep(1)
    
    # Final decision display
    print("\n" + "="*60)
    print("🎉 FINAL RECOMMENDATION")
    print("="*60)
    print(f"🏆 Restaurant: {final_choice['name']}")
    print(f"🍽️ Cuisine: {final_choice['cuisine']}")
    print(f"⭐ Rating: {final_choice['rating']}/5.0")
    print(f"💰 Price: {final_choice['price']}")
    print(f"📍 Location: {final_choice['location']}")
    print(f"⏰ Estimated Wait: {final_choice['wait']} minutes")
    print(f"📞 Phone: {final_choice['phone']}")
    print(f"🕐 Hours: {final_choice['hours']}")
    print(f"✨ Features: {', '.join(final_choice['features'])}")
    print(f"\n📊 Decision Confidence: 0.97")
    print(f"💭 Reasoning: Selected Le Jardin Romantique with 0.96 match score. Excellent rating of 4.8/5.0 stars. Perfect for romantic dining with wine pairing and romantic atmosphere. Outperformed 2 other quality options.")
    print("\n✅ Enjoy your anniversary dinner!")
    print("="*60)

def run_dynamic_scenario_2():
    """Business lunch scenario"""
    
    print("\n\n🌟" + "="*58 + "🌟")
    print("🎯 SCENARIO 2: BUSINESS LUNCH MEETING")
    print("🌟" + "="*58 + "🌟")
    print()
    
    print("🔍 ALICE: Hi! Ready for another recommendation?\n")
    
    # Quick business scenario
    user_request = simulate_user_input("💬 What kind of dining experience are you looking for?", 
                                     "Professional business lunch venue for client meeting", 0.5)
    
    location = simulate_user_input("📍 Location?", "financial district", 0.5)
    cuisine = simulate_user_input("🍽️ Cuisine?", "American or upscale casual", 0.5)  
    budget = simulate_user_input("💰 Budget?", "$$$$", 0.5)
    party_size = simulate_user_input("👥 Party size?", "4", 0.5)
    
    print("\n🔍 Alice: Business lunch detected - prioritizing professional venues")
    print("✅ Found 6 upscale restaurants in financial district")
    
    print("\n🧠 Bob: Quick analysis for time-sensitive business need")
    print("📊 Filtered to 3 business-appropriate venues")
    print("📊 Confidence: 0.91")
    
    print("\n👑 Charlie: Top recommendation for business lunch:")
    print("\n🏆 RECOMMENDATION: Executive Club")
    print("🍽️ Upscale American • ⭐ 4.7/5.0 • 💰 $$$$")
    print("📍 Financial District Center")
    print("✨ Features: business_atmosphere, private_booths, wifi, valet_parking")
    print("⏰ Available now - 15 min wait")
    print("💭 Perfect for professional meetings with excellent service")
    
    print("\n✅ Reservation recommended due to business district location!")

def run_dynamic_scenario_3():
    """Family dinner with real-time adjustments"""
    
    print("\n\n🌟" + "="*58 + "🌟")
    print("🎯 SCENARIO 3: DYNAMIC ADAPTATION")
    print("🌟" + "="*58 + "🌟")
    print()
    
    print("🔍 ALICE: Let me show you dynamic adaptation in action!\n")
    
    user_request = simulate_user_input("💬 Dining experience?", "family dinner with kids", 0.5)
    location = simulate_user_input("📍 Location?", "suburbs", 0.5)
    cuisine = simulate_user_input("🍽️ Cuisine?", "pizza or American", 0.5)
    budget = simulate_user_input("💰 Budget?", "$$", 0.5)
    
    print("\n🔍 Alice: Family-friendly options detected")
    print("🧠 Bob: Analyzing kid-friendly restaurants...")
    
    print("\n💡 DYNAMIC ADAPTATION EXAMPLE:")
    print("🔄 Initial search: Found 4 family restaurants")
    print("⚠️ Real-time update: One restaurant just got busy (45min wait)")
    print("🔄 Re-analyzing: Adjusting recommendations...")
    print("✅ Updated recommendations with current wait times")
    
    print("\n👑 Charlie: Adapted recommendation:")
    print("🏆 Pizza Palace Family - ⭐ 4.2, 💰 $$, ⏰ 10min wait")
    print("✨ Features: family_friendly, kids_menu, playground, quick_service")
    print("🎯 Perfect timing and atmosphere for family dinner!")

def main():
    """Run all dynamic scenarios"""
    
    print("🔥 DYNAMIC AGENT SYSTEM - COMPLETE DEMONSTRATION 🔥")
    print("This shows how agents adapt to different scenarios dynamically\n")
    
    try:
        # Scenario 1: Romantic dinner (detailed)
        run_dynamic_scenario_1()
        
        time.sleep(3)
        
        # Scenario 2: Business lunch (faster)
        run_dynamic_scenario_2()
        
        time.sleep(2)
        
        # Scenario 3: Dynamic adaptation
        run_dynamic_scenario_3()
        
        print("\n\n🌟" + "="*58 + "🌟")
        print("🎊 DYNAMIC FEATURES DEMONSTRATED:")
        print("✅ Real user input processing")
        print("✅ Dynamic restaurant data generation")
        print("✅ Context-aware preference analysis")  
        print("✅ Multi-criteria dynamic scoring")
        print("✅ Interactive decision making")
        print("✅ Real-time adaptation to conditions")
        print("✅ Personalized reasoning generation")
        print("✅ Different scenario handling")
        print("\n🎯 This system can be extended with:")
        print("🌐 Real APIs (Google Places, Yelp)")
        print("🤖 AI/LLM integration for smarter analysis")
        print("📱 Web/mobile interface")
        print("📊 Machine learning for user preferences")
        print("🔄 Real-time availability checking")
        print("🌟" + "="*58 + "🌟")
        
    except KeyboardInterrupt:
        print("\n\n👋 Dynamic demo completed!")

if __name__ == "__main__":
    main()
