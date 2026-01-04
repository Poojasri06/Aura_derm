# food_map.py

def get_diet(skin_issue):
    skin_issue = skin_issue.lower()

    diet_map = {
        "acne": {
            "eat": ["Green leafy vegetables", "Berries", "Whole grains", "Zinc-rich foods"],
            "avoid": ["Sugar", "Dairy products", "Refined carbs", "Fast food"]
        },
        "wrinkles": {
            "eat": ["Blueberries", "Avocados", "Nuts", "Green tea"],
            "avoid": ["Red meat", "Alcohol", "Deep-fried snacks"]
        },
        "dark spots": {
            "eat": ["Citrus fruits", "Papaya", "Tomatoes", "Pumpkin seeds"],
            "avoid": ["Sugary drinks", "Greasy food", "Processed snacks"]
        },
        "pigmentation": {
            "eat": ["Carrots", "Spinach", "Almonds", "Sunflower seeds"],
            "avoid": ["Soda", "White bread", "Overcooked meat"]
        }
    }

    return diet_map.get(skin_issue, {"eat": ["No data"], "avoid": ["No data"]})