"""
Report Generator Agent - Creates comprehensive PDF reports
"""

from datetime import datetime
import time
from pathlib import Path
from typing import Dict, Any, List
import json
from fpdf import FPDF
from PIL import Image
import io
import base64

from uagents import Context
from .base_agent import BaseAgent, TaskRequest, ReportResult

class DeepfakeReport(FPDF):
    """Custom PDF class for deepfake analysis reports"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        # Use built-in Helvetica font instead of DejaVu
        self.set_font('Helvetica', '', 12)
        
    def header(self):
        """Add report header"""
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'Deepfake Analysis Report', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        """Add report footer"""
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')
        
    def chapter_title(self, title: str):
        """Add chapter title"""
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
        
    def chapter_body(self, text: str):
        """Add chapter body text"""
        self.set_font('Helvetica', '', 11)
        self.multi_cell(0, 10, text)
        self.ln()
        
    def add_image(self, image_path: str, caption: str = ""):
        """Add image with caption"""
        if Path(image_path).exists():
            self.image(image_path, x=10, w=190)
            if caption:
                self.set_font('Helvetica', '', 10)
                self.cell(0, 10, caption, 0, 1, 'C')
                self.ln(5)

class ReportGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating comprehensive analysis reports
    """
    
    def __init__(self, name: str, seed: str, port: int):
        """Initialize the Report Generator Agent"""
        super().__init__(name, seed, port)
        self._register_report_generator_handlers()
        self.report_dir = Path("reports")
        self.report_dir.mkdir(exist_ok=True)

    def _register_report_generator_handlers(self):
        """Register report generator specific message handlers"""
        
        @self.agent.on_message(model=TaskRequest)
        async def generate_report(ctx: Context, sender: str, msg: TaskRequest):
            """Generate comprehensive analysis report"""
            try:
                start_time = time.time()
                
                # Generate report
                report_path = self._generate_report(
                    msg.task_id,
                    msg.data["analysis_result"],
                    msg.data["forensic_result"]
                )
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                # Generate report summary
                summary = self._generate_report_summary(
                    msg.data["analysis_result"],
                    msg.data["forensic_result"]
                )
                
                # Send results
                await ctx.send(
                    sender,
                    ReportResult(
                        task_id=msg.task_id,
                        timestamp=datetime.now().isoformat(),
                        sender=self.agent.name,
                        message_type="report_result",
                        data={
                            "report_path": str(report_path),
                            "processing_time": processing_time,
                            "summary": summary
                        },
                        report_path=str(report_path),
                        report_summary=summary,
                        status="completed"
                    )
                )
                
            except Exception as e:
                await self.handle_error(ctx, msg.task_id, e)

    def _generate_report(
        self,
        task_id: str,
        analysis_result: Dict[str, Any],
        forensic_result: Dict[str, Any]
    ) -> Path:
        """Create comprehensive PDF report"""
        print("\n📄 Starting report generation process...")
        report_path = self.report_dir / f"deepfake_analysis_{task_id}.pdf"
        print(f"📝 Report will be saved to: {report_path}")
        
        # Create PDF
        pdf = DeepfakeReport()
        pdf.alias_nb_pages()
        
        # Add cover page
        self._add_cover_page(pdf, task_id)
        
        # Add executive summary
        self._add_executive_summary(pdf, analysis_result, forensic_result)
        
        # Add technical analysis
        self._add_technical_analysis(pdf, analysis_result)
        
        # Add forensic analysis
        self._add_forensic_analysis(pdf, forensic_result)
        
        # Add visualizations
        self._add_visualizations(pdf, analysis_result, forensic_result)
        
        # Add metadata analysis
        self._add_metadata_analysis(pdf, forensic_result["metadata"])
        
        # Add conclusion
        self._add_conclusion(pdf, analysis_result, forensic_result)
        
        # Save report
        pdf.output(str(report_path))
        
        return report_path

    def _add_cover_page(self, pdf: DeepfakeReport, task_id: str):
        """Add report cover page"""
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 24)
        pdf.cell(0, 20, 'Deepfake Analysis Report', 0, 1, 'C')
        pdf.ln(20)
        
        pdf.set_font('Helvetica', '', 12)
        pdf.cell(0, 10, f'Analysis ID: {task_id}', 0, 1, 'C')
        pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        
        pdf.ln(50)
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 10, 'CONFIDENTIAL', 0, 1, 'C')

    def _add_executive_summary(
        self,
        pdf: DeepfakeReport,
        analysis_result: Dict[str, Any],
        forensic_result: Dict[str, Any]
    ):
        """Add executive summary section"""
        pdf.add_page()
        pdf.chapter_title('Executive Summary')
        
        # Calculate overall verdict with weighted scores
        deepfake_score = analysis_result["confidence_score"]
        ela_score = forensic_result["ela_analysis"]["score"]
        compression_score = max(0, 1 + forensic_result["compression_analysis"]["score"])  # Normalize negative scores
        noise_score = max(0, forensic_result["noise_analysis"]["score"])
        
        # Weight the scores (deep learning model has highest weight)
        weighted_score = (
            0.4 * deepfake_score +  # Deep learning model
            0.3 * ela_score +       # Error Level Analysis
            0.2 * compression_score + # Compression analysis
            0.1 * noise_score        # Noise analysis
        )
        
        # Final verdict based on weighted score and model prediction
        is_fake = weighted_score > 0.5 or analysis_result["prediction"].upper() == "FAKE"
        verdict = "LIKELY FAKE" if is_fake else "LIKELY GENUINE"
        confidence = f"{weighted_score * 100:.1f}%"
        
        # Get confidence level interpretation
        confidence_level = self._get_confidence_interpretation(weighted_score)
        
        summary_text = (
            f"Analysis Verdict: {verdict}\n"
            f"Confidence Level: {confidence} ({confidence_level})\n\n"
            f"Interpretation: {self._get_verdict_explanation(weighted_score, analysis_result, forensic_result)}\n\n"
            f"Key Findings:\n"
            f"- Deepfake Detection Score: {deepfake_score * 100:.1f}%\n"
            f"- Forensic Analysis Score: {forensic_score * 100:.1f}%\n"
            f"- Number of Faces Detected: {analysis_result['num_faces_detected']}\n"
        )
        
        if forensic_result["anomalies"]:
            summary_text += "\nDetected Anomalies:\n"
            for category, anomalies in forensic_result["anomalies"].items():
                for anomaly in anomalies:
                    summary_text += f"- {category.title()}: {anomaly}\n"
        
        pdf.chapter_body(summary_text)

    def _add_technical_analysis(self, pdf: DeepfakeReport, analysis_result: Dict[str, Any]):
        """Add technical analysis section"""
        pdf.add_page()
        pdf.chapter_title('Technical Analysis')
        
        # Add deepfake detection results
        analysis_text = (
            f"Deepfake Detection Analysis:\n"
            f"- Prediction: {analysis_result['prediction'].upper()}\n"
            f"- Confidence Score: {analysis_result['confidence_score'] * 100:.1f}%\n\n"
            f"Image Analysis:\n"
            f"- Resolution: {analysis_result['analysis_details']['resolution']}\n"
            f"- Aspect Ratio: {analysis_result['analysis_details']['aspect_ratio']:.2f}\n\n"
        )
        
        # Add color analysis
        color_analysis = analysis_result['analysis_details']['color_analysis']
        analysis_text += (
            f"Color Distribution Analysis:\n"
            f"- Red Channel - Mean: {color_analysis['mean_r']:.1f}, Std: {color_analysis['std_r']:.1f}\n"
            f"- Green Channel - Mean: {color_analysis['mean_g']:.1f}, Std: {color_analysis['std_g']:.1f}\n"
            f"- Blue Channel - Mean: {color_analysis['mean_b']:.1f}, Std: {color_analysis['std_b']:.1f}\n"
        )
        
        pdf.chapter_body(analysis_text)
        
        # Add visualization
        if 'heatmap_path' in analysis_result:
            pdf.add_image(
                analysis_result['heatmap_path'],
                'Figure 1: Deepfake Detection Heatmap'
            )

    def _add_forensic_analysis(self, pdf: DeepfakeReport, forensic_result: Dict[str, Any]):
        """Add forensic analysis section"""
        pdf.add_page()
        pdf.chapter_title('Forensic Analysis')
        
        # Add ELA analysis
        ela_text = (
            f"Error Level Analysis (ELA):\n"
            f"- Score: {forensic_result['ela_analysis']['score'] * 100:.1f}%\n"
            f"- Analysis: {forensic_result['ela_analysis']['analysis']}\n"
            f"- Mean Error: {forensic_result['ela_analysis']['mean_error']:.2f}\n"
            f"- Standard Deviation: {forensic_result['ela_analysis']['std_error']:.2f}\n\n"
        )
        
        # Add compression analysis
        compression_text = (
            f"Compression Analysis:\n"
            f"- Score: {forensic_result['compression_analysis']['score'] * 100:.1f}%\n"
            f"- Analysis: {forensic_result['compression_analysis']['analysis']}\n"
            f"- Mean Coefficients: {forensic_result['compression_analysis']['mean_coefficients']:.2f}\n"
            f"- Std Coefficients: {forensic_result['compression_analysis']['std_coefficients']:.2f}\n\n"
        )
        
        # Add noise analysis
        noise_text = (
            f"Noise Pattern Analysis:\n"
            f"- Score: {forensic_result['noise_analysis']['score'] * 100:.1f}%\n"
            f"- Analysis: {forensic_result['noise_analysis']['analysis']}\n\n"
        )
        
        pdf.chapter_body(ela_text + compression_text + noise_text)

    def _add_visualizations(
        self,
        pdf: DeepfakeReport,
        analysis_result: Dict[str, Any],
        forensic_result: Dict[str, Any]
    ):
        """Add visualization section"""
        pdf.add_page()
        pdf.chapter_title('Visual Analysis')

        # Add original image
        if 'filepath' in analysis_result:
            try:
                pdf.image(analysis_result['filepath'], x=10, y=None, w=190)
                pdf.ln(10)
                pdf.chapter_body("Original Image")
                pdf.ln(10)
            except Exception as e:
                pdf.chapter_body(f"Note: Could not add original image ({str(e)})")

        # Add heatmap if available
        if 'heatmap_path' in analysis_result and Path(analysis_result['heatmap_path']).exists():
            try:
                pdf.image(analysis_result['heatmap_path'], x=10, y=None, w=190)
                pdf.ln(10)
                pdf.chapter_body("Deepfake Detection Heatmap")
                pdf.ln(10)
            except Exception as e:
                pdf.chapter_body(f"Note: Could not add heatmap visualization ({str(e)})")
        
        # Add scores as text
        scores_text = "\nAnalysis Scores:\n"
        scores = {
            'Deepfake Detection (40% weight)': analysis_result['confidence_score'],
            'ELA Analysis (30% weight)': forensic_result['ela_analysis']['score'],
            'Compression (20% weight)': max(0, 1 + forensic_result['compression_analysis']['score']),
            'Noise Analysis (10% weight)': forensic_result['noise_analysis']['score']
        }
        
        # Add visual indicators for scores
        for name, score in scores.items():
            bar_length = int(score * 20)  # 20 characters for 100%
            bar = '█' * bar_length + '░' * (20 - bar_length)
            confidence_level = self._get_confidence_interpretation(score)
            scores_text += f"- {name}:\n"
            scores_text += f"  {score * 100:.1f}% {bar} ({confidence_level})\n"
        pdf.chapter_body(scores_text)
        
        # Add noise pattern analysis as text
        if 'noise_analysis' in forensic_result:
            noise_text = "\nNoise Pattern Analysis by Channel:\n"
            stats = forensic_result['noise_analysis']['channel_statistics']
            channels = ['Red', 'Green', 'Blue']
            for channel, stat in zip(channels, stats):
                noise_text += f"- {channel} Channel:\n"
                noise_text += f"  Mean: {stat['mean']:.2f}\n"
                noise_text += f"  Std: {stat['std']:.2f}\n"
            pdf.chapter_body(noise_text)

    def _add_metadata_analysis(self, pdf: DeepfakeReport, metadata: Dict[str, Any]):
        """Add metadata analysis section"""
        pdf.add_page()
        pdf.chapter_title('Metadata Analysis')
        
        metadata_text = "File Information:\n"
        for key, value in metadata.items():
            if key not in ('JPEGThumbnail', 'TIFFThumbnail'):
                metadata_text += f"- {key}: {value}\n"
        
        pdf.chapter_body(metadata_text)

    def _add_conclusion(
        self,
        pdf: DeepfakeReport,
        analysis_result: Dict[str, Any],
        forensic_result: Dict[str, Any]
    ):
        """Add conclusion section"""
        pdf.add_page()
        pdf.chapter_title('Conclusion')
        
        # Calculate overall assessment
        overall_score = (
            analysis_result["confidence_score"] + 
            forensic_result["forensic_score"]
        ) / 2
        
        conclusion_text = (
            f"Based on comprehensive analysis of both visual and forensic evidence, "
            f"this image is assessed to be "
            f"{'LIKELY FAKE' if overall_score > 0.5 else 'LIKELY GENUINE'} "
            f"with {overall_score * 100:.1f}% confidence.\n\n"
        )
        
        # Add supporting evidence
        conclusion_text += "Supporting Evidence:\n"
        if analysis_result["confidence_score"] > 0.5:
            conclusion_text += (
                f"- Deep learning model detected manipulation patterns with "
                f"{analysis_result['confidence_score'] * 100:.1f}% confidence\n"
            )
        
        if forensic_result["anomalies"]:
            conclusion_text += "- Detected forensic anomalies:\n"
            for category, anomalies in forensic_result["anomalies"].items():
                for anomaly in anomalies:
                    conclusion_text += f"  - {anomaly}\n"
        
        pdf.chapter_body(conclusion_text)
        
        # Add recommendations
        pdf.ln(10)
        pdf.chapter_title('Recommendations')
        recommendations = self._get_recommendations(weighted_score, analysis_result, forensic_result)
        pdf.chapter_body(recommendations)


    def _get_confidence_interpretation(self, score: float) -> str:
        """Get human-readable interpretation of confidence score"""
        if score >= 0.9:
            return "Very High Confidence"
        elif score >= 0.75:
            return "High Confidence"
        elif score >= 0.6:
            return "Moderate Confidence"
        elif score >= 0.5:
            return "Low Confidence"
        else:
            return "Very Low Confidence"

    def _get_verdict_explanation(
        self,
        weighted_score: float,
        analysis_result: Dict[str, Any],
        forensic_result: Dict[str, Any]
    ) -> str:
        """Generate detailed explanation of the verdict"""
        model_verdict = "fake" if analysis_result["prediction"].upper() == "FAKE" else "genuine"
        ela_verdict = "manipulated" if forensic_result["ela_analysis"]["score"] < 0.5 else "not manipulated"
        compression_analysis = forensic_result["compression_analysis"]["analysis"].lower()
        noise_verdict = forensic_result["noise_analysis"]["analysis"]
        
        explanation = (
            f"The deep learning model suggests this image is {model_verdict}. "
            f"Error Level Analysis indicates the image is {ela_verdict}. "
            f"The image shows {compression_analysis}, and noise analysis reveals {noise_verdict.lower()}. "
            f"Based on these factors, with a weighted confidence of {weighted_score * 100:.1f}%, "
            f"our analysis suggests this image is {'likely manipulated' if weighted_score > 0.5 else 'likely genuine'}."
        )
        return explanation

    def _get_recommendations(
        self,
        weighted_score: float,
        analysis_result: Dict[str, Any],
        forensic_result: Dict[str, Any]
    ) -> str:
        """Generate recommendations based on analysis results"""
        recommendations = []
        
        # Add general recommendations
        if weighted_score > 0.5:
            recommendations.extend([
                "Consider requesting the original, unedited source image",
                "Look for additional context or metadata about the image's origin",
                "If this image is being used in a critical context, seek additional verification methods"
            ])
        
        # Add specific recommendations based on analysis
        if forensic_result["compression_analysis"]["score"] < 0:
            recommendations.append(
                "The image shows unusual compression patterns. Request a higher quality version if available."
            )
        
        if forensic_result["noise_analysis"]["score"] == 0:
            recommendations.append(
                "Inconsistent noise patterns detected. This could indicate image manipulation or heavy post-processing."
            )
        
        if analysis_result["num_faces_detected"] > 0:
            recommendations.append(
                f"This image contains {analysis_result['num_faces_detected']} detected face(s). "
                "For face-related analysis, consider using specialized face authentication tools."
            )
        
        # Format recommendations
        if not recommendations:
            recommendations = ["No specific recommendations at this time."]
        
        return "Based on our analysis, we recommend:\n" + "\n".join(f"- {r}" for r in recommendations)

    def _generate_report_summary(
        self,
        analysis_result: Dict[str, Any],
        forensic_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a summary of the report findings"""
        # Calculate weighted scores
        deepfake_score = analysis_result["confidence_score"]
        ela_score = forensic_result["ela_analysis"]["score"]
        compression_score = max(0, 1 + forensic_result["compression_analysis"]["score"])
        noise_score = max(0, forensic_result["noise_analysis"]["score"])
        
        # Weight the scores
        weighted_score = (
            0.4 * deepfake_score +    # Deep learning model
            0.3 * ela_score +         # Error Level Analysis
            0.2 * compression_score + # Compression analysis
            0.1 * noise_score        # Noise analysis
        )
        
        # Final verdict based on weighted score and model prediction
        is_fake = weighted_score > 0.5 or analysis_result["prediction"].upper() == "FAKE"
        
        return {
            "verdict": "LIKELY FAKE" if is_fake else "LIKELY GENUINE",
            "confidence": weighted_score,
            "deepfake_score": deepfake_score,
            "ela_score": ela_score,
            "compression_score": compression_score,
            "noise_score": noise_score,
            "num_anomalies": sum(
                len(anomalies) 
                for anomalies in forensic_result["anomalies"].values()
            ),
            "timestamp": datetime.now().isoformat()
        }
