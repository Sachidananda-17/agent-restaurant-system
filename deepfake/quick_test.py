"""
Quick test script to run the system with basic functionality
"""

import asyncio
from agents.coordinator_agent import CoordinatorAgent
from agents.image_processor_agent import ImageProcessorAgent
from agents.forensic_analyzer_agent import ForensicAnalyzerAgent
from agents.report_generator_agent import ReportGeneratorAgent

async def main():
    print("🚀 Starting Deepfake Detection System (Basic Mode)")
    print("=" * 50)

    # Initialize agents
    coordinator = CoordinatorAgent(
        name="coordinator",
        seed="coordinator_seed_2024",
        port=8000
    )

    image_processor = ImageProcessorAgent(
        name="image_processor",
        seed="processor_seed_2024",
        port=8001
    )

    forensic_analyzer = ForensicAnalyzerAgent(
        name="forensic_analyzer",
        seed="analyzer_seed_2024",
        port=8002
    )

    report_generator = ReportGeneratorAgent(
        name="report_generator",
        seed="generator_seed_2024",
        port=8003
    )

    print("\n🤖 Agents Initialized:")
    print("- Coordinator Agent (Port 8000)")
    print("- Image Processor Agent (Port 8001)")
    print("- Forensic Analyzer Agent (Port 8002)")
    print("- Report Generator Agent (Port 8003)")

    print("\n📋 Basic Functionality Available:")
    print("- Face Detection")
    print("- Basic Image Analysis")
    print("- Metadata Analysis")
    print("- PDF Report Generation")

    print("\n⚠️ Note: Running in basic mode without full deepfake detection")
    print("To enable full functionality, training data is needed")

    # Start agents
    await asyncio.gather(
        coordinator.agent.run(),
        image_processor.agent.run(),
        forensic_analyzer.agent.run(),
        report_generator.agent.run()
    )

if __name__ == "__main__":
    print("\n🌐 Starting Web Interface at http://localhost:5000")
    print("Press Ctrl+C to stop the system")
    asyncio.run(main())
