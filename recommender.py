# D:/Aura_derm/app/recommender.py

def get_products(skin_issue):
    skin_issue = skin_issue.lower()

    recommendations = {
        "acne": [
            {"name": "Salicylic Acid Cleanser", "type": "Cleanser"},
            {"name": "Benzoyl Peroxide Gel", "type": "Spot Treatment"},
            {"name": "Niacinamide Serum", "type": "Serum"},
            {"name": "Oil-Free Moisturizer", "type": "Moisturizer"}
        ],
        "wrinkles": [
            {"name": "Retinol Serum", "type": "Serum"},
            {"name": "Peptide Cream", "type": "Night Cream"},
            {"name": "Hyaluronic Acid Moisturizer", "type": "Moisturizer"},
            {"name": "Broad Spectrum Sunscreen SPF 50", "type": "Sunscreen"}
        ],
        "dark spots": [
            {"name": "Kojic Acid Cream", "type": "Cream"},
            {"name": "Vitamin C Serum", "type": "Serum"},
            {"name": "Glycolic Acid Toner", "type": "Toner"},
            {"name": "Alpha Arbutin Gel", "type": "Gel"}
        ],
        "pigmentation": [
            {"name": "Niacinamide + Zinc Serum", "type": "Serum"},
            {"name": "Azelaic Acid Cream", "type": "Cream"},
            {"name": "Tranexamic Acid Solution", "type": "Serum"},
            {"name": "Licorice Root Extract Gel", "type": "Gel"}
        ]
    }

    return recommendations.get(skin_issue, [{"name": "No products found", "type": "N/A"}])
