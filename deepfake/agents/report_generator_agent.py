"""
Report Generator Agent - Creates comprehensive PDF reports
"""

from datetime import datetime
import time
from pathlib import Path
from typing import Dict, Any, List
import json
from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
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
        report_path = self.report_dir / f"deepfake_analysis_{task_id}.pdf"
        
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
        pdf.set_font('DejaVu', 'B', 24)
        pdf.cell(0, 20, 'Deepfake Analysis Report', 0, 1, 'C')
        pdf.ln(20)
        
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(0, 10, f'Analysis ID: {task_id}', 0, 1, 'C')
        pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        
        pdf.ln(50)
        pdf.set_font('DejaVu', '', 10)
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
        
        # Calculate overall verdict
        deepfake_score = analysis_result["confidence_score"]
        forensic_score = forensic_result["forensic_score"]
        overall_score = (deepfake_score + forensic_score) / 2
        
        verdict = "LIKELY FAKE" if overall_score > 0.5 else "LIKELY GENUINE"
        confidence = f"{overall_score * 100:.1f}%"
        
        summary_text = (
            f"Analysis Verdict: {verdict}\n"
            f"Confidence Level: {confidence}\n\n"
            f"Key Findings:\n"
            f"• Deepfake Detection Score: {deepfake_score * 100:.1f}%\n"
            f"• Forensic Analysis Score: {forensic_score * 100:.1f}%\n"
            f"• Number of Faces Detected: {analysis_result['num_faces_detected']}\n"
        )
        
        if forensic_result["anomalies"]:
            summary_text += "\nDetected Anomalies:\n"
            for category, anomalies in forensic_result["anomalies"].items():
                for anomaly in anomalies:
                    summary_text += f"• {category.title()}: {anomaly}\n"
        
        pdf.chapter_body(summary_text)

    def _add_technical_analysis(self, pdf: DeepfakeReport, analysis_result: Dict[str, Any]):
        """Add technical analysis section"""
        pdf.add_page()
        pdf.chapter_title('Technical Analysis')
        
        # Add deepfake detection results
        analysis_text = (
            f"Deepfake Detection Analysis:\n"
            f"• Prediction: {analysis_result['prediction'].upper()}\n"
            f"• Confidence Score: {analysis_result['confidence_score'] * 100:.1f}%\n\n"
            f"Image Analysis:\n"
            f"• Resolution: {analysis_result['analysis_details']['resolution']}\n"
            f"• Aspect Ratio: {analysis_result['analysis_details']['aspect_ratio']:.2f}\n\n"
        )
        
        # Add color analysis
        color_analysis = analysis_result['analysis_details']['color_analysis']
        analysis_text += (
            f"Color Distribution Analysis:\n"
            f"• Red Channel - Mean: {color_analysis['mean_r']:.1f}, Std: {color_analysis['std_r']:.1f}\n"
            f"• Green Channel - Mean: {color_analysis['mean_g']:.1f}, Std: {color_analysis['std_g']:.1f}\n"
            f"• Blue Channel - Mean: {color_analysis['mean_b']:.1f}, Std: {color_analysis['std_b']:.1f}\n"
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
            f"• Score: {forensic_result['ela_analysis']['score'] * 100:.1f}%\n"
            f"• Analysis: {forensic_result['ela_analysis']['analysis']}\n"
            f"• Mean Error: {forensic_result['ela_analysis']['mean_error']:.2f}\n"
            f"• Standard Deviation: {forensic_result['ela_analysis']['std_error']:.2f}\n\n"
        )
        
        # Add compression analysis
        compression_text = (
            f"Compression Analysis:\n"
            f"• Score: {forensic_result['compression_analysis']['score'] * 100:.1f}%\n"
            f"• Analysis: {forensic_result['compression_analysis']['analysis']}\n"
            f"• Mean Coefficients: {forensic_result['compression_analysis']['mean_coefficients']:.2f}\n"
            f"• Std Coefficients: {forensic_result['compression_analysis']['std_coefficients']:.2f}\n\n"
        )
        
        # Add noise analysis
        noise_text = (
            f"Noise Pattern Analysis:\n"
            f"• Score: {forensic_result['noise_analysis']['score'] * 100:.1f}%\n"
            f"• Analysis: {forensic_result['noise_analysis']['analysis']}\n\n"
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
        
        # Create and add confidence score comparison chart
        scores_fig = self._create_score_comparison_chart(analysis_result, forensic_result)
        pdf.image(scores_fig, x=10, w=190)
        
        # Add noise pattern visualization if available
        if 'noise_analysis' in forensic_result:
            noise_fig = self._create_noise_pattern_visualization(
                forensic_result['noise_analysis']
            )
            pdf.image(noise_fig, x=10, w=190)

    def _add_metadata_analysis(self, pdf: DeepfakeReport, metadata: Dict[str, Any]):
        """Add metadata analysis section"""
        pdf.add_page()
        pdf.chapter_title('Metadata Analysis')
        
        metadata_text = "File Information:\n"
        for key, value in metadata.items():
            if key not in ('JPEGThumbnail', 'TIFFThumbnail'):
                metadata_text += f"• {key}: {value}\n"
        
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
                f"• Deep learning model detected manipulation patterns with "
                f"{analysis_result['confidence_score'] * 100:.1f}% confidence\n"
            )
        
        if forensic_result["anomalies"]:
            conclusion_text += "• Detected forensic anomalies:\n"
            for category, anomalies in forensic_result["anomalies"].items():
                for anomaly in anomalies:
                    conclusion_text += f"  - {anomaly}\n"
        
        pdf.chapter_body(conclusion_text)

    def _create_score_comparison_chart(
        self,
        analysis_result: Dict[str, Any],
        forensic_result: Dict[str, Any]
    ) -> str:
        """Create score comparison chart"""
        plt.figure(figsize=(10, 6))
        
        scores = {
            'Deepfake Detection': analysis_result['confidence_score'],
            'ELA Analysis': forensic_result['ela_analysis']['score'],
            'Compression': forensic_result['compression_analysis']['score'],
            'Noise Analysis': forensic_result['noise_analysis']['score']
        }
        
        plt.bar(scores.keys(), scores.values())
        plt.title('Analysis Scores Comparison')
        plt.ylabel('Score')
        plt.ylim(0, 1)
        
        # Save to bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        
        return buf

    def _create_noise_pattern_visualization(
        self,
        noise_analysis: Dict[str, Any]
    ) -> str:
        """Create noise pattern visualization"""
        plt.figure(figsize=(10, 6))
        
        stats = noise_analysis['channel_statistics']
        channels = ['Red', 'Green', 'Blue']
        
        x = range(len(channels))
        means = [stat['mean'] for stat in stats]
        stds = [stat['std'] for stat in stats]
        
        plt.errorbar(x, means, yerr=stds, fmt='o', capsize=5)
        plt.xticks(x, channels)
        plt.title('Noise Pattern Analysis by Color Channel')
        plt.ylabel('Noise Level')
        
        # Save to bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        
        return buf

    def _generate_report_summary(
        self,
        analysis_result: Dict[str, Any],
        forensic_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a summary of the report findings"""
        overall_score = (
            analysis_result["confidence_score"] + 
            forensic_result["forensic_score"]
        ) / 2
        
        return {
            "verdict": "LIKELY FAKE" if overall_score > 0.5 else "LIKELY GENUINE",
            "confidence": overall_score,
            "deepfake_score": analysis_result["confidence_score"],
            "forensic_score": forensic_result["forensic_score"],
            "num_anomalies": sum(
                len(anomalies) 
                for anomalies in forensic_result["anomalies"].values()
            ),
            "timestamp": datetime.now().isoformat()
        }
