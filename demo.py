#!/usr/bin/env python3
"""
Demo script to test the Aura Derm skincare advisor functionality
This script demonstrates the core functionality without the authentication layer
"""

import torch
from torchvision import transforms
from PIL import Image
import io

# Import our modules
from main import SkinClassifier
from recommender import get_products
from food_map import get_diet
from acid_map import get_acids_for_skin_problem

# Class names
CLASS_NAMES = ['acne', 'dark spots', 'pigmentation', 'wrinkles']

def demo_prediction(class_index=0):
    """
    Demonstrate a prediction for a given skin condition
    """
    predicted_class = CLASS_NAMES[class_index]
    
    print("=" * 70)
    print(f"🎯 DETECTED SKIN CONCERN: {predicted_class.upper()}")
    print("=" * 70)
    print()
    
    # Get recommendations
    products = get_products(predicted_class)
    acids = get_acids_for_skin_problem(predicted_class)
    diet = get_diet(predicted_class)
    
    # Display products
    print("🧴 RECOMMENDED PRODUCTS:")
    print("-" * 70)
    for i, product in enumerate(products, 1):
        print(f"   {i}. {product}")
    print()
    
    # Display acids
    print("🧪 KEY ACTIVE INGREDIENTS:")
    print("-" * 70)
    for acid in acids:
        print(f"   💊 {acid}")
    print()
    
    # Display diet
    print("🥗 DIETARY RECOMMENDATIONS:")
    print("-" * 70)
    print("   ✅ Foods to Eat:")
    for food in diet['eat']:
        print(f"      • {food}")
    print()
    print("   ❌ Foods to Avoid:")
    for food in diet['avoid']:
        print(f"      • {food}")
    print()
    
    print("=" * 70)
    print()

def main():
    """
    Run demo for all skin conditions
    """
    print("\n" + "=" * 70)
    print("💆‍♀️ AURA DERM - AI SKINCARE ADVISOR DEMO")
    print("=" * 70)
    print()
    print("This demo shows the recommendations for each skin condition.")
    print()
    
    # Demo each skin condition
    for i, condition in enumerate(CLASS_NAMES):
        demo_prediction(i)
        if i < len(CLASS_NAMES) - 1:
            input("Press Enter to see next condition...")
            print("\n")
    
    print("✅ Demo completed successfully!")
    print("\nTo run the full application with UI:")
    print("   streamlit run streamlit_app.py")
    print("\nDefault login credentials:")
    print("   Username: admin  |  Password: admin123")
    print("   Username: demo   |  Password: demo123")
    print()

if __name__ == "__main__":
    main()
