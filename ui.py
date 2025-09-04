import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import json

class PromptEngineering:
    """Advanced prompt engineering for AI interactions"""
    
    def __init__(self):
        self.prompt_templates = {
            'vehicle_generation': {
                'system': "You are an expert automotive analyst specializing in vehicle generations and model years. Provide accurate, concise information about vehicle generations.",
                'user_template': "What generation does a {year} {make} {model} belong to? Please answer with only the year range of the generation, e.g., '2000-2005'. If uncertain, provide the most likely range based on common knowledge.",
                'examples': [
                    {"input": "What generation does a 2005 Toyota Corolla belong to?", "output": "2003-2008"},
                    {"input": "What generation does a 2018 Honda Civic belong to?", "output": "2016-2021"}
                ]
            },
            'price_analysis': {
                'system': "You are a professional vehicle appraiser with expertise in market analysis. Analyze vehicle pricing factors and provide insights.",
                'user_template': "Analyze the pricing for a {year} {make} {model} with {mileage}km in {city}. Consider factors like market trends, location, and condition. Provide a brief analysis in 2-3 sentences.",
                'examples': [
                    {"input": "Analyze pricing for a 2010 Honda Civic with 150000km in Toronto", "output": "The 2010 Honda Civic is in the 8th generation (2006-2011), known for reliability. With 150,000km, this vehicle is in the mid-life range where depreciation typically stabilizes. Toronto's market tends to command higher prices due to urban demand and limited parking, suggesting a premium of 10-15% over rural areas."}
                ]
            },
            'market_insights': {
                'system': "You are a market research analyst specializing in automotive industry trends and regional market dynamics.",
                'user_template': "What are the key market factors affecting {make} {model} prices in {city}? Consider seasonal trends, supply/demand, and regional preferences.",
                'examples': [
                    {"input": "What affects Toyota Corolla prices in Calgary?", "output": "Calgary's Toyota Corolla market is influenced by the city's strong economy and preference for reliable vehicles. Winter conditions favor AWD/4WD models, while fuel efficiency remains important. Seasonal fluctuations occur with spring/summer typically showing 5-10% higher prices due to increased demand."}
                ]
            }
        }
        
        self.context_enhancers = {
            'seasonal_factors': [
                "Consider current season and its impact on vehicle demand",
                "Factor in seasonal maintenance requirements",
                "Account for weather-related market fluctuations"
            ],
            'market_conditions': [
                "Include current economic indicators",
                "Consider supply chain impacts",
                "Factor in fuel price trends"
            ],
            'regional_specifics': [
                "Account for local market preferences",
                "Consider regional economic factors",
                "Include local competition analysis"
            ]
        }
    
    def build_prompt(self, template_name, variables, include_context=True, temperature=0.3):
        """Build a structured prompt with context and examples"""
        if template_name not in self.prompt_templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.prompt_templates[template_name]
        
        # Build the main prompt
        user_prompt = template['user_template'].format(**variables)
        
        # Add context if requested
        if include_context:
            context_parts = []
            for context_type, factors in self.context_enhancers.items():
                context_parts.extend(factors)
            
            context_text = "Additional considerations:\n" + "\n".join(f"• {factor}" for factor in context_parts[:3])
            user_prompt += f"\n\n{context_text}"
        
        # Add examples if available
        if template.get('examples'):
            examples_text = "\n\nExamples:\n"
            for example in template['examples']:
                examples_text += f"Q: {example['input']}\nA: {example['output']}\n"
            user_prompt += examples_text
        
        return {
            'system': template['system'],
            'user': user_prompt,
            'temperature': temperature,
            'max_tokens': 200
        }
    
    def get_enhanced_generation_prompt(self, make, model, year, city):
        """Get enhanced generation prompt with market context"""
        variables = {
            'year': year,
            'make': make,
            'model': model,
            'city': city
        }
        return self.build_prompt('vehicle_generation', variables, include_context=True)
    
    def get_price_analysis_prompt(self, make, model, year, mileage, city):
        """Get price analysis prompt with market insights"""
        variables = {
            'year': year,
            'make': make,
            'model': model,
            'mileage': f"{mileage:,}",
            'city': city
        }
        return self.build_prompt('price_analysis', variables, include_context=True)
    
    def get_market_insights_prompt(self, make, model, city):
        """Get market insights prompt for regional analysis"""
        variables = {
            'make': make,
            'model': model,
            'city': city
        }
        return self.build_prompt('market_insights', variables, include_context=True)

class VehicleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Price Predictor with AI Prompt Engineering")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize prompt engineering
        self.prompt_engineer = PromptEngineering()
        
        # Variables to store user inputs
        self.city_var = tk.StringVar(value="calgary")
        self.make_var = tk.StringVar(value="toyota")
        self.model_var = tk.StringVar(value="corolla")
        self.model_year_var = tk.StringVar(value="2005")
        self.transmission_var = tk.StringVar(value="automatic")
        self.car_mileage_var = tk.StringVar(value="299999")
        
        # Prompt engineering variables
        self.include_context_var = tk.BooleanVar(value=True)
        self.temperature_var = tk.DoubleVar(value=0.3)
        self.custom_prompt_var = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame with scrollbar
        main_canvas = tk.Canvas(self.root, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Main frame
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Vehicle Price Predictor with AI Prompt Engineering", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Vehicle Information Section
        vehicle_frame = ttk.LabelFrame(main_frame, text="Vehicle Information", padding="15")
        vehicle_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Input fields
        # City
        ttk.Label(vehicle_frame, text="City:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(vehicle_frame, textvariable=self.city_var, width=25).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Make
        ttk.Label(vehicle_frame, text="Make:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(vehicle_frame, textvariable=self.make_var, width=25).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Model
        ttk.Label(vehicle_frame, text="Model:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(vehicle_frame, textvariable=self.model_var, width=25).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Model Year
        ttk.Label(vehicle_frame, text="Model Year:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(vehicle_frame, textvariable=self.model_year_var, width=25).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Transmission
        ttk.Label(vehicle_frame, text="Transmission:").grid(row=4, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        transmission_combo = ttk.Combobox(vehicle_frame, textvariable=self.transmission_var, 
                                        values=["automatic", "manual"], width=22)
        transmission_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Car Mileage
        ttk.Label(vehicle_frame, text="Car Mileage (km):").grid(row=5, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(vehicle_frame, textvariable=self.car_mileage_var, width=25).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Prompt Engineering Section
        prompt_frame = ttk.LabelFrame(main_frame, text="AI Prompt Engineering", padding="15")
        prompt_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Context inclusion
        ttk.Checkbutton(prompt_frame, text="Include Market Context", 
                       variable=self.include_context_var).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Temperature control
        ttk.Label(prompt_frame, text="AI Creativity (Temperature):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        temp_scale = ttk.Scale(prompt_frame, from_=0.0, to=1.0, variable=self.temperature_var, 
                              orient=tk.HORIZONTAL, length=200)
        temp_scale.grid(row=1, column=1, sticky=tk.W, pady=5)
        temp_label = ttk.Label(prompt_frame, text="0.0 = Precise, 1.0 = Creative")
        temp_label.grid(row=1, column=2, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Custom prompt
        ttk.Label(prompt_frame, text="Custom Prompt (Optional):").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        custom_prompt_entry = ttk.Entry(prompt_frame, textvariable=self.custom_prompt_var, width=50)
        custom_prompt_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Prompt Preview Section
        preview_frame = ttk.LabelFrame(main_frame, text="Generated Prompt Preview", padding="15")
        preview_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Preview buttons
        preview_buttons_frame = ttk.Frame(preview_frame)
        preview_buttons_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(preview_buttons_frame, text="Preview Generation Prompt", 
                  command=self.preview_generation_prompt).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(preview_buttons_frame, text="Preview Price Analysis Prompt", 
                  command=self.preview_price_prompt).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(preview_buttons_frame, text="Preview Market Insights Prompt", 
                  command=self.preview_market_prompt).grid(row=0, column=2)
        
        # Preview text area
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=8, width=70, wrap=tk.WORD)
        self.preview_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Start Search with Enhanced AI", 
                  command=self.start_search).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Save Prompt Settings", 
                  command=self.save_prompt_settings).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="Load Prompt Settings", 
                  command=self.load_prompt_settings).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(button_frame, text="Exit", 
                  command=self.exit_program).grid(row=0, column=3)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        prompt_frame.columnconfigure(1, weight=1)
        preview_frame.columnconfigure(1, weight=1)
        
        # Configure canvas
        main_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def preview_generation_prompt(self):
        """Preview the generation prompt"""
        try:
            variables = {
                'year': self.model_year_var.get(),
                'make': self.make_var.get(),
                'model': self.model_var.get(),
                'city': self.city_var.get()
            }
            
            prompt_data = self.prompt_engineer.get_enhanced_generation_prompt(
                variables['make'], variables['model'], variables['year'], variables['city']
            )
            
            preview_text = f"System Prompt:\n{prompt_data['system']}\n\n"
            preview_text += f"User Prompt:\n{prompt_data['user']}\n\n"
            preview_text += f"Parameters:\n• Temperature: {prompt_data['temperature']}\n• Max Tokens: {prompt_data['max_tokens']}"
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating preview: {str(e)}")
    
    def preview_price_prompt(self):
        """Preview the price analysis prompt"""
        try:
            variables = {
                'year': self.model_year_var.get(),
                'make': self.make_var.get(),
                'model': self.model_var.get(),
                'mileage': self.car_mileage_var.get(),
                'city': self.city_var.get()
            }
            
            prompt_data = self.prompt_engineer.get_price_analysis_prompt(
                variables['make'], variables['model'], variables['year'], 
                int(variables['mileage']), variables['city']
            )
            
            preview_text = f"System Prompt:\n{prompt_data['system']}\n\n"
            preview_text += f"User Prompt:\n{prompt_data['user']}\n\n"
            preview_text += f"Parameters:\n• Temperature: {prompt_data['temperature']}\n• Max Tokens: {prompt_data['max_tokens']}"
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating preview: {str(e)}")
    
    def preview_market_prompt(self):
        """Preview the market insights prompt"""
        try:
            variables = {
                'make': self.make_var.get(),
                'model': self.model_var.get(),
                'city': self.city_var.get()
            }
            
            prompt_data = self.prompt_engineer.get_market_insights_prompt(
                variables['make'], variables['model'], variables['city']
            )
            
            preview_text = f"System Prompt:\n{prompt_data['system']}\n\n"
            preview_text += f"User Prompt:\n{prompt_data['user']}\n\n"
            preview_text += f"Parameters:\n• Temperature: {prompt_data['temperature']}\n• Max Tokens: {prompt_data['max_tokens']}"
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating preview: {str(e)}")
    
    def save_prompt_settings(self):
        """Save current prompt engineering settings"""
        try:
            settings = {
                'include_context': self.include_context_var.get(),
                'temperature': self.temperature_var.get(),
                'custom_prompt': self.custom_prompt_var.get()
            }
            
            with open('prompt_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
            
            messagebox.showinfo("Success", "Prompt settings saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving settings: {str(e)}")
    
    def load_prompt_settings(self):
        """Load saved prompt engineering settings"""
        try:
            with open('prompt_settings.json', 'r') as f:
                settings = json.load(f)
            
            self.include_context_var.set(settings.get('include_context', True))
            self.temperature_var.set(settings.get('temperature', 0.3))
            self.custom_prompt_var.set(settings.get('custom_prompt', ''))
            
            messagebox.showinfo("Success", "Prompt settings loaded successfully!")
            
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved settings found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading settings: {str(e)}")
    
    def validate_inputs(self):
        """Validate all user inputs"""
        try:
            # Validate numeric inputs
            int(self.model_year_var.get())
            int(self.car_mileage_var.get())
            
            # Validate ranges
            year = int(self.model_year_var.get())
            if year < 1900 or year > 2025:
                raise ValueError("Model year must be between 1900 and 2025")
            
            mileage = int(self.car_mileage_var.get())
            if mileage < 0:
                raise ValueError("Car mileage cannot be negative")
            
            # Validate text inputs
            if not self.city_var.get().strip():
                raise ValueError("City cannot be empty")
            if not self.make_var.get().strip():
                raise ValueError("Make cannot be empty")
            if not self.model_var.get().strip():
                raise ValueError("Model cannot be empty")
            
            return True
        except ValueError as e:
            messagebox.showerror("Validation Error", f"Invalid input: {str(e)}")
            return False
    
    def get_settings(self):
        """Return current settings as a dictionary"""
        if not self.validate_inputs():
            return None
        
        return {
            'city': self.city_var.get().strip(),
            'make': self.make_var.get().strip(),
            'model': self.model_var.get().strip(),
            'model_year': int(self.model_year_var.get()),
            'transmission': self.transmission_var.get(),
            'car_mileage': int(self.car_mileage_var.get()),
            'prompt_engineering': {
                'include_context': self.include_context_var.get(),
                'temperature': self.temperature_var.get(),
                'custom_prompt': self.custom_prompt_var.get()
            }
        }
    
    def start_search(self):
        """Start the vehicle search with current settings"""
        settings = self.get_settings()
        if settings:
            self.root.quit()
            return settings
        return None
    
    def exit_program(self):
        """Exit the program completely"""
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

def show_results(vehicle_info, lr_predicted_price, average_price, final_price, vehicles_found, 
                ai_price_analysis=None, market_insights=None):
    """Show results in a popup window with AI analysis"""
    result_window = tk.Tk()
    result_window.title("Price Prediction Results with AI Analysis")
    result_window.geometry("600x700")
    result_window.configure(bg='#f0f0f0')
    
    # Center the window
    result_window.eval('tk::PlaceWindow . center')
    
    # Main frame
    main_frame = ttk.Frame(result_window, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Title
    title_label = ttk.Label(main_frame, text="PRICE PREDICTION RESULTS", 
                           font=('Arial', 16, 'bold'))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    # Vehicle info
    vehicle_frame = ttk.LabelFrame(main_frame, text="Vehicle Information", padding="10")
    vehicle_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
    
    ttk.Label(vehicle_frame, text=f"Vehicle: {vehicle_info['model_year']} {vehicle_info['make']} {vehicle_info['model']}", 
              font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=2)
    ttk.Label(vehicle_frame, text=f"Mileage: {vehicle_info['car_mileage']:,} km", 
              font=('Arial', 11)).grid(row=1, column=0, sticky=tk.W, pady=2)
    ttk.Label(vehicle_frame, text=f"Location: {vehicle_info['city']}", 
              font=('Arial', 11)).grid(row=2, column=0, sticky=tk.W, pady=2)
    
    # Results
    results_frame = ttk.LabelFrame(main_frame, text="Price Predictions", padding="10")
    results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
    
    ttk.Label(results_frame, text=f"Linear Regression Prediction: ${lr_predicted_price:,.2f}", 
              font=('Arial', 11)).grid(row=0, column=0, sticky=tk.W, pady=2)
    ttk.Label(results_frame, text=f"Average Comparable Price: ${average_price:,.2f}", 
              font=('Arial', 11)).grid(row=1, column=0, sticky=tk.W, pady=2)
    
    # Final price (highlighted)
    final_price_label = ttk.Label(results_frame, text=f"FINAL PREDICTED PRICE: ${final_price:,.2f}", 
                                 font=('Arial', 14, 'bold'), foreground='green')
    final_price_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
    
    # Data info
    info_frame = ttk.LabelFrame(main_frame, text="Data Analysis", padding="10")
    info_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
    
    ttk.Label(info_frame, text=f"Vehicles found: {vehicles_found}", 
              font=('Arial', 11)).grid(row=0, column=0, sticky=tk.W, pady=2)
    
    # AI Analysis Section (if available)
    if ai_price_analysis or market_insights:
        ai_frame = ttk.LabelFrame(main_frame, text="AI-Powered Analysis", padding="10")
        ai_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        if ai_price_analysis:
            ttk.Label(ai_frame, text="AI Price Analysis:", 
                      font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(5, 2))
            ai_analysis_label = ttk.Label(ai_frame, text=ai_price_analysis, 
                                         wraplength=500, justify=tk.LEFT)
            ai_analysis_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        if market_insights:
            ttk.Label(ai_frame, text="Market Insights:", 
                      font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(5, 2))
            market_insights_label = ttk.Label(ai_frame, text=market_insights, 
                                            wraplength=500, justify=tk.LEFT)
            market_insights_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
    
    # Add buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=5, column=0, columnspan=2, pady=20)
    
    def new_search():
        result_window.destroy()
        # Restart the application
        import subprocess
        import sys
        subprocess.Popen([sys.executable, 'main.py'])
        sys.exit(0)
    
    ttk.Button(button_frame, text="New Search", 
              command=new_search).grid(row=0, column=0, padx=(0, 10))
    ttk.Button(button_frame, text="Close", 
              command=result_window.destroy).grid(row=0, column=1)
    
    # Handle window close (X button) to only close this window
    def on_closing():
        result_window.destroy()
    
    result_window.protocol("WM_DELETE_WINDOW", on_closing)
    result_window.mainloop()

def run_ui():
    """Run the UI and return the settings"""
    root = tk.Tk()
    app = VehicleUI(root)
    root.mainloop()
    
    # Get settings after window is closed
    return app.get_settings()

if __name__ == "__main__":
    settings = run_ui()
    if settings:
        print("Settings:", settings)
    else:
        print("No settings returned") 