# AutoValuate with Advanced AI Prompt Engineering

A sophisticated vehicle price prediction application that combines web scraping, machine learning, and advanced AI prompt engineering to provide accurate price estimates for used vehicles. AutoValuate scrapes real market data from Facebook Marketplace and uses linear regression along with comparable vehicle analysis, enhanced by sophisticated AI interactions through prompt engineering.

## 🚗 Features

- **Web Scraping**: Automatically scrapes vehicle listings from Facebook Marketplace
- **Machine Learning**: Uses linear regression to predict prices based on mileage
- **Advanced AI-Powered Analysis**: Leverages Groq's LLM with sophisticated prompt engineering
- **Enhanced User Interface**: Comprehensive Tkinter interface with prompt engineering controls
- **Comprehensive Results**: Displays multiple price predictions with detailed AI analysis
- **Data Validation**: Robust input validation and error handling
- **Real-time Data**: Uses current market data for accurate predictions
- **Prompt Engineering**: Advanced AI prompt optimization and customization

## 🧠 AI Prompt Engineering Features

### Core Capabilities
- **Structured Prompt Templates**: Pre-built templates for different analysis types
- **Context-Aware Prompts**: Market context, seasonal factors, and regional insights
- **Example-Based Learning**: Few-shot learning with relevant examples
- **Temperature Control**: Adjustable AI creativity levels (0.0 = precise, 1.0 = creative)
- **Dynamic Context Inclusion**: Smart context selection based on analysis type

### Prompt Types
1. **Vehicle Generation Analysis**: Determines vehicle generation with market context
2. **Price Analysis**: AI-powered pricing insights with market factors
3. **Market Insights**: Regional market dynamics and trends
4. **Condition Assessment**: Vehicle condition evaluation and pricing impact

### Context Enhancement
- **Seasonal Factors**: Weather impact, maintenance cycles, demand fluctuations
- **Market Conditions**: Economic indicators, supply chain, fuel prices
- **Regional Specifics**: Local preferences, economic factors, competition
- **Vehicle Specifics**: Reliability ratings, common issues, brand reputation

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

### Basic Usage
1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Enter vehicle details** in the enhanced GUI:
   - **City**: Location for marketplace search (e.g., "calgary")
   - **Make**: Vehicle manufacturer (e.g., "toyota")
   - **Model**: Vehicle model (e.g., "corolla")
   - **Model Year**: Year of manufacture (e.g., "2005")
   - **Transmission**: "automatic" or "manual"
   - **Car Mileage**: Current mileage in kilometers

### Advanced Prompt Engineering
3. **Configure AI parameters**:
   - **Include Market Context**: Enable/disable contextual analysis
   - **AI Creativity (Temperature)**: Adjust from precise (0.0) to creative (1.0)
   - **Custom Prompt**: Add your own prompt modifications

4. **Preview Generated Prompts**:
   - Click "Preview Generation Prompt" to see the AI prompt for vehicle generation
   - Click "Preview Price Analysis Prompt" to see the pricing analysis prompt
   - Click "Preview Market Insights Prompt" to see the market analysis prompt

5. **Save/Load Settings**:
   - Save your prompt engineering preferences for future use
   - Load previously saved configurations

6. **Click "Start Search with Enhanced AI"** to begin the analysis

### Results Display
7. **View comprehensive results** including:
   - **Vehicle Information**: Basic vehicle details
   - **Price Predictions**: Linear regression and comparable analysis
   - **AI-Powered Analysis**: Enhanced insights using prompt engineering
   - **Market Insights**: Regional market factors and trends
   - **Data Analysis**: Number of vehicles found and analyzed

## 🔧 How It Works

### 1. Enhanced Data Collection
- Scrapes Facebook Marketplace for vehicle listings matching your criteria
- Extracts prices, mileage, location, and vehicle details
- Filters out invalid or placeholder listings

### 2. Advanced AI Analysis with Prompt Engineering
- **Structured Prompts**: Uses carefully crafted system and user prompts
- **Context Integration**: Incorporates market, seasonal, and regional factors
- **Example-Based Learning**: Provides relevant examples for better AI responses
- **Dynamic Optimization**: Adjusts prompts based on analysis type and context

### 3. Sophisticated Price Prediction
- **Linear Regression**: Predicts price based on mileage trends
- **Comparable Analysis**: Calculates average price of similar vehicles (±20,000 km)
- **AI Enhancement**: Additional insights from LLM analysis
- **Final Prediction**: Combines all methods for optimal accuracy

### 4. Enhanced Results Display
- Shows detailed breakdown of all predictions
- Displays AI-generated insights and market analysis
- Provides comprehensive vehicle assessment
- Option to start new searches with different parameters

## 📁 Project Structure

```
AutoValuate/
├── main.py              # Main application logic with enhanced AI
├── ui.py                # Enhanced UI with prompt engineering controls
├── prompt_config.json   # Advanced prompt engineering configuration
├── README.md            # This comprehensive documentation
└── .env                 # Environment variables (create this)
```

## 🧠 Prompt Engineering Architecture

### Template System
- **Modular Design**: Separate templates for different analysis types
- **Variable Substitution**: Dynamic prompt generation based on user input
- **Context Selection**: Smart inclusion of relevant market factors
- **Example Integration**: Few-shot learning with curated examples

### Context Enhancement
- **Multi-Layer Context**: Market, seasonal, regional, and vehicle-specific factors
- **Adaptive Inclusion**: Context selection based on analysis requirements
- **Quality Metrics**: Built-in validation and improvement tracking
- **Optimization Rules**: Configurable strategies for different use cases

### Configuration Management
- **JSON-Based Config**: Easy modification of prompts and settings
- **User Preferences**: Saveable prompt engineering configurations
- **Template Versioning**: Track changes and improvements over time
- **Quality Assurance**: Built-in validation and error handling

## 🔍 Technical Details

### Dependencies
- **selenium**: Web scraping automation
- **beautifulsoup4**: HTML parsing
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning (linear regression)
- **groq**: AI/LLM integration with advanced prompting
- **tkinter**: Enhanced GUI framework with prompt controls
- **matplotlib**: Data visualization (if needed)

### Key Components

#### `main.py`
- Orchestrates the entire prediction process
- Integrates enhanced prompt engineering with AI analysis
- Handles web scraping, data processing, and ML predictions
- Manages multiple AI analysis types

#### `ui.py`
- `PromptEngineering` class: Advanced prompt template management
- `VehicleUI` class: Enhanced input interface with prompt controls
- `show_results()` function: Comprehensive results display
- Input validation and error handling

#### `prompt_config.json`
- Comprehensive prompt engineering configuration
- Template definitions with examples and context rules
- Optimization strategies and quality metrics
- Context enhancement specifications

## ⚠️ Important Notes

- **Facebook Marketplace**: The application scrapes Facebook Marketplace. Changes to Facebook's HTML structure may require updates to the scraping logic.
- **API Limits**: Groq API has rate limits. For heavy usage, consider implementing rate limiting.
- **Headless Mode**: The browser runs in headless mode by default for better performance.
- **Data Accuracy**: Predictions are based on current market data and may vary by location and time.
- **Prompt Engineering**: Advanced prompts require careful tuning for optimal results.

## 🐛 Troubleshooting

### Common Issues

1. **ChromeDriver Issues**:
   - The application automatically downloads ChromeDriver
   - Ensure Chrome browser is installed and up to date

2. **API Key Errors**:
   - Verify your Groq API key is correctly set in `.env`
   - Check that the API key has sufficient credits

3. **Prompt Engineering Issues**:
   - Verify prompt configuration file is valid JSON
   - Check temperature settings (0.0-1.0 range)
   - Ensure context inclusion settings are appropriate

4. **No Results Found**:
   - Try different search parameters
   - Check internet connection
   - Verify the vehicle make/model spelling
   - Adjust prompt engineering parameters

5. **GUI Not Displaying**:
   - Ensure tkinter is installed: `python -m tkinter`
   - On Linux, you may need: `sudo apt-get install python3-tk`

## 📊 Example Output

The enhanced application provides comprehensive results including:
- Vehicle information summary
- Linear regression prediction
- Average comparable price
- Final predicted price
- AI-powered price analysis
- Market insights and trends
- Number of vehicles analyzed
- Prompt engineering configuration used

## 🚀 Advanced Usage

### Custom Prompt Development
1. **Modify Templates**: Edit `prompt_config.json` to customize prompts
2. **Add Context Factors**: Include new market or regional considerations
3. **Optimize Examples**: Improve few-shot learning with better examples
4. **Temperature Tuning**: Experiment with different creativity levels

### Batch Processing
- Save multiple prompt configurations for different analysis types
- Use different temperature settings for various scenarios
- Implement automated prompt optimization based on results

### Quality Improvement
- Monitor response quality metrics
- Track context utilization effectiveness
- Optimize token usage vs. information provided
- Implement feedback loops for continuous improvement

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug reports and feature requests
- Prompt engineering improvements
- New analysis types and templates
- UI/UX enhancements
- Documentation updates

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Facebook Marketplace for providing vehicle listing data
- Groq for AI/LLM capabilities and API access
- The open-source community for the libraries used in this project
- Contributors to prompt engineering research and best practices

---

**Note**: This application is for educational and informational purposes. Always verify prices through multiple sources before making purchasing decisions. The AI analysis should be used as a supplement to, not a replacement for, professional vehicle appraisal services.
