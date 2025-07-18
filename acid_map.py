def get_acids_for_skin_problem(skin_problem):
    acids = {
        "acne": ["Salicylic Acid", "Niacinamide", "Tea Tree Oil"],
        "pigmentation": ["Kojic Acid", "Glycolic Acid", "Alpha Arbutin"],
        "wrinkles": ["Retinol", "Peptides", "Hyaluronic Acid"],
        "dark spots": ["Vitamin C", "Tranexamic Acid", "Licorice Extract"]
    }
    return acids.get(skin_problem.lower(), ["No specific acids found"])
