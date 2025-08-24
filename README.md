# AutoValuate

A sophisticated vehicle price prediction application that combines web scraping, machine learning, and AI to provide accurate price estimates for used vehicles. AutoValuate scrapes real market data from Facebook Marketplace and uses linear regression along with comparable vehicle analysis to predict fair market values.

## 🚗 Features

- **Web Scraping**: Automatically scrapes vehicle listings from Facebook Marketplace
- **Machine Learning**: Uses linear regression to predict prices based on mileage
- **AI-Powered Analysis**: Leverages Groq's LLM to determine vehicle generations
- **User-Friendly GUI**: Clean Tkinter interface for easy data input
- **Comprehensive Results**: Displays multiple price predictions with detailed analysis
- **Data Validation**: Robust input validation and error handling
- **Real-time Data**: Uses current market data for accurate predictions

## 📋 Prerequisites

Before running AutoValuate, ensure you have the following installed:

- Python 3.7 or higher
- Google Chrome browser
- Internet connection for web scraping and AI API calls

## 🛠️ Installation

1. **Clone the repository** (if using git):
   ```bash
   git clone <repository-url>
   cd AutoValuate
   ```

2. **Install required dependencies**:
   ```bash
   pip install selenium webdriver-manager beautifulsoup4 pandas matplotlib groq python-dotenv scikit-learn numpy
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root and add your Groq API key:
   ```
   API_KEY=your_groq_api_key_here
   ```

   To get a Groq API key:
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up for an account
   - Generate an API key

## 🚀 Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Enter vehicle details** in the GUI:
   - **City**: Location for marketplace search (e.g., "calgary")
   - **Make**: Vehicle manufacturer (e.g., "toyota")
   - **Model**: Vehicle model (e.g., "corolla")
   - **Model Year**: Year of manufacture (e.g., "2005")
   - **Transmission**: "automatic" or "manual"
   - **Car Mileage**: Current mileage in kilometers

3. **Click "Start Search"** to begin the analysis

4. **View results** in the popup window showing:
   - Linear regression prediction
   - Average comparable price
   - Final predicted price
   - Number of vehicles found in analysis

## 🔧 How It Works

### 1. Data Collection
- Scrapes Facebook Marketplace for vehicle listings matching your criteria
- Extracts prices, mileage, location, and vehicle details
- Filters out invalid or placeholder listings

### 2. AI Analysis
- Uses Groq's LLM to determine the vehicle generation (year range)
- Filters comparable vehicles within the same generation

### 3. Price Prediction
- **Linear Regression**: Predicts price based on mileage trends
- **Comparable Analysis**: Calculates average price of similar vehicles (±20,000 km)
- **Final Prediction**: Combines both methods for optimal accuracy

### 4. Results Display
- Shows detailed breakdown of predictions
- Displays vehicle information and analysis statistics
- Provides option to start a new search

## 📁 Project Structure

```
AutoValuate/
├── main.py          # Main application logic
├── ui.py            # User interface components
├── README.md        # This file
└── .env             # Environment variables (create this)
```

## 🔍 Technical Details

### Dependencies
- **selenium**: Web scraping automation
- **beautifulsoup4**: HTML parsing
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning (linear regression)
- **groq**: AI/LLM integration
- **tkinter**: GUI framework
- **matplotlib**: Data visualization (if needed)

### Key Components

#### `main.py`
- Orchestrates the entire prediction process
- Handles web scraping, data processing, and ML predictions
- Integrates with UI components

#### `ui.py`
- `VehicleUI` class: Main input interface
- `show_results()` function: Results display
- Input validation and error handling

## ⚠️ Important Notes

- **Facebook Marketplace**: The application scrapes Facebook Marketplace. Changes to Facebook's HTML structure may require updates to the scraping logic.
- **API Limits**: Groq API has rate limits. For heavy usage, consider implementing rate limiting.
- **Headless Mode**: The browser runs in headless mode by default for better performance.
- **Data Accuracy**: Predictions are based on current market data and may vary by location and time.

## 🐛 Troubleshooting

### Common Issues

1. **ChromeDriver Issues**:
   - The application automatically downloads ChromeDriver
   - Ensure Chrome browser is installed and up to date

2. **API Key Errors**:
   - Verify your Groq API key is correctly set in `.env`
   - Check that the API key has sufficient credits

3. **No Results Found**:
   - Try different search parameters
   - Check internet connection
   - Verify the vehicle make/model spelling

4. **GUI Not Displaying**:
   - Ensure tkinter is installed: `python -m tkinter`
   - On Linux, you may need: `sudo apt-get install python3-tk`

## 📊 Example Output

The application provides detailed results including:
- Vehicle information summary
- Linear regression prediction
- Average comparable price
- Final predicted price
- Number of vehicles analyzed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Facebook Marketplace for providing vehicle listing data
- Groq for AI/LLM capabilities
- The open-source community for the libraries used in this project

---

**Note**: This application is for educational and informational purposes. Always verify prices through multiple sources before making purchasing decisions.
