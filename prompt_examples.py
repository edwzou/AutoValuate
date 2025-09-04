#!/usr/bin/env python3
"""
Prompt Engineering Examples for AutoValuate
This script demonstrates the advanced prompt engineering capabilities
"""

from ui import PromptEngineering
import json

def demonstrate_prompt_engineering():
    """Demonstrate various prompt engineering features"""
    
    print("🚗 AutoValuate Prompt Engineering Examples\n")
    
    # Initialize the prompt engineer
    prompt_engineer = PromptEngineering()
    
    # Example 1: Vehicle Generation Analysis
    print("1️⃣ Vehicle Generation Analysis")
    print("=" * 50)
    
    generation_prompt = prompt_engineer.get_enhanced_generation_prompt(
        make="toyota", model="corolla", year="2005", city="calgary"
    )
    
    print("System Prompt:")
    print(generation_prompt['system'])
    print("\nUser Prompt:")
    print(generation_prompt['user'])
    print(f"\nParameters: Temperature={generation_prompt['temperature']}, Max Tokens={generation_prompt['max_tokens']}")
    
    # Example 2: Price Analysis
    print("\n\n2️⃣ Price Analysis")
    print("=" * 50)
    
    price_prompt = prompt_engineer.get_price_analysis_prompt(
        make="honda", model="civic", year="2010", mileage=150000, city="toronto"
    )
    
    print("System Prompt:")
    print(price_prompt['system'])
    print("\nUser Prompt:")
    print(price_prompt['user'])
    print(f"\nParameters: Temperature={price_prompt['temperature']}, Max Tokens={price_prompt['max_tokens']}")
    
    # Example 3: Market Insights
    print("\n\n3️⃣ Market Insights")
    print("=" * 50)
    
    market_prompt = prompt_engineer.get_market_insights_prompt(
        make="ford", model="f-150", city="edmonton"
    )
    
    print("System Prompt:")
    print(market_prompt['system'])
    print("\nUser Prompt:")
    print(market_prompt['user'])
    print(f"\nParameters: Temperature={market_prompt['temperature']}, Max Tokens={market_prompt['max_tokens']}")
    
    # Example 4: Custom Temperature Settings
    print("\n\n4️⃣ Custom Temperature Settings")
    print("=" * 50)
    
    # High precision (low temperature)
    precise_prompt = prompt_engineer.build_prompt(
        'vehicle_generation', 
        {'year': '2015', 'make': 'bmw', 'model': '3-series', 'city': 'vancouver'},
        include_context=True,
        temperature=0.0
    )
    
    print("High Precision (Temperature=0.0):")
    print(f"Temperature: {precise_prompt['temperature']}")
    print("Best for: Factual information, exact answers")
    
    # Balanced (medium temperature)
    balanced_prompt = prompt_engineer.build_prompt(
        'price_analysis',
        {'year': '2015', 'make': 'bmw', 'model': '3-series', 'mileage': '80000', 'city': 'vancouver'},
        include_context=True,
        temperature=0.3
    )
    
    print("\nBalanced (Temperature=0.3):")
    print(f"Temperature: {balanced_prompt['temperature']}")
    print("Best for: Balanced analysis, market insights")
    
    # Creative (high temperature)
    creative_prompt = prompt_engineer.build_prompt(
        'market_insights',
        {'make': 'bmw', 'model': '3-series', 'city': 'vancouver'},
        include_context=True,
        temperature=0.8
    )
    
    print("\nCreative (Temperature=0.8):")
    print(f"Temperature: {creative_prompt['temperature']}")
    print("Best for: Creative insights, trend analysis")
    
    # Example 5: Context Enhancement
    print("\n\n5️⃣ Context Enhancement")
    print("=" * 50)
    
    print("Available Context Types:")
    for context_type, factors in prompt_engineer.context_enhancers.items():
        print(f"\n{context_type.replace('_', ' ').title()}:")
        for factor in factors:
            print(f"  • {factor}")
    
    # Example 6: Template Customization
    print("\n\n6️⃣ Template Customization")
    print("=" * 50)
    
    print("Available Templates:")
    for template_name in prompt_engineer.prompt_templates.keys():
        template = prompt_engineer.prompt_templates[template_name]
        print(f"\n{template_name.replace('_', ' ').title()}:")
        print(f"  Context Importance: {template.get('context_importance', 'N/A')}")
        print(f"  Max Tokens: {template.get('max_tokens', 'N/A')}")
        print(f"  Examples: {len(template.get('examples', []))}")

def demonstrate_config_loading():
    """Demonstrate loading configuration from file"""
    
    print("\n\n7️⃣ Configuration Loading")
    print("=" * 50)
    
    try:
        with open('prompt_config.json', 'r') as f:
            config = json.load(f)
        
        print("Configuration loaded successfully!")
        print(f"Number of prompt templates: {len(config['prompt_templates'])}")
        print(f"Number of context enhancers: {len(config['context_enhancers'])}")
        
        print("\nAvailable prompt types:")
        for template_name in config['prompt_templates'].keys():
            print(f"  • {template_name}")
            
    except FileNotFoundError:
        print("Configuration file not found. Run the main application first to generate it.")
    except json.JSONDecodeError:
        print("Configuration file is invalid JSON.")

if __name__ == "__main__":
    try:
        demonstrate_prompt_engineering()
        demonstrate_config_loading()
        
        print("\n\n✅ Prompt Engineering Examples Completed!")
        print("\nTo use these features in the main application:")
        print("1. Run: python main.py")
        print("2. Configure prompt engineering settings in the UI")
        print("3. Preview generated prompts before running analysis")
        print("4. Save your preferred settings for future use")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have the required dependencies installed:")
        print("pip install groq python-dotenv")
