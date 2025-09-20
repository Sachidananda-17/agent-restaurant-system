"""
Charlie - Final Decision Maker & Coordinator Agent
Role: Receives analysis from Bob, makes final decisions, coordinates the team
Collaborates with Alice (Data Collector) and Bob (Analyzer)
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
from config.agent_config import AGENTS, SYSTEM_CONFIG

# === CHARLIE AGENT SETUP ===
charlie = Agent(
    name=AGENTS["charlie"]["name"],
    seed=AGENTS["charlie"]["seed"],
    port=AGENTS["charlie"]["port"],
    endpoint=[AGENTS["charlie"]["endpoint"]]
)

# Store addresses of Alice and Bob
ALICE_ADDRESS = ""
BOB_ADDRESS = ""

# Charlie's decision-making memory and capabilities
charlie_memory = {
    "pending_decisions": {},
    "completed_decisions": [],
    "team_addresses": {},
    "decision_criteria": {
        "min_confidence_threshold": SYSTEM_CONFIG["decision_threshold"],
        "decision_factors": ["rating", "preference_match", "price", "location"],
        "risk_tolerance": "moderate"
    }
}

@charlie.on_event("startup")
async def charlie_startup(ctx: Context):
    """Charlie introduces his coordination capabilities"""
    ctx.logger.info("👑 Charlie Coordinator Agent Starting...")
    ctx.logger.info(f"📍 Charlie Address: {charlie.address}")
    ctx.logger.info("🎯 Role: Final Decision Making & Team Coordination")
    ctx.logger.info("🤝 Looking for Alice (Data Collector) and Bob (Analyzer)...")
    ctx.logger.info("🧠 Decision-Making Capabilities:")
    ctx.logger.info("   • Multi-criteria decision analysis")
    ctx.logger.info("   • Risk assessment & mitigation")
    ctx.logger.info("   • Team coordination & communication")
    ctx.logger.info("   • Consensus building & conflict resolution")
    ctx.logger.info(f"   • Confidence threshold: {charlie_memory['decision_criteria']['min_confidence_threshold']}")
    ctx.logger.info("🚀 Charlie is ready to coordinate and decide!")

# === TEAM DISCOVERY BROADCAST ===
@charlie.on_interval(period=20.0)
async def coordinate_team_status(ctx: Context):
    """Charlie broadcasts coordination status to the team"""
    status_msg = StatusUpdate(
        task_id="coordination",
        status="coordinating",
        progress_percentage=100,
        message="Charlie Coordinator managing team collaboration",
        timestamp=datetime.datetime.now().isoformat(),
        sender="Charlie"
    )
    
    ctx.logger.info("📡 Charlie coordinating team communication...")

# === MAIN DECISION HANDLER ===
@charlie.on_message(model=AnalysisResult)
async def make_final_decision(ctx: Context, sender: str, msg: AnalysisResult):
    """Charlie receives analysis from Bob and makes the final decision"""
    global BOB_ADDRESS
    
    ctx.logger.info(f"🎯 Decision request received for task: {msg.task_id}")
    ctx.logger.info(f"📊 From: {msg.sender}")
    ctx.logger.info(f"📋 Analysis Summary: {msg.analysis_summary}")
    ctx.logger.info(f"🏆 {len(msg.recommendations)} recommendations to evaluate")
    
    # Store the decision task
    charlie_memory["pending_decisions"][msg.task_id] = {
        "status": "evaluating",
        "start_time": datetime.datetime.now().isoformat(),
        "analysis_data": msg,
        "sender_address": sender
    }
    
    # Record Bob's address for future communication
    if not BOB_ADDRESS and msg.sender == "Bob":
        BOB_ADDRESS = sender
        charlie_memory["team_addresses"]["bob"] = sender
        ctx.logger.info(f"🤝 Bob address recorded: {sender}")
    
    ctx.logger.info("🔄 Starting decision evaluation process...")
    
    # Stage 1: Validate analysis quality
    analysis_quality = validate_analysis_quality(msg)
    ctx.logger.info(f"📊 Stage 1: Analysis quality score: {analysis_quality:.2f}")
    
    if analysis_quality < 0.6:
        # Request additional analysis if quality is low
        await request_additional_analysis(ctx, sender, msg)
        return
    
    # Stage 2: Apply decision criteria
    evaluated_options = apply_decision_criteria(msg)
    ctx.logger.info("📊 Stage 2: Decision criteria applied")
    
    # Stage 3: Make final decision
    final_choice = make_decision(evaluated_options, msg)
    ctx.logger.info(f"📊 Stage 3: Final decision made - {final_choice['name']}")
    
    # Stage 4: Calculate decision confidence
    decision_confidence = calculate_decision_confidence(final_choice, evaluated_options, msg)
    ctx.logger.info(f"📊 Stage 4: Decision confidence: {decision_confidence:.2f}")
    
    # Stage 5: Generate decision reasoning
    reasoning = generate_decision_reasoning(final_choice, evaluated_options, msg)
    
    # Prepare final decision
    final_decision = FinalDecision(
        task_id=msg.task_id,
        final_choice=final_choice,
        decision_reasoning=reasoning,
        confidence_score=decision_confidence,
        all_participants=["Alice", "Bob", "Charlie"],
        timestamp=datetime.datetime.now().isoformat(),
        sender="Charlie"
    )
    
    # Update decision status
    charlie_memory["pending_decisions"][msg.task_id]["status"] = "decided"
    charlie_memory["pending_decisions"][msg.task_id]["final_decision"] = final_decision
    
    # Broadcast decision to all team members
    await broadcast_decision(ctx, final_decision)
    
    # Archive the completed decision
    completed_decision = charlie_memory["pending_decisions"].pop(msg.task_id)
    completed_decision["completion_time"] = datetime.datetime.now().isoformat()
    charlie_memory["completed_decisions"].append(completed_decision)

def validate_analysis_quality(analysis: AnalysisResult) -> float:
    """Stage 1: Validate the quality of Bob's analysis"""
    quality_score = 0.0
    
    # Check recommendation count
    if len(analysis.recommendations) >= 3:
        quality_score += 0.3
    elif len(analysis.recommendations) >= 1:
        quality_score += 0.2
    
    # Check confidence scores
    overall_confidence = analysis.confidence_scores.get("overall_confidence", 0)
    quality_score += overall_confidence * 0.4
    
    # Check analysis completeness
    if analysis.supporting_data:
        quality_score += 0.2
    
    # Check reasoning quality (simplified)
    if analysis.analysis_summary and len(analysis.analysis_summary) > 50:
        quality_score += 0.1
    
    return min(quality_score, 1.0)

async def request_additional_analysis(ctx: Context, bob_address: str, original_analysis: AnalysisResult):
    """Request additional analysis from Bob if quality is insufficient"""
    ctx.logger.info("⚠️ Analysis quality below threshold - requesting enhancement")
    
    clarification_request = DecisionRequest(
        task_id=original_analysis.task_id,
        clarification_needed="Need more detailed analysis with additional criteria",
        additional_criteria={
            "detailed_scoring": True,
            "risk_assessment": True,
            "alternative_options": True
        },
        timestamp=datetime.datetime.now().isoformat(),
        sender="Charlie"
    )
    
    try:
        await ctx.send(bob_address, clarification_request)
        ctx.logger.info("📤 Additional analysis requested from Bob")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to request additional analysis: {str(e)}")

def apply_decision_criteria(analysis: AnalysisResult) -> list:
    """Stage 2: Apply Charlie's decision criteria to recommendations"""
    evaluated_options = []
    
    for rec in analysis.recommendations:
        # Calculate Charlie's decision score
        charlie_score = calculate_charlie_score(rec, analysis)
        
        # Add risk assessment
        risk_assessment = assess_option_risk(rec)
        
        # Create evaluated option
        evaluated_option = {
            **rec,
            "charlie_score": charlie_score,
            "risk_assessment": risk_assessment,
            "decision_factors": get_decision_factors(rec)
        }
        
        evaluated_options.append(evaluated_option)
    
    # Sort by Charlie's scoring (highest first)
    return sorted(evaluated_options, key=lambda x: x["charlie_score"], reverse=True)

def calculate_charlie_score(recommendation: dict, analysis: AnalysisResult) -> float:
    """Calculate Charlie's decision score for an option"""
    score = 0.0
    
    # Base score from Bob's analysis (50% weight)
    score += recommendation["analysis_score"] * 0.5
    
    # Decision-specific factors (50% weight)
    restaurant = recommendation["restaurant"]
    
    # Rating importance (20% weight)
    rating_score = (restaurant["rating"] / 5.0) * 0.2
    score += rating_score
    
    # Price reasonableness (15% weight) 
    price_score = get_price_reasonableness_score(restaurant["price"])
    score += price_score * 0.15
    
    # Feature completeness (10% weight)
    features = restaurant.get("features", [])
    feature_score = min(len(features) * 0.02, 0.1)
    score += feature_score
    
    # Confidence bonus (5% weight)
    confidence_bonus = analysis.confidence_scores.get("overall_confidence", 0) * 0.05
    score += confidence_bonus
    
    return min(score, 1.0)

def get_price_reasonableness_score(price: str) -> float:
    """Assess price reasonableness"""
    price_scores = {"$": 0.9, "$$": 1.0, "$$$": 0.8, "$$$$": 0.6}
    return price_scores.get(price, 0.5)

def assess_option_risk(recommendation: dict) -> dict:
    """Assess potential risks of choosing this option"""
    risks = []
    risk_level = "low"
    
    restaurant = recommendation["restaurant"]
    
    # Rating-based risk
    if restaurant["rating"] < 4.0:
        risks.append("Below average customer satisfaction")
        risk_level = "medium"
    
    # Price-based risk
    if restaurant["price"] == "$$$$":
        risks.append("High cost may exceed budget")
        risk_level = "medium"
    
    # Location-based risk
    if restaurant["location"] == "Suburbs":
        risks.append("Distance may be inconvenient")
    
    # Limited features risk
    if len(restaurant.get("features", [])) < 2:
        risks.append("Limited amenities or features")
    
    if len(risks) >= 3:
        risk_level = "high"
    elif len(risks) >= 2:
        risk_level = "medium"
    
    return {
        "risk_level": risk_level,
        "identified_risks": risks,
        "risk_score": len(risks) * 0.1
    }

def get_decision_factors(recommendation: dict) -> dict:
    """Extract key factors that influenced the decision"""
    return {
        "rating": recommendation["restaurant"]["rating"],
        "analysis_score": recommendation["analysis_score"],
        "pros_count": len(recommendation.get("pros", [])),
        "cons_count": len(recommendation.get("cons", []))
    }

def make_decision(evaluated_options: list, analysis: AnalysisResult) -> dict:
    """Stage 3: Make the final decision"""
    
    if not evaluated_options:
        # Fallback decision if no options available
        return {
            "name": "No suitable options found",
            "reasoning": "Unable to find restaurants matching criteria"
        }
    
    # Apply decision threshold
    top_option = evaluated_options[0]
    
    # Check if top option meets confidence threshold
    min_threshold = charlie_memory["decision_criteria"]["min_confidence_threshold"]
    
    if top_option["charlie_score"] >= min_threshold:
        # High confidence decision
        chosen_restaurant = top_option["restaurant"]
        return {
            "name": chosen_restaurant["name"],
            "cuisine": chosen_restaurant["cuisine"],
            "rating": chosen_restaurant["rating"],
            "price": chosen_restaurant["price"],
            "location": chosen_restaurant["location"],
            "features": chosen_restaurant.get("features", []),
            "decision_score": top_option["charlie_score"],
            "rank": top_option["rank"],
            "risk_level": top_option["risk_assessment"]["risk_level"]
        }
    else:
        # Lower confidence - consider top 2 options
        if len(evaluated_options) >= 2:
            second_option = evaluated_options[1]
            score_diff = top_option["charlie_score"] - second_option["charlie_score"]
            
            if score_diff < 0.1:  # Very close scores
                # Choose based on lowest risk
                if top_option["risk_assessment"]["risk_level"] == "low":
                    return format_final_choice(top_option)
                elif second_option["risk_assessment"]["risk_level"] == "low":
                    return format_final_choice(second_option)
        
        # Default to top option
        return format_final_choice(top_option)

def format_final_choice(option: dict) -> dict:
    """Format the final choice consistently"""
    restaurant = option["restaurant"]
    return {
        "name": restaurant["name"],
        "cuisine": restaurant["cuisine"], 
        "rating": restaurant["rating"],
        "price": restaurant["price"],
        "location": restaurant["location"],
        "features": restaurant.get("features", []),
        "decision_score": option["charlie_score"],
        "rank": option["rank"],
        "risk_level": option["risk_assessment"]["risk_level"]
    }

def calculate_decision_confidence(final_choice: dict, evaluated_options: list, analysis: AnalysisResult) -> float:
    """Stage 4: Calculate confidence in the final decision"""
    
    # Base confidence from analysis
    analysis_confidence = analysis.confidence_scores.get("overall_confidence", 0.5)
    
    # Decision score confidence
    decision_score_confidence = final_choice.get("decision_score", 0.5)
    
    # Option spread confidence (more options = more confidence in choice)
    option_count_confidence = min(len(evaluated_options) * 0.1, 0.3)
    
    # Risk level confidence (lower risk = higher confidence)
    risk_confidence = {"low": 0.2, "medium": 0.1, "high": 0.05}.get(
        final_choice.get("risk_level", "medium"), 0.1
    )
    
    total_confidence = (
        analysis_confidence * 0.4 + 
        decision_score_confidence * 0.3 + 
        option_count_confidence * 0.2 + 
        risk_confidence * 0.1
    )
    
    return min(total_confidence, 1.0)

def generate_decision_reasoning(final_choice: dict, evaluated_options: list, analysis: AnalysisResult) -> str:
    """Generate clear reasoning for the final decision"""
    
    reasoning_parts = [
        f"Selected {final_choice['name']} based on comprehensive multi-criteria analysis.",
    ]
    
    # Add score-based reasoning
    if final_choice.get("decision_score", 0) >= 0.8:
        reasoning_parts.append("Excellent overall match with high confidence scores.")
    elif final_choice.get("decision_score", 0) >= 0.7:
        reasoning_parts.append("Very good match meeting all key criteria.")
    else:
        reasoning_parts.append("Best available option meeting minimum requirements.")
    
    # Add specific strengths
    rating = final_choice.get("rating", 0)
    if rating >= 4.5:
        reasoning_parts.append(f"Outstanding customer rating of {rating}/5.0.")
    elif rating >= 4.0:
        reasoning_parts.append(f"Strong customer rating of {rating}/5.0.")
    
    # Add risk assessment
    risk_level = final_choice.get("risk_level", "medium")
    if risk_level == "low":
        reasoning_parts.append("Low risk option with minimal identified concerns.")
    elif risk_level == "medium":
        reasoning_parts.append("Moderate risk option with manageable considerations.")
    
    # Add comparative reasoning
    if len(evaluated_options) > 1:
        reasoning_parts.append(f"Chosen from {len(evaluated_options)} analyzed options.")
    
    return " ".join(reasoning_parts)

async def broadcast_decision(ctx: Context, final_decision: FinalDecision):
    """Broadcast the final decision to all team members"""
    
    ctx.logger.info("📢 Broadcasting final decision to team...")
    
    # Send to Alice if address known
    if ALICE_ADDRESS:
        try:
            await ctx.send(ALICE_ADDRESS, final_decision)
            ctx.logger.info("📤 Decision sent to Alice")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to send decision to Alice: {str(e)}")
    
    # Send to Bob if address known  
    if BOB_ADDRESS:
        try:
            await ctx.send(BOB_ADDRESS, final_decision)
            ctx.logger.info("📤 Decision sent to Bob")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to send decision to Bob: {str(e)}")
    
    # Log the final decision details
    ctx.logger.info("🎉 FINAL DECISION SUMMARY:")
    ctx.logger.info(f"   🏆 Choice: {final_decision.final_choice['name']}")
    ctx.logger.info(f"   🍽️ Cuisine: {final_decision.final_choice['cuisine']}")
    ctx.logger.info(f"   ⭐ Rating: {final_decision.final_choice['rating']}/5.0")
    ctx.logger.info(f"   💰 Price: {final_decision.final_choice['price']}")
    ctx.logger.info(f"   📍 Location: {final_decision.final_choice['location']}")
    ctx.logger.info(f"   📊 Confidence: {final_decision.confidence_score:.2f}")
    ctx.logger.info(f"   💭 Reasoning: {final_decision.decision_reasoning}")

# === TEAM DISCOVERY ===
@charlie.on_message(model=StatusUpdate)
async def handle_team_discovery(ctx: Context, sender: str, msg: StatusUpdate):
    """Discover other team members"""
    global ALICE_ADDRESS, BOB_ADDRESS
    if msg.sender == "Alice" and not ALICE_ADDRESS:
        ALICE_ADDRESS = sender
        charlie_memory["team_addresses"]["alice"] = sender
        ctx.logger.info(f"🤝 Alice discovered! Address: {sender}")
    elif msg.sender == "Bob" and not BOB_ADDRESS:
        BOB_ADDRESS = sender
        charlie_memory["team_addresses"]["bob"] = sender
        ctx.logger.info(f"🤝 Bob discovered! Address: {sender}")

if __name__ == "__main__":
    print("👑 Starting Charlie - Decision Coordinator Agent")
    print(f"📍 Charlie will run on port {AGENTS['charlie']['port']}")
    charlie.run()
