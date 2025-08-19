"""
GUI Module for Nutrition App
Tkinter-based GUI for user interaction.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import logging
from typing import Optional, Dict, Any
import json

# Import our custom modules
from pdf_parser import PDFParser
from llm_engine import LLMEngine
from report_generator import ReportGenerator
from chart_builder import ChartBuilder
import config


class AppGUI:
    """Tkinter-based GUI for user interaction."""
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Application state
        self.pdf_path = tk.StringVar()
        self.output_dir = tk.StringVar(value=config.OUTPUT_DIR)
        self.model_type = tk.StringVar(value="openrouter")
        self.api_key = tk.StringVar(value="")
        self.processing = False
        
        # Initialize components
        self.pdf_parser = None
        self.llm_engine = None
        self.report_generator = None
        self.chart_builder = None
        
        self.setup_gui()
        
    def setup_logging(self):
        """Set up logging for the application."""
        logging.basicConfig(
            level=getattr(logging, config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('nutrition_app.log'),
                logging.StreamHandler()
            ]
        )
        
    def setup_gui(self):
        """Set up the main GUI interface."""
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(config.WINDOW_SIZE)
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Nutrition & Training Plan Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        self.create_file_selection_section(main_frame, row=1)
        
        # Output directory section
        self.create_output_section(main_frame, row=2)
        
        # Model selection section
        self.create_model_section(main_frame, row=3)
        
        # API key section
        self.create_api_section(main_frame, row=4)
        
        # Control buttons
        self.create_control_section(main_frame, row=5)
        
        # Progress section
        self.create_progress_section(main_frame, row=6)
        
        # Log output section
        self.create_log_section(main_frame, row=7)
        
        # Status bar
        self.create_status_bar(main_frame, row=8)
        
    def create_file_selection_section(self, parent, row):
        """Create PDF file selection section."""
        # Label
        ttk.Label(parent, text="PDF Questionnaire:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=(10, 5)
        )
        
        # File path entry
        pdf_entry = ttk.Entry(parent, textvariable=self.pdf_path, width=50)
        pdf_entry.grid(row=row+1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Browse button
        browse_btn = ttk.Button(parent, text="Browse", command=self.browse_pdf_file)
        browse_btn.grid(row=row+1, column=2, sticky=tk.W)
        
        # File info label
        self.file_info_label = ttk.Label(parent, text="No file selected", foreground="gray")
        self.file_info_label.grid(row=row+2, column=0, columnspan=3, sticky=tk.W, pady=(5, 15))
        
    def create_output_section(self, parent, row):
        """Create output directory selection section."""
        # Label
        ttk.Label(parent, text="Output Directory:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=(15, 5)
        )
        
        # Directory path entry
        output_entry = ttk.Entry(parent, textvariable=self.output_dir, width=50)
        output_entry.grid(row=row+1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Browse button
        output_browse_btn = ttk.Button(parent, text="Browse", command=self.browse_output_dir)
        output_browse_btn.grid(row=row+1, column=2, sticky=tk.W)
        
        # Add spacing after output section
        ttk.Label(parent, text="").grid(row=row+2, column=0, pady=(0, 10))
        
    def create_model_section(self, parent, row):
        """Create LLM model selection section."""
        # Label
        ttk.Label(parent, text="AI Model:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=(15, 5)
        )
        
        # Model selection frame
        model_frame = ttk.Frame(parent)
        model_frame.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Radio buttons for model selection
        ttk.Radiobutton(model_frame, text="OpenRouter (Cloud)", 
                       variable=self.model_type, value="openrouter",
                       command=self.on_model_change).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        ttk.Radiobutton(model_frame, text="Local Model (Offline)", 
                       variable=self.model_type, value="local",
                       command=self.on_model_change).grid(row=0, column=1, sticky=tk.W)
        
        # Model info label
        self.model_info_label = ttk.Label(parent, text="Cloud-based AI model (requires internet)", 
                                         foreground="blue")
        self.model_info_label.grid(row=row+2, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
    def create_api_section(self, parent, row):
        """Create API key input section."""
        # Label
        self.api_label = ttk.Label(parent, text="OpenRouter API Key:", font=('Arial', 10, 'bold'))
        self.api_label.grid(row=row, column=0, sticky=tk.W, pady=(15, 5))
        
        # API key entry
        self.api_entry = ttk.Entry(parent, textvariable=self.api_key, show="*", width=50)
        self.api_entry.grid(row=row+1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # API help button
        api_help_btn = ttk.Button(parent, text="Help", command=self.show_api_help)
        api_help_btn.grid(row=row+1, column=2, sticky=tk.W)
        
        # API info label
        self.api_info_label = ttk.Label(parent, text="Get your API key from openrouter.ai", 
                                       foreground="blue")
        self.api_info_label.grid(row=row+2, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
    def create_control_section(self, parent, row):
        """Create control buttons section."""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=row, column=0, columnspan=3, pady=(25, 15))
        
        # Generate button
        self.generate_btn = ttk.Button(control_frame, text="Generate Reports", 
                                      command=self.start_processing, style='Accent.TButton')
        self.generate_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Test connection button
        self.test_btn = ttk.Button(control_frame, text="Test AI Connection", 
                                  command=self.test_ai_connection)
        self.test_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Open output button
        self.open_output_btn = ttk.Button(control_frame, text="Open Output Folder", 
                                         command=self.open_output_folder)
        self.open_output_btn.grid(row=0, column=2)
        
    def create_progress_section(self, parent, row):
        """Create progress indicator section."""
        # Progress label
        self.progress_label = ttk.Label(parent, text="Ready", font=('Arial', 10))
        self.progress_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(15, 5))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(parent, mode='indeterminate')
        self.progress_bar.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
    def create_log_section(self, parent, row):
        """Create log output section."""
        # Log label
        ttk.Label(parent, text="Processing Log:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=(15, 5)
        )
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(parent, height=8, width=70)
        self.log_text.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          pady=(0, 10))
        
        # Configure text area to expand with window
        parent.rowconfigure(row+1, weight=1)
        
    def create_status_bar(self, parent, row):
        """Create status bar."""
        self.status_label = ttk.Label(parent, text="Ready to process questionnaire", 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
    def browse_pdf_file(self):
        """Open file dialog to select PDF file."""
        file_path = filedialog.askopenfilename(
            title="Select PDF Questionnaire",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            self.pdf_path.set(file_path)
            file_size = os.path.getsize(file_path) / 1024  # Size in KB
            self.file_info_label.config(
                text=f"Selected: {os.path.basename(file_path)} ({file_size:.1f} KB)",
                foreground="green"
            )
            self.log_message(f"Selected PDF file: {file_path}")
            
    def browse_output_dir(self):
        """Open dialog to select output directory."""
        dir_path = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir.get()
        )
        
        if dir_path:
            self.output_dir.set(dir_path)
            self.log_message(f"Output directory set to: {dir_path}")
            
    def on_model_change(self):
        """Handle model selection change."""
        model = self.model_type.get()
        
        if model == "local":
            self.model_info_label.config(text="Local AI model (works offline, requires model file)")
            self.api_label.grid_remove()
            self.api_entry.grid_remove()
            self.api_info_label.grid_remove()
        else:
            self.model_info_label.config(text="Cloud-based AI model (requires internet)")
            self.api_label.grid()
            self.api_entry.grid()
            self.api_info_label.grid()
            
        self.log_message(f"Model selection changed to: {model}")
        
    def show_api_help(self):
        """Show API key help dialog."""
        help_text = """
OpenRouter API Key Help

1. Go to https://openrouter.ai
2. Sign up for an account
3. Navigate to your API Keys section
4. Generate a new API key
5. Copy and paste it in the API Key field

Note: You'll need credits in your OpenRouter account to use the service.
Alternative: Use local models for offline processing.
        """
        
        messagebox.showinfo("API Key Help", help_text.strip())
        
    def test_ai_connection(self):
        """Test AI model connection."""
        if self.processing:
            return
            
        def test_connection():
            try:
                self.update_status("Testing AI connection...")
                self.log_message("Testing AI connection...")
                
                # Initialize LLM engine
                api_key = self.api_key.get() if self.model_type.get() == "openrouter" else None
                llm_engine = LLMEngine(self.model_type.get(), api_key)
                
                # Run connection test
                if llm_engine.test_connection():
                    self.update_status("AI connection successful!")
                    self.log_message("✓ AI connection test passed")
                    messagebox.showinfo("Connection Test", "AI connection successful!")
                else:
                    self.update_status("AI connection failed")
                    self.log_message("✗ AI connection test failed")
                    messagebox.showwarning("Connection Test", "AI connection failed. Check your settings.")
                    
            except Exception as e:
                error_msg = f"Connection test error: {str(e)}"
                self.update_status("Connection test failed")
                self.log_message(f"✗ {error_msg}")
                messagebox.showerror("Connection Test", error_msg)
        
        threading.Thread(target=test_connection, daemon=True).start()
        
    def start_processing(self):
        """Start the report generation process."""
        if self.processing:
            return
            
        # Validate inputs
        if not self.pdf_path.get():
            messagebox.showerror("Error", "Please select a PDF questionnaire file.")
            return
            
        if not os.path.exists(self.pdf_path.get()):
            messagebox.showerror("Error", "Selected PDF file does not exist.")
            return
            
        if self.model_type.get() == "openrouter" and not self.api_key.get():
            messagebox.showerror("Error", "Please enter your OpenRouter API key.")
            return
            
        # Start processing in separate thread
        threading.Thread(target=self.process_questionnaire, daemon=True).start()
        
    def process_questionnaire(self):
        """Process the questionnaire and generate reports."""
        try:
            self.processing = True
            self.set_processing_state(True)
            
            # Initialize components
            self.initialize_components()
            
            # Step 1: Parse PDF
            self.update_status("Parsing PDF questionnaire...")
            self.log_message("Step 1: Parsing PDF questionnaire...")
            
            questionnaire_data = self.pdf_parser.parse()
            self.log_message("✓ PDF parsing completed")
            
            # Step 2: Generate chart
            self.update_status("Creating health assessment chart...")
            self.log_message("Step 2: Creating health assessment chart...")
            
            chart_path = None
            scale_responses = questionnaire_data.get('scale_responses', {})
            if scale_responses:
                chart_path = os.path.join(self.output_dir.get(), "health_assessment_chart.png")
                self.chart_builder.build_radar_chart(scale_responses, chart_path)
                self.log_message("✓ Health assessment chart created")
            else:
                self.log_message("⚠ No scale responses found for chart")
            
            # Step 3: Generate AI content
            self.update_status("Generating AI content...")
            self.log_message("Step 3: Generating AI content with LLM...")
            
            llm_content = {
                "summary": self.llm_engine.generate_summary_report(questionnaire_data),
                "training": self.llm_engine.generate_training_plan(questionnaire_data),
                "nutrition": self.llm_engine.generate_nutrition_plan(questionnaire_data)
            }
            self.log_message("✓ AI content generation completed")
            
            # Step 4: Generate reports
            self.update_status("Creating Word documents...")
            self.log_message("Step 4: Generating Word documents...")
            
            generated_reports = self.report_generator.generate_all_reports(
                questionnaire_data, llm_content, chart_path
            )
            
            # Success message
            self.update_status("Reports generated successfully!")
            self.log_message("✓ All reports generated successfully!")
            self.log_message(f"✓ Output saved to: {self.output_dir.get()}")
            
            # Show success dialog
            success_msg = f"Reports generated successfully!\n\nFiles created:\n"
            for report_type, path in generated_reports.items():
                filename = os.path.basename(path)
                success_msg += f"• {filename}\n"
            success_msg += f"\nLocation: {self.output_dir.get()}"
            
            messagebox.showinfo("Success", success_msg)
            
        except Exception as e:
            error_msg = f"Error processing questionnaire: {str(e)}"
            self.update_status("Processing failed")
            self.log_message(f"✗ {error_msg}")
            messagebox.showerror("Error", error_msg)
            
        finally:
            self.processing = False
            self.set_processing_state(False)
            
    def initialize_components(self):
        """Initialize processing components."""
        # Ensure output directory exists
        os.makedirs(self.output_dir.get(), exist_ok=True)
        
        # Initialize PDF parser
        self.pdf_parser = PDFParser(self.pdf_path.get())
        
        # Initialize LLM engine
        api_key = self.api_key.get() if self.model_type.get() == "openrouter" else None
        self.llm_engine = LLMEngine(self.model_type.get(), api_key)
        
        # Initialize report generator
        self.report_generator = ReportGenerator(
            templates_dir=config.TEMPLATES_DIR,
            output_dir=self.output_dir.get()
        )
        
        # Initialize chart builder
        self.chart_builder = ChartBuilder(output_dir=self.output_dir.get())
        
        # Create templates if they don't exist
        self.report_generator.create_sample_templates()
        
    def set_processing_state(self, processing: bool):
        """Set UI state for processing."""
        state = 'disabled' if processing else 'normal'
        
        self.generate_btn.config(state=state)
        self.test_btn.config(state=state)
        
        if processing:
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            
    def update_status(self, message: str):
        """Update status bar message."""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def log_message(self, message: str):
        """Add message to log output."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
        # Also log to file
        self.logger.info(message)
        
    def open_output_folder(self):
        """Open the output folder in file explorer."""
        output_path = self.output_dir.get()
        if os.path.exists(output_path):
            os.startfile(output_path)  # Windows-specific
        else:
            messagebox.showwarning("Warning", f"Output directory does not exist: {output_path}")
            
    def run(self):
        """Start the GUI application."""
        try:
            self.log_message("Nutrition & Training Plan Generator started")
            self.log_message(f"Output directory: {self.output_dir.get()}")
            self.log_message(f"Model type: {self.model_type.get()}")
            
            # Handle window closing
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Start the main loop
            self.root.mainloop()
            
        except Exception as e:
            self.logger.error(f"GUI error: {str(e)}")
            messagebox.showerror("Application Error", f"An error occurred: {str(e)}")
            
    def on_closing(self):
        """Handle application closing."""
        if self.processing:
            if messagebox.askokcancel("Quit", "Processing is in progress. Are you sure you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()


class CLIHandler:
    """Command-line interface handler for the application."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def run_cli(self, pdf_path: str, output_dir: str = None, model_type: str = "openrouter", 
                api_key: str = None):
        """
        Run the application in CLI mode.
        
        Args:
            pdf_path: Path to PDF questionnaire
            output_dir: Output directory for reports
            model_type: Type of LLM model to use
            api_key: API key for cloud models
        """
        try:
            print("Nutrition & Training Plan Generator - CLI Mode")
            print("=" * 50)
            
            # Set defaults
            if not output_dir:
                output_dir = config.OUTPUT_DIR
                
            # Validate inputs
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
                
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Initialize components
            print("Initializing components...")
            pdf_parser = PDFParser(pdf_path)
            llm_engine = LLMEngine(model_type, api_key)
            report_generator = ReportGenerator(config.TEMPLATES_DIR, output_dir)
            chart_builder = ChartBuilder(output_dir)
            
            # Create templates
            report_generator.create_sample_templates()
            
            # Process questionnaire
            print("1. Parsing PDF questionnaire...")
            questionnaire_data = pdf_parser.parse()
            print("✓ PDF parsing completed")
            
            print("2. Creating health assessment chart...")
            chart_path = None
            scale_responses = questionnaire_data.get('scale_responses', {})
            if scale_responses:
                chart_path = os.path.join(output_dir, "health_assessment_chart.png")
                chart_builder.build_radar_chart(scale_responses, chart_path)
                print("✓ Chart created")
            
            print("3. Generating AI content...")
            llm_content = {
                "summary": llm_engine.generate_summary_report(questionnaire_data),
                "training": llm_engine.generate_training_plan(questionnaire_data),
                "nutrition": llm_engine.generate_nutrition_plan(questionnaire_data)
            }
            print("✓ AI content generated")
            
            print("4. Creating Word documents...")
            generated_reports = report_generator.generate_all_reports(
                questionnaire_data, llm_content, chart_path
            )
            print("✓ Reports generated")
            
            print("\nSuccess! Files created:")
            for report_type, path in generated_reports.items():
                print(f"  • {os.path.basename(path)}")
            print(f"\nLocation: {output_dir}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            self.logger.error(f"CLI processing error: {str(e)}")
            raise


if __name__ == "__main__":
    import sys
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Check if CLI arguments provided
    if len(sys.argv) > 1:
        # CLI mode
        if len(sys.argv) < 2:
            print("Usage: python app_gui.py <pdf_path> [output_dir] [model_type] [api_key]")
            sys.exit(1)
            
        pdf_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        model_type = sys.argv[3] if len(sys.argv) > 3 else "openrouter"
        api_key = sys.argv[4] if len(sys.argv) > 4 else None
        
        cli = CLIHandler()
        cli.run_cli(pdf_path, output_dir, model_type, api_key)
    else:
        # GUI mode
        app = AppGUI()
        app.run()
