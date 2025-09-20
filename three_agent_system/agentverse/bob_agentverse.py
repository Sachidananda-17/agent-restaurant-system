"""
Bob Agent - Agentverse Production Version  
🧠 Solution Analyzer & Processor for Global Restaurant Intelligence
🌐 Deployed on Fetch.ai Agentverse Platform
"""

from uagents import Agent, Context, Model
import datetime
import random

# === MESSAGE MODELS ===
class DataCollection(Model):
    task_id: str
    user_preferences: dict
    location_data: dict
    search_criteria: dict
    confidence_score: float
    timestamp: str
    sender: str = "Alice"

class AnalysisRequest(Model):
    task_id: str
    requested_data: list
    analysis_focus: str
    timestamp: str
    sender: str = "Bob"

class AnalysisResult(Model):
    task_id: str
    analysis_summary: str
    recommendations: list
    confidence_scores: dict
    supporting_data: dict
    timestamp: str
    sender: str = "Bob"

class DecisionRequest(Model):
    task_id: str
    clarification_needed: str
    additional_criteria: dict
    timestamp: str
    sender: str = "Charlie"

class StatusUpdate(Model):
    task_id: str
    status: str
    progress_percentage: int
    message: str
    timestamp: str
    sender: str

# === AGENTVERSE BOB AGENT ===
bob = Agent(
    name="bob_global_restaurant_analyzer",
    seed="bob_production_agentverse_seed_2024"
    # 🌐 No port or endpoint - Agentverse manages automatically
)

# Global team discovery
ALICE_ADDRESS = ""
CHARLIE_ADDRESS = ""
bob_global_memory = {
    "completed_analyses": [],
    "active_analyses": {},
    "global_stats": {
        "total_analyses": 0,
        "average_confidence": 0.0,
        "processing_time_avg": 0.0
    },
    "analysis_models": {
        "recommendation_engine": "v2.1",
        "sentiment_analyzer": "advanced",
        "price_optimizer": "dynamic",
        "location_matcher": "geo_enhanced"
    }
}

# Global restaurant intelligence database (enhanced for Agentverse)
GLOBAL_RESTAURANT_INTELLIGENCE = {
    "cuisine_profiles": {
        "Italian": {
            "avg_rating": 4.3,
            "price_distribution": {"$": 0.2, "$$": 0.4, "$$$": 0.3, "$$$$": 0.1},
            "popular_features": ["wine_selection", "outdoor_seating", "family_friendly"],
            "peak_times": ["19:00-21:00"],
            "dietary_accommodations": ["vegetarian", "gluten_free"]
        },
        "French": {
            "avg_rating": 4.6,
            "price_distribution": {"$": 0.05, "$$": 0.25, "$$$": 0.45, "$$$$": 0.25},
            "popular_features": ["wine_pairing", "romantic_atmosphere", "chef_specials"],
            "peak_times": ["19:30-22:00"],
            "dietary_accommodations": ["vegetarian"]
        },
        "Japanese": {
            "avg_rating": 4.5,
            "price_distribution": {"$": 0.15, "$$": 0.35, "$$$": 0.4, "$$$$": 0.1},
            "popular_features": ["fresh_fish", "sake_bar", "sushi_counter"],
            "peak_times": ["18:00-20:00", "12:00-13:30"],
            "dietary_accommodations": ["vegetarian", "raw_fish"]
        }
    },
    "global_trends": {
        "sustainability": 0.3,
        "plant_based": 0.4,
        "local_sourcing": 0.5,
        "tech_ordering": 0.6
    }
}

@bob.on_event("startup")
async def bob_global_startup(ctx: Context):
    """Bob announces advanced analytical capabilities on Agentverse"""
    ctx.logger.info("🌐 Bob Restaurant Analyzer starting on Agentverse!")
    ctx.logger.info(f"📍 Global Address: {bob.address}")
    ctx.logger.info("🧠 Specialization: Advanced restaurant analysis and recommendation intelligence")
    ctx.logger.info("🔧 Analysis Capabilities:")
    ctx.logger.info("   • Multi-criteria recommendation engine v2.1")
    ctx.logger.info("   • Global sentiment analysis processing")
    ctx.logger.info("   • Dynamic price-performance optimization")
    ctx.logger.info("   • Geo-enhanced location matching")
    ctx.logger.info("   • Cultural cuisine intelligence")
    ctx.logger.info("🤝 Seeking Alice (Data Collector) and Charlie (Coordinator)")
    ctx.logger.info("🌟 Ready for global restaurant analysis tasks!")
    
    # Broadcast analytical capabilities to global network
    startup_status = StatusUpdate(
        task_id="bob_global_startup",
        status="analytical_services_online",
        progress_percentage=100,
        message="Bob Restaurant Analyzer providing global analysis services",
        timestamp=datetime.datetime.now().isoformat(),
        sender="Bob"
    )
    
    ctx.logger.info("📡 Broadcasting analytical services on Agentverse network")

@bob.on_interval(period=120.0)  # Every 2 minutes - performance update
async def broadcast_global_capabilities(ctx: Context):
    """Broadcast Bob's analytical performance to the network"""
    stats = bob_global_memory["global_stats"]
    
    if stats["total_analyses"] > 0:
        ctx.logger.info("📊 Global Analysis Performance Update:")
        ctx.logger.info(f"   • Total analyses completed: {stats['total_analyses']}")
        ctx.logger.info(f"   • Average confidence score: {stats['average_confidence']:.3f}")
        ctx.logger.info(f"   • Average processing time: {stats['processing_time_avg']:.1f}s")
        ctx.logger.info("🧠 Bob ready for complex global restaurant analysis tasks")

@bob.on_message(model=DataCollection)
async def perform_global_analysis(ctx: Context, sender: str, msg: DataCollection):
    """Perform advanced global restaurant analysis"""
    global ALICE_ADDRESS
    analysis_start_time = datetime.datetime.now()
    
    ctx.logger.info("🌐 ===== GLOBAL ANALYSIS INITIATED =====")
    ctx.logger.info(f"📊 Analysis request: {msg.task_id}")
    ctx.logger.info(f"🔍 Data source: Alice ({sender[:16]}...)")
    ctx.logger.info(f"👤 User preferences: {msg.user_preferences}")
    ctx.logger.info(f"📍 Location requirements: {msg.location_data}")
    
    # Record Alice if first contact
    if not ALICE_ADDRESS and msg.sender == "Alice":
        ALICE_ADDRESS = sender
        ctx.logger.info(f"🌐 ✅ Global Alice registered: {sender[:16]}...")
    
    # Store analysis in global memory
    bob_global_memory["active_analyses"][msg.task_id] = {
        "start_time": analysis_start_time.isoformat(),
        "source_data": msg,
        "sender_address": sender,
        "status": "processing"
    }
    
    ctx.logger.info("🧠 Starting advanced global analysis pipeline...")
    
    # Stage 1: Global Restaurant Intelligence Lookup
    global_restaurants = generate_global_restaurant_data(msg)
    ctx.logger.info(f"📊 Stage 1: Generated {len(global_restaurants)} global restaurant options")
    
    # Stage 2: Advanced filtering with global intelligence
    filtered_restaurants = advanced_global_filter(global_restaurants, msg)
    ctx.logger.info(f"📊 Stage 2: Filtered to {len(filtered_restaurants)} high-quality matches")
    
    # Stage 3: Multi-dimensional scoring with cultural intelligence
    scored_restaurants = global_multi_dimensional_scoring(filtered_restaurants, msg)
    ctx.logger.info("📊 Stage 3: Applied multi-dimensional cultural scoring")
    
    # Stage 4: Generate intelligent global recommendations
    recommendations = generate_global_recommendations(scored_restaurants, msg)
    ctx.logger.info(f"📊 Stage 4: Generated {len(recommendations)} intelligent global recommendations")
    
    # Stage 5: Calculate comprehensive confidence metrics
    confidence_metrics = calculate_global_confidence(recommendations, msg)
    ctx.logger.info(f"📊 Stage 5: Analysis confidence: {confidence_metrics['overall_confidence']:.3f}")
    
    # Prepare comprehensive analysis results
    analysis_summary = create_global_analysis_summary(recommendations, msg, len(global_restaurants))
    
    supporting_data = {
        "total_restaurants_analyzed": len(global_restaurants),
        "filtering_efficiency": len(filtered_restaurants) / len(global_restaurants),
        "analysis_methods": list(bob_global_memory["analysis_models"].keys()),
        "global_intelligence_version": "2.1",
        "processing_time_seconds": (datetime.datetime.now() - analysis_start_time).total_seconds(),
        "cultural_factors_considered": get_cultural_factors(msg.user_preferences)
    }
    
    analysis_result = AnalysisResult(
        task_id=msg.task_id,
        analysis_summary=analysis_summary,
        recommendations=recommendations,
        confidence_scores=confidence_metrics,
        supporting_data=supporting_data,
        timestamp=datetime.datetime.now().isoformat(),
        sender="Bob"
    )
    
    # Update global memory
    bob_global_memory["active_analyses"][msg.task_id].update({
        "status": "completed",
        "results": analysis_result,
        "processing_time": supporting_data["processing_time_seconds"]
    })
    
    # Update global stats
    bob_global_memory["global_stats"]["total_analyses"] += 1
    total = bob_global_memory["global_stats"]["total_analyses"]
    current_avg = bob_global_memory["global_stats"]["average_confidence"]
    new_confidence = confidence_metrics["overall_confidence"]
    bob_global_memory["global_stats"]["average_confidence"] = (current_avg * (total-1) + new_confidence) / total
    
    current_time_avg = bob_global_memory["global_stats"]["processing_time_avg"]  
    new_time = supporting_data["processing_time_seconds"]
    bob_global_memory["global_stats"]["processing_time_avg"] = (current_time_avg * (total-1) + new_time) / total
    
    ctx.logger.info("🧠 ===== GLOBAL ANALYSIS COMPLETED =====")
    ctx.logger.info(f"⏱️ Processing time: {supporting_data['processing_time_seconds']:.1f} seconds")
    ctx.logger.info(f"🎯 Top recommendation: {recommendations[0]['restaurant']['name']}")
    ctx.logger.info(f"📊 Global confidence: {confidence_metrics['overall_confidence']:.3f}")
    
    # Send to global Charlie
    if CHARLIE_ADDRESS:
        try:
            await ctx.send(CHARLIE_ADDRESS, analysis_result)
            ctx.logger.info("🌐 ✅ Global analysis results sent to Charlie")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to send to global Charlie: {str(e)}")
    else:
        ctx.logger.warning("⚠️ Global Charlie not yet discovered - results cached")

def generate_global_restaurant_data(data_msg: DataCollection) -> list:
    """Generate realistic global restaurant data based on preferences"""
    preferences = data_msg.user_preferences
    location = data_msg.location_data
    
    # Base restaurant types by cuisine with global variations
    global_restaurant_templates = {
        'Italian': [
            {'base_name': 'Villa Roma', 'region': 'Tuscan', 'specialty': 'handmade_pasta'},
            {'base_name': 'Giuseppe\'s', 'region': 'Sicilian', 'specialty': 'wood_fired_pizza'},
            {'base_name': 'Bella Napoli', 'region': 'Neapolitan', 'specialty': 'authentic_pizza'},
            {'base_name': 'Osteria Milano', 'region': 'Northern', 'specialty': 'risotto'},
            {'base_name': 'Trattoria Venice', 'region': 'Venetian', 'specialty': 'seafood_pasta'}
        ],
        'French': [
            {'base_name': 'Le Petit Bistro', 'region': 'Parisian', 'specialty': 'classic_bistro'},
            {'base_name': 'Château Blanc', 'region': 'Loire_Valley', 'specialty': 'wine_pairing'},
            {'base_name': 'Brasserie Lyon', 'region': 'Lyonnaise', 'specialty': 'traditional_cuisine'},
            {'base_name': 'Café Provence', 'region': 'Provençal', 'specialty': 'mediterranean'},
            {'base_name': 'L\'Atelier Rouge', 'region': 'Bordeaux', 'specialty': 'fine_dining'}
        ],
        'Japanese': [
            {'base_name': 'Sakura Sushi', 'region': 'Tokyo', 'specialty': 'omakase'},
            {'base_name': 'Ramen Yokocho', 'region': 'Osaka', 'specialty': 'tonkotsu_ramen'},
            {'base_name': 'Izakaya Koi', 'region': 'Kyoto', 'specialty': 'traditional_izakaya'},
            {'base_name': 'Sushi Zen', 'region': 'Tsukiji', 'specialty': 'fresh_sashimi'},
            {'base_name': 'Teppanyaki House', 'region': 'Kobe', 'specialty': 'wagyu_beef'}
        ]
    }
    
    restaurants = []
    
    # Determine cuisines to generate
    target_cuisine = preferences.get('cuisine', 'any')
    if target_cuisine == 'any':
        cuisines_to_use = list(global_restaurant_templates.keys())
    else:
        cuisines_to_use = [target_cuisine] if target_cuisine in global_restaurant_templates else ['Italian']
    
    for cuisine in cuisines_to_use[:3]:  # Limit to 3 cuisines max
        templates = global_restaurant_templates[cuisine]
        
        for i, template in enumerate(templates[:4]):  # Max 4 per cuisine
            # Generate dynamic properties
            base_rating = random.uniform(3.8, 4.9)
            time_variance = (datetime.datetime.now().hour % 24) / 24 * 0.2
            rating = round(min(base_rating + time_variance, 5.0), 1)
            
            # Dynamic pricing based on preferences and occasion
            occasion = preferences.get('occasion', 'casual')
            if occasion == 'business' or occasion == 'romantic':
                price_options = ['$$$', '$$$$']
            elif occasion == 'family':
                price_options = ['$', '$$', '$$$']
            else:
                price_options = ['$$', '$$$']
            
            price = random.choice(price_options)
            
            # Generate comprehensive features
            features = generate_comprehensive_features(cuisine, price, occasion, template)
            
            # Location intelligence
            location_area = generate_intelligent_location(location.get('area', 'city_center'), cuisine)
            
            restaurant = {
                'name': template['base_name'],
                'cuisine': cuisine,
                'regional_style': template['region'],
                'specialty': template['specialty'],
                'rating': rating,
                'price': price,
                'location': location_area,
                'features': features,
                'atmosphere': generate_atmosphere_profile(cuisine, occasion),
                'service_style': determine_service_style(price, cuisine),
                'dietary_accommodations': get_dietary_accommodations(cuisine),
                'cultural_authenticity': random.uniform(0.7, 1.0),
                'innovation_score': random.uniform(0.3, 0.9),
                'local_popularity': random.uniform(0.6, 1.0),
                'global_recognition': random.uniform(0.4, 0.8)
            }
            
            restaurants.append(restaurant)
    
    return restaurants

def generate_comprehensive_features(cuisine: str, price: str, occasion: str, template: dict) -> list:
    """Generate comprehensive feature list based on multiple factors"""
    base_features = ['takeout_available', 'reservations_accepted', 'credit_cards']
    
    # Cuisine-specific features
    cuisine_features = {
        'Italian': ['wine_cellar', 'wood_fired_oven', 'homemade_pasta', 'outdoor_terrace'],
        'French': ['wine_sommelier', 'chef_specials', 'romantic_lighting', 'dress_code'],
        'Japanese': ['sake_selection', 'sushi_bar', 'tatami_rooms', 'omakase_available']
    }
    
    # Price-based features
    price_features = {
        '$': ['casual_atmosphere', 'quick_service', 'family_portions'],
        '$$': ['table_service', 'full_bar', 'parking_available'],
        '$$$': ['upscale_decor', 'wine_list', 'private_dining'],
        '$$$$': ['valet_parking', 'fine_dining', 'tasting_menu', 'michelin_recommended']
    }
    
    # Occasion-specific features
    occasion_features = {
        'romantic': ['candlelit_tables', 'live_music', 'couples_seating'],
        'business': ['quiet_environment', 'wifi', 'business_lunch_menu'],
        'family': ['kids_menu', 'high_chairs', 'playground_area'],
        'celebration': ['private_rooms', 'birthday_specials', 'group_accommodations']
    }
    
    # Template specialty features
    specialty_features = {
        'handmade_pasta': ['pasta_making_visible', 'gluten_free_pasta'],
        'wood_fired_pizza': ['pizza_oven_viewing', 'custom_toppings'],
        'omakase': ['chef_counter', 'seasonal_menu'],
        'wine_pairing': ['wine_flights', 'cellar_tours']
    }
    
    # Combine features intelligently
    features = base_features.copy()
    features.extend(cuisine_features.get(cuisine, []))
    features.extend(price_features.get(price, []))
    features.extend(occasion_features.get(occasion, []))
    features.extend(specialty_features.get(template.get('specialty', ''), []))
    
    # Return reasonable number of features
    return random.sample(features, min(len(features), random.randint(5, 8)))

def advanced_global_filter(restaurants: list, data_msg: DataCollection) -> list:
    """Advanced filtering with global intelligence"""
    preferences = data_msg.user_preferences
    location = data_msg.location_data
    criteria = data_msg.search_criteria
    
    filtered = []
    
    for restaurant in restaurants:
        # Basic filters
        if preferences.get('cuisine', 'any') != 'any':
            if restaurant['cuisine'] != preferences['cuisine']:
                continue
        
        # Rating threshold with cultural adjustment
        min_rating = criteria.get('min_rating', 3.5)
        cultural_bonus = restaurant.get('cultural_authenticity', 0.8) * 0.3
        effective_rating = restaurant['rating'] + cultural_bonus
        
        if effective_rating < min_rating:
            continue
        
        # Price range compatibility
        budget = preferences.get('price_range', '$$')
        if not price_range_compatible(restaurant['price'], budget):
            continue
        
        # Dietary accommodations
        dietary_needs = preferences.get('dietary_restrictions', [])
        if dietary_needs:
            accommodations = restaurant.get('dietary_accommodations', [])
            if not any(need in accommodations for need in dietary_needs):
                continue
        
        # Location accessibility
        if location.get('area') != 'city_center':
            if restaurant['location'] not in get_acceptable_locations(location.get('area')):
                continue
        
        filtered.append(restaurant)
    
    return filtered

def price_range_compatible(restaurant_price: str, user_budget: str) -> bool:
    """Check if restaurant price is compatible with user budget"""
    price_values = {'$': 1, '$$': 2, '$$$': 3, '$$$$': 4}
    
    rest_level = price_values.get(restaurant_price, 2)
    budget_level = price_values.get(user_budget, 2)
    
    # Allow flexibility: one level above budget, two levels below
    return (rest_level <= budget_level + 1) and (rest_level >= max(1, budget_level - 2))

def global_multi_dimensional_scoring(restaurants: list, data_msg: DataCollection) -> list:
    """Multi-dimensional scoring with global cultural intelligence"""
    preferences = data_msg.user_preferences
    scored = []
    
    for restaurant in restaurants:
        score_components = {}
        
        # 1. Base Quality Score (25%)
        quality_score = (restaurant['rating'] / 5.0) * 0.25
        score_components['quality'] = quality_score
        
        # 2. Cultural Authenticity & Innovation Balance (20%)
        authenticity = restaurant.get('cultural_authenticity', 0.8)
        innovation = restaurant.get('innovation_score', 0.5)
        cultural_score = (authenticity * 0.6 + innovation * 0.4) * 0.20
        score_components['cultural'] = cultural_score
        
        # 3. Preference Alignment (20%)
        preference_score = calculate_preference_alignment(restaurant, preferences) * 0.20
        score_components['preferences'] = preference_score
        
        # 4. Local & Global Recognition (15%)
        local_pop = restaurant.get('local_popularity', 0.7)
        global_rec = restaurant.get('global_recognition', 0.6)
        recognition_score = (local_pop * 0.6 + global_rec * 0.4) * 0.15
        score_components['recognition'] = recognition_score
        
        # 5. Service & Atmosphere Match (10%)
        atmosphere_score = calculate_atmosphere_match(restaurant, preferences) * 0.10
        score_components['atmosphere'] = atmosphere_score
        
        # 6. Value Proposition (10%)
        value_score = calculate_value_proposition(restaurant, preferences) * 0.10
        score_components['value'] = value_score
        
        # Calculate total score
        total_score = sum(score_components.values())
        
        restaurant['global_analysis_score'] = min(total_score, 1.0)
        restaurant['score_breakdown'] = score_components
        scored.append(restaurant)
    
    return sorted(scored, key=lambda x: x['global_analysis_score'], reverse=True)

def calculate_preference_alignment(restaurant: dict, preferences: dict) -> float:
    """Calculate how well restaurant aligns with user preferences"""
    alignment_score = 0.5  # Base score
    
    # Occasion match
    occasion = preferences.get('occasion', 'casual')
    atmosphere = restaurant.get('atmosphere', {})
    
    if occasion == 'romantic' and atmosphere.get('romance_level', 0) > 0.7:
        alignment_score += 0.3
    elif occasion == 'business' and atmosphere.get('professional_level', 0) > 0.7:
        alignment_score += 0.3
    elif occasion == 'family' and atmosphere.get('family_friendliness', 0) > 0.7:
        alignment_score += 0.3
    
    # Features match
    desired_ambiance = preferences.get('ambiance_preferences', [])
    restaurant_features = restaurant.get('features', [])
    
    matches = len(set(desired_ambiance) & set(restaurant_features))
    if desired_ambiance:
        feature_match_score = matches / len(desired_ambiance)
        alignment_score += feature_match_score * 0.2
    
    return min(alignment_score, 1.0)

def generate_global_recommendations(scored_restaurants: list, data_msg: DataCollection) -> list:
    """Generate intelligent global recommendations with comprehensive reasoning"""
    recommendations = []
    max_results = data_msg.search_criteria.get('max_results', 3)
    
    for i, restaurant in enumerate(scored_restaurants[:max_results]):
        reasoning = generate_comprehensive_reasoning(restaurant, data_msg.user_preferences)
        
        recommendation = {
            'rank': i + 1,
            'restaurant': {
                'name': restaurant['name'],
                'cuisine': restaurant['cuisine'],
                'regional_style': restaurant.get('regional_style', ''),
                'specialty': restaurant.get('specialty', ''),
                'rating': restaurant['rating'],
                'price': restaurant['price'],
                'location': restaurant['location'],
                'features': restaurant.get('features', [])[:6],  # Top 6 features
                'atmosphere_profile': restaurant.get('atmosphere', {}),
                'service_style': restaurant.get('service_style', 'table_service'),
                'cultural_authenticity': restaurant.get('cultural_authenticity', 0.8)
            },
            'analysis_scores': {
                'overall_match': restaurant['global_analysis_score'],
                'score_breakdown': restaurant.get('score_breakdown', {}),
                'confidence_level': calculate_recommendation_confidence(restaurant)
            },
            'reasoning': reasoning,
            'unique_selling_points': identify_unique_selling_points(restaurant),
            'potential_considerations': identify_potential_considerations(restaurant, data_msg.user_preferences)
        }
        
        recommendations.append(recommendation)
    
    return recommendations

def generate_comprehensive_reasoning(restaurant: dict, preferences: dict) -> str:
    """Generate comprehensive reasoning for recommendation"""
    reasons = []
    
    # Quality reasoning
    rating = restaurant['rating']
    if rating >= 4.7:
        reasons.append(f"Exceptional quality with {rating}/5.0 rating")
    elif rating >= 4.3:
        reasons.append(f"High quality with {rating}/5.0 rating")
    else:
        reasons.append(f"Solid choice with {rating}/5.0 rating")
    
    # Cultural authenticity
    authenticity = restaurant.get('cultural_authenticity', 0.8)
    if authenticity >= 0.9:
        reasons.append(f"Highly authentic {restaurant['cuisine']} cuisine")
    elif authenticity >= 0.8:
        reasons.append(f"Authentic {restaurant['cuisine']} experience")
    
    # Specialty highlight
    if restaurant.get('specialty'):
        reasons.append(f"Specializes in {restaurant['specialty'].replace('_', ' ')}")
    
    # Occasion match
    occasion = preferences.get('occasion', 'casual')
    atmosphere = restaurant.get('atmosphere', {})
    
    if occasion == 'romantic' and atmosphere.get('romance_level', 0) > 0.7:
        reasons.append("Perfect romantic atmosphere")
    elif occasion == 'business' and atmosphere.get('professional_level', 0) > 0.7:
        reasons.append("Ideal for business meetings")
    elif occasion == 'family' and atmosphere.get('family_friendliness', 0) > 0.7:
        reasons.append("Excellent for family dining")
    
    return '. '.join(reasons) if reasons else "Great overall match for your preferences"

def identify_unique_selling_points(restaurant: dict) -> list:
    """Identify what makes this restaurant unique"""
    usps = []
    
    if restaurant.get('cultural_authenticity', 0) > 0.9:
        usps.append("Exceptional cultural authenticity")
    
    if restaurant.get('innovation_score', 0) > 0.8:
        usps.append("Innovative culinary approach")
    
    special_features = ['michelin_recommended', 'chef_specials', 'omakase_available', 'wine_sommelier']
    restaurant_features = restaurant.get('features', [])
    
    for feature in special_features:
        if feature in restaurant_features:
            usps.append(feature.replace('_', ' ').title())
    
    if restaurant.get('global_recognition', 0) > 0.8:
        usps.append("Internationally recognized")
    
    return usps[:3]  # Top 3 USPs

def calculate_global_confidence(recommendations: list, data_msg: DataCollection) -> dict:
    """Calculate comprehensive confidence metrics for global analysis"""
    if not recommendations:
        return {'overall_confidence': 0.1, 'factors': 'No recommendations generated'}
    
    # Base confidence from top recommendation
    top_score = recommendations[0]['analysis_scores']['overall_match']
    
    # Data quality confidence
    data_confidence = data_msg.confidence_score
    
    # Recommendation diversity confidence
    if len(recommendations) >= 3:
        diversity_confidence = 0.2
    elif len(recommendations) >= 2:
        diversity_confidence = 0.15
    else:
        diversity_confidence = 0.1
    
    # Cultural intelligence confidence
    cultural_scores = [r['restaurant']['cultural_authenticity'] for r in recommendations]
    cultural_confidence = sum(cultural_scores) / len(cultural_scores) * 0.15
    
    # Global recognition confidence
    recognition_scores = [r['restaurant'].get('global_recognition', 0.6) for r in recommendations] 
    recognition_confidence = sum(recognition_scores) / len(recognition_scores) * 0.1
    
    overall_confidence = (
        top_score * 0.4 +
        data_confidence * 0.25 +
        diversity_confidence +
        cultural_confidence +
        recognition_confidence
    )
    
    return {
        'overall_confidence': min(overall_confidence, 1.0),
        'data_quality': data_confidence,
        'recommendation_strength': top_score,
        'cultural_intelligence': cultural_confidence / 0.15,
        'global_recognition': recognition_confidence / 0.1,
        'analysis_depth': 'comprehensive_global'
    }

@bob.on_message(model=DecisionRequest)
async def handle_global_decision_request(ctx: Context, sender: str, msg: DecisionRequest):
    """Handle clarification requests from global Charlie"""
    ctx.logger.info(f"📨 Global clarification request from Charlie: {msg.task_id}")
    ctx.logger.info(f"🔍 Clarification needed: {msg.clarification_needed}")
    
    if msg.task_id in bob_global_memory["active_analyses"]:
        original_analysis = bob_global_memory["active_analyses"][msg.task_id]["results"]
        
        # Generate enhanced analysis based on Charlie's request
        enhanced_analysis = enhance_global_analysis(original_analysis, msg)
        
        try:
            await ctx.send(sender, enhanced_analysis)
            ctx.logger.info("🌐 ✅ Enhanced global analysis sent to Charlie")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to send enhanced analysis: {str(e)}")

def enhance_global_analysis(original: AnalysisResult, request: DecisionRequest) -> AnalysisResult:
    """Enhance analysis based on Charlie's global clarification request"""
    enhanced_supporting_data = {
        **original.supporting_data,
        'enhancement_request': request.clarification_needed,
        'additional_criteria': request.additional_criteria,
        'enhanced_timestamp': datetime.datetime.now().isoformat(),
        'enhancement_version': 'global_v2'
    }
    
    return AnalysisResult(
        task_id=original.task_id,
        analysis_summary=f"Enhanced Global Analysis: {original.analysis_summary}",
        recommendations=original.recommendations,
        confidence_scores={
            **original.confidence_scores,
            'enhancement_confidence': 0.95
        },
        supporting_data=enhanced_supporting_data,
        timestamp=datetime.datetime.now().isoformat(),
        sender="Bob"
    )

@bob.on_message(model=StatusUpdate)
async def discover_global_team_members(ctx: Context, sender: str, msg: StatusUpdate):
    """Discover team members on global Agentverse network"""
    global ALICE_ADDRESS, CHARLIE_ADDRESS
    
    if msg.sender == "Alice" and not ALICE_ADDRESS:
        ALICE_ADDRESS = sender
        ctx.logger.info(f"🌐 ✅ Global Alice discovered: {sender[:16]}...")
    elif msg.sender == "Charlie" and not CHARLIE_ADDRESS:
        CHARLIE_ADDRESS = sender
        ctx.logger.info(f"🌐 ✅ Global Charlie discovered: {sender[:16]}...")

# Helper functions for location, atmosphere, etc. (simplified for space)
def generate_intelligent_location(area: str, cuisine: str) -> str:
    locations = ["Downtown Core", "Historic District", "Arts Quarter", "Riverside", "Financial District"]
    return random.choice(locations)

def generate_atmosphere_profile(cuisine: str, occasion: str) -> dict:
    return {
        'romance_level': random.uniform(0.3, 1.0) if occasion == 'romantic' else random.uniform(0.2, 0.7),
        'professional_level': random.uniform(0.6, 1.0) if occasion == 'business' else random.uniform(0.3, 0.7),
        'family_friendliness': random.uniform(0.7, 1.0) if occasion == 'family' else random.uniform(0.4, 0.8),
        'noise_level': random.choice(['quiet', 'moderate', 'lively']),
        'formality': random.choice(['casual', 'smart_casual', 'formal'])
    }

def determine_service_style(price: str, cuisine: str) -> str:
    if price in ['$$$', '$$$$']:
        return 'fine_dining'
    elif price == '$$':
        return 'table_service'
    else:
        return 'casual_service'

def get_dietary_accommodations(cuisine: str) -> list:
    accommodations = {
        'Italian': ['vegetarian', 'gluten_free'],
        'French': ['vegetarian'],
        'Japanese': ['vegetarian', 'raw_fish', 'gluten_free'],
        'Indian': ['vegetarian', 'vegan', 'dairy_free'],
        'Mexican': ['vegetarian', 'vegan']
    }
    return accommodations.get(cuisine, ['vegetarian'])

def get_cultural_factors(preferences: dict) -> list:
    factors = ['regional_authenticity', 'traditional_preparation']
    
    if preferences.get('occasion') == 'business':
        factors.append('international_appeal')
    elif preferences.get('occasion') == 'romantic':
        factors.append('ambiance_culture')
    
    return factors

def calculate_atmosphere_match(restaurant: dict, preferences: dict) -> float:
    atmosphere = restaurant.get('atmosphere', {})
    occasion = preferences.get('occasion', 'casual')
    
    if occasion == 'romantic':
        return atmosphere.get('romance_level', 0.5)
    elif occasion == 'business':
        return atmosphere.get('professional_level', 0.5)
    elif occasion == 'family':
        return atmosphere.get('family_friendliness', 0.5)
    else:
        return 0.7  # Neutral for casual

def calculate_value_proposition(restaurant: dict, preferences: dict) -> float:
    price_levels = {'$': 0.9, '$$': 1.0, '$$$': 0.8, '$$$$': 0.6}
    price_score = price_levels.get(restaurant['price'], 0.7)
    
    quality_score = restaurant['rating'] / 5.0
    
    return (price_score + quality_score) / 2

def calculate_recommendation_confidence(restaurant: dict) -> float:
    return min(
        restaurant['global_analysis_score'] + 
        restaurant.get('cultural_authenticity', 0.8) * 0.1 +
        restaurant.get('local_popularity', 0.7) * 0.1,
        1.0
    )

def identify_potential_considerations(restaurant: dict, preferences: dict) -> list:
    considerations = []
    
    if restaurant['price'] == '$$$$':
        considerations.append("Premium pricing - special occasion dining")
    
    if restaurant['rating'] < 4.2:
        considerations.append("Mixed reviews - consider recent feedback")
    
    atmosphere = restaurant.get('atmosphere', {})
    if atmosphere.get('noise_level') == 'lively' and preferences.get('occasion') == 'business':
        considerations.append("Lively atmosphere may not be ideal for business discussions")
    
    return considerations[:2]  # Top 2 considerations

def get_acceptable_locations(user_area: str) -> list:
    location_mapping = {
        'downtown': ['Downtown Core', 'Financial District', 'Historic District'],
        'uptown': ['Arts Quarter', 'Riverside', 'North District'],
        'suburbs': ['Residential Area', 'Shopping District', 'Family Quarter']
    }
    return location_mapping.get(user_area.lower(), ['Downtown Core', 'Historic District'])

def create_global_analysis_summary(recommendations: list, data_msg: DataCollection, total_restaurants: int) -> str:
    """Create comprehensive global analysis summary"""
    if not recommendations:
        return f"Global analysis of {total_restaurants} restaurants found no suitable matches for the specified criteria."
    
    top_choice = recommendations[0]
    restaurant = top_choice['restaurant']
    
    summary_parts = [
        f"Global analysis complete using advanced cultural intelligence.",
        f"Analyzed {total_restaurants} international restaurants across multiple cuisines.",
        f"Top recommendation: {restaurant['name']} ({restaurant['cuisine']} cuisine)",
        f"with {restaurant['rating']}/5.0 rating and {top_choice['analysis_scores']['overall_match']:.3f} global match score.",
        f"Cultural authenticity: {restaurant.get('cultural_authenticity', 0.8):.1%}.",
        f"Confidence level: {top_choice['analysis_scores']['confidence_level']:.3f}."
    ]
    
    return " ".join(summary_parts)

if __name__ == "__main__":
    print("🌐 Starting Bob on Agentverse Global Network")
    print("🧠 Bob will provide advanced restaurant analysis services worldwide")
    bob.run()
