# recommender.py

def get_products(skin_issue):
    """
    Get product recommendations for a specific skin issue.
    Returns a list of product strings.
    """
    skin_issue = skin_issue.lower()

    recommendations = {
        "acne": [
            "Salicylic Acid Cleanser (Cleanser)",
            "Benzoyl Peroxide Gel (Spot Treatment)",
            "Niacinamide Serum (Serum)",
            "Oil-Free Moisturizer (Moisturizer)",
            "Tea Tree Oil Spot Treatment"
        ],
        "wrinkles": [
            "Retinol Serum (Anti-Aging Serum)",
            "Peptide Cream (Night Cream)",
            "Hyaluronic Acid Moisturizer (Moisturizer)",
            "Broad Spectrum Sunscreen SPF 50 (Sunscreen)",
            "Vitamin E Oil (Nourishing Oil)"
        ],
        "dark spots": [
            "Kojic Acid Cream (Brightening Cream)",
            "Vitamin C Serum (Brightening Serum)",
            "Glycolic Acid Toner (Exfoliating Toner)",
            "Alpha Arbutin Gel (Spot Treatment)",
            "Niacinamide Serum (Skin Tone Corrector)"
        ],
        "pigmentation": [
            "Niacinamide + Zinc Serum (Treatment Serum)",
            "Azelaic Acid Cream (Pigmentation Cream)",
            "Tranexamic Acid Solution (Serum)",
            "Licorice Root Extract Gel (Soothing Gel)",
            "Vitamin C + Ferulic Acid Serum (Brightening Serum)"
        ]
    }

    return recommendations.get(skin_issue, ["Gentle Cleanser", "Basic Moisturizer", "Sunscreen SPF 30"])
