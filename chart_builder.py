"""
Chart Builder Module for Nutrition App
Creates radar (spider web) charts from scale responses.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
import os


class ChartBuilder:
    """Creates radar (spider web) charts from scale responses."""
    
    def __init__(self, output_dir: str = "charts"):
        """
        Initialize ChartBuilder.
        
        Args:
            output_dir (str): Directory to save chart images
        """
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Set matplotlib backend for Windows compatibility
        plt.switch_backend('Agg')
    
    def build_radar_chart(self, 
                         scale_responses: Dict[str, int], 
                         output_path: str,
                         title: str = "Health & Fitness Assessment",
                         max_scale: int = 10) -> str:
        """
        Create a radar chart from scale responses.
        
        Args:
            scale_responses: Dictionary of scale responses (1-10)
            output_path: Path to save the chart image
            title: Chart title
            max_scale: Maximum value on the scale
            
        Returns:
            Path to the saved chart image
        """
        try:
            self.logger.info(f"Creating radar chart: {title}")
            
            # Prepare data
            if not scale_responses:
                return self._create_empty_chart(output_path, title)
            
            categories = list(scale_responses.keys())
            values = list(scale_responses.values())
            
            # Clean up category names for display
            display_categories = [self._format_category_name(cat) for cat in categories]
            
            # Validate values
            values = [max(1, min(max_scale, v)) for v in values]
            
            # Create radar chart
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
            
            # Calculate angles for each category
            N = len(categories)
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]  # Complete the circle
            
            # Add values to complete the circle
            values += values[:1]
            
            # Plot the radar chart
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            
            # Draw the plot
            ax.plot(angles, values, 'o-', linewidth=2, label='Your Scores', color='#2E86AB')
            ax.fill(angles, values, alpha=0.25, color='#2E86AB')
            
            # Add category labels
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(display_categories, fontsize=11, fontweight='bold')
            
            # Set y-axis limits and labels
            ax.set_ylim(0, max_scale)
            ax.set_yticks(range(0, max_scale + 1, 2))
            ax.set_yticklabels([str(i) for i in range(0, max_scale + 1, 2)], fontsize=9)
            ax.grid(True, alpha=0.3)
            
            # Add title
            plt.title(title, size=16, fontweight='bold', pad=20)
            
            # Add score annotations
            for angle, value, category in zip(angles[:-1], values[:-1], display_categories):
                ax.annotate(f'{value}', 
                           xy=(angle, value), 
                           xytext=(5, 5), 
                           textcoords='offset points',
                           fontsize=10, 
                           fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
            
            # Add a legend
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            
            # Style improvements
            ax.spines['polar'].set_visible(False)
            ax.set_facecolor('#f8f9fa')
            
            # Save the chart
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            plt.close()
            
            self.logger.info(f"Radar chart saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating radar chart: {str(e)}")
            return self._create_empty_chart(output_path, title)
    
    def build_progress_chart(self, 
                            data: Dict[str, List[float]], 
                            output_path: str,
                            title: str = "Progress Tracking") -> str:
        """
        Create a line chart for progress tracking.
        
        Args:
            data: Dictionary with metric names and list of values over time
            output_path: Path to save the chart
            title: Chart title
            
        Returns:
            Path to the saved chart image
        """
        try:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#4A90E2']
            
            for i, (metric, values) in enumerate(data.items()):
                weeks = list(range(1, len(values) + 1))
                color = colors[i % len(colors)]
                
                ax.plot(weeks, values, marker='o', linewidth=2, 
                       label=self._format_category_name(metric), color=color)
            
            ax.set_xlabel('Week', fontsize=12, fontweight='bold')
            ax.set_ylabel('Score', fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Progress chart saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating progress chart: {str(e)}")
            return self._create_empty_chart(output_path, title)
    
    def build_comparison_chart(self, 
                              current_scores: Dict[str, int],
                              target_scores: Dict[str, int],
                              output_path: str,
                              title: str = "Current vs Target Scores") -> str:
        """
        Create a comparison radar chart showing current vs target scores.
        
        Args:
            current_scores: Current scale responses
            target_scores: Target scale responses
            output_path: Path to save the chart
            title: Chart title
            
        Returns:
            Path to the saved chart image
        """
        try:
            # Ensure both dictionaries have the same keys
            all_categories = set(current_scores.keys()) | set(target_scores.keys())
            categories = sorted(list(all_categories))
            
            current_values = [current_scores.get(cat, 0) for cat in categories]
            target_values = [target_scores.get(cat, 0) for cat in categories]
            
            display_categories = [self._format_category_name(cat) for cat in categories]
            
            # Create radar chart
            fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
            
            N = len(categories)
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]
            
            current_values += current_values[:1]
            target_values += target_values[:1]
            
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            
            # Plot both current and target
            ax.plot(angles, current_values, 'o-', linewidth=2, 
                   label='Current Scores', color='#2E86AB')
            ax.fill(angles, current_values, alpha=0.15, color='#2E86AB')
            
            ax.plot(angles, target_values, 's-', linewidth=2, 
                   label='Target Scores', color='#F18F01')
            ax.fill(angles, target_values, alpha=0.15, color='#F18F01')
            
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(display_categories, fontsize=11, fontweight='bold')
            
            ax.set_ylim(0, 10)
            ax.set_yticks(range(0, 11, 2))
            ax.grid(True, alpha=0.3)
            
            plt.title(title, size=16, fontweight='bold', pad=20)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Comparison chart saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating comparison chart: {str(e)}")
            return self._create_empty_chart(output_path, title)
    
    def build_nutrition_breakdown_chart(self, 
                                       macros: Dict[str, float],
                                       output_path: str,
                                       title: str = "Daily Macronutrient Breakdown") -> str:
        """
        Create a pie chart for macronutrient breakdown.
        
        Args:
            macros: Dictionary with macronutrient percentages
            output_path: Path to save the chart
            title: Chart title
            
        Returns:
            Path to the saved chart image
        """
        try:
            # Default macros if none provided
            if not macros:
                macros = {"Protein": 25, "Carbs": 50, "Fats": 25}
            
            labels = list(macros.keys())
            sizes = list(macros.values())
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
            
            fig, ax = plt.subplots(figsize=(10, 8))
            
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors[:len(labels)],
                                             autopct='%1.1f%%', startangle=90, 
                                             textprops={'fontsize': 12, 'fontweight': 'bold'})
            
            # Beautify the pie chart
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Nutrition breakdown chart saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating nutrition breakdown chart: {str(e)}")
            return self._create_empty_chart(output_path, title)
    
    def _format_category_name(self, category: str) -> str:
        """Format category names for display."""
        # Replace underscores with spaces and title case
        formatted = category.replace('_', ' ').title()
        
        # Handle specific formatting cases
        formatting_map = {
            'Bmi': 'BMI',
            'Hr': 'HR',
            'Resting Heart Rate': 'Resting HR',
            'Body Fat': 'Body Fat %',
            'Activity Level': 'Activity'
        }
        
        for old, new in formatting_map.items():
            formatted = formatted.replace(old, new)
        
        return formatted
    
    def _create_empty_chart(self, output_path: str, title: str) -> str:
        """Create an empty placeholder chart when data is insufficient."""
        try:
            fig, ax = plt.subplots(figsize=(10, 8))
            
            ax.text(0.5, 0.5, 'No Data Available\nfor Chart Generation', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=16, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=1', facecolor='lightgray', alpha=0.8))
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_xticks([])
            ax.set_yticks([])
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating empty chart: {str(e)}")
            raise
    
    def create_sample_chart(self, output_path: str) -> str:
        """Create a sample radar chart for demonstration."""
        sample_data = {
            "fitness_level": 6,
            "energy_level": 7,
            "strength": 5,
            "endurance": 4,
            "flexibility": 3,
            "nutrition_knowledge": 8,
            "motivation": 9,
            "stress_management": 5
        }
        
        return self.build_radar_chart(
            sample_data, 
            output_path, 
            "Sample Health & Fitness Assessment"
        )


if __name__ == "__main__":
    # Test the chart builder
    logging.basicConfig(level=logging.INFO)
    
    print("Testing Chart Builder...")
    print("=" * 50)
    
    # Create test directory
    test_dir = "test_charts"
    os.makedirs(test_dir, exist_ok=True)
    
    chart_builder = ChartBuilder(test_dir)
    
    # Test data
    test_scales = {
        "fitness_level": 6,
        "energy_level": 7,
        "strength": 5,
        "endurance": 4,
        "flexibility": 3,
        "nutrition_knowledge": 8,
        "motivation": 9,
        "stress_management": 5
    }
    
    # Test radar chart
    print("Creating radar chart...")
    radar_path = chart_builder.build_radar_chart(
        test_scales, 
        os.path.join(test_dir, "test_radar_chart.png"),
        "Test Health Assessment"
    )
    print(f"✓ Radar chart created: {radar_path}")
    
    # Test progress chart
    print("Creating progress chart...")
    progress_data = {
        "fitness_level": [4, 5, 6, 7],
        "energy_level": [5, 6, 7, 8],
        "strength": [3, 4, 5, 6]
    }
    progress_path = chart_builder.build_progress_chart(
        progress_data,
        os.path.join(test_dir, "test_progress_chart.png"),
        "4-Week Progress"
    )
    print(f"✓ Progress chart created: {progress_path}")
    
    # Test nutrition breakdown
    print("Creating nutrition breakdown chart...")
    macros = {"Protein": 30, "Carbohydrates": 40, "Fats": 30}
    nutrition_path = chart_builder.build_nutrition_breakdown_chart(
        macros,
        os.path.join(test_dir, "test_nutrition_chart.png")
    )
    print(f"✓ Nutrition chart created: {nutrition_path}")
    
    print("\n✓ All chart tests completed successfully!")
