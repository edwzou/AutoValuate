import tkinter as tk
from tkinter import ttk, messagebox
import sys

class VehicleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Price Predictor")
        self.root.geometry("300x330")
        self.root.configure(bg='#f0f0f0')
        
        # Variables to store user inputs
        self.city_var = tk.StringVar(value="calgary")
        self.make_var = tk.StringVar(value="toyota")
        self.model_var = tk.StringVar(value="corolla")
        self.model_year_var = tk.StringVar(value="2005")
        self.transmission_var = tk.StringVar(value="automatic")
        self.car_mileage_var = tk.StringVar(value="299999")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Vehicle Price Predictor", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input fields
        # City
        ttk.Label(main_frame, text="City:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(main_frame, textvariable=self.city_var, width=25).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Make
        ttk.Label(main_frame, text="Make:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(main_frame, textvariable=self.make_var, width=25).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Model
        ttk.Label(main_frame, text="Model:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(main_frame, textvariable=self.model_var, width=25).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Model Year
        ttk.Label(main_frame, text="Model Year:").grid(row=4, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(main_frame, textvariable=self.model_year_var, width=25).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Transmission
        ttk.Label(main_frame, text="Transmission:").grid(row=5, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        transmission_combo = ttk.Combobox(main_frame, textvariable=self.transmission_var, 
                                        values=["automatic", "manual"], width=22)
        transmission_combo.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Car Mileage
        ttk.Label(main_frame, text="Car Mileage (km):").grid(row=6, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Entry(main_frame, textvariable=self.car_mileage_var, width=25).grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Start Search", 
                  command=self.start_search).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Exit", 
                  command=self.exit_program).grid(row=0, column=1)
    
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
            'car_mileage': int(self.car_mileage_var.get())
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

def show_results(vehicle_info, lr_predicted_price, average_price, final_price, vehicles_found):
    """Show results in a popup window"""
    result_window = tk.Tk()
    result_window.title("Price Prediction Results")
    result_window.geometry("400x480")
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
    
    # Add buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=4, column=0, columnspan=2, pady=20)
    
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