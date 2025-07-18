def get_recommendation(problem):
    data = {
        'Acne': {
            'avoid': ['Sugary foods', 'Dairy'],
            'eat': ['Zinc-rich foods', 'Green tea'],
            'products': ['Salicylic acid cleanser', 'Niacinamide serum'],
            'timing': 'Morning and Night'
        },
        'Pigmentation': {
            'avoid': ['Excessive sun', 'Fried foods'],
            'eat': ['Vitamin C', 'Papaya'],
            'products': ['Kojic acid cream', 'Vitamin C serum'],
            'timing': 'Night'
        },
        'Dark_Spots': {
            'avoid': ['Scrubbing', 'Picking skin'],
            'eat': ['Citrus fruits', 'Antioxidants'],
            'products': ['Retinol', 'Glycolic acid cream'],
            'timing': 'Night'
        },
        'Wrinkles': {
            'avoid': ['Smoking', 'Dehydration'],
            'eat': ['Omega-3', 'Hyaluronic acid rich foods'],
            'products': ['Retinoids', 'Peptides serum'],
            'timing': 'Night'
        }
    }
    return data.get(problem, {})
