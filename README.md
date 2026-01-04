# 💆‍♀️ Aura Derm - AI Skincare Advisor

An intelligent AI-powered skincare advisor application that analyzes your skin condition and provides personalized recommendations for products, ingredients, and diet.

## ✨ Features

- 🔐 **Secure Authentication** - Login system with user registration
- 📸 **Image Upload/Capture** - Upload photos or use your camera
- 🤖 **AI-Powered Analysis** - Detects skin conditions using deep learning
- 🧴 **Product Recommendations** - Personalized skincare product suggestions
- 🧪 **Active Ingredients** - Key acids and ingredients for your skin type
- 🥗 **Dietary Advice** - Foods to eat and avoid for better skin
- 📄 **PDF Prescriptions** - Downloadable reports with all recommendations
- 🎨 **Beautiful UI** - Modern, responsive design with gradient themes

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Poojasri06/Aura_derm.git
cd Aura_derm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run streamlit_app.py
```

4. Open your browser and navigate to:
```
http://localhost:8501
```

## 🔑 Default Login Credentials

### Admin Account
- **Username:** admin
- **Password:** admin123

### Demo Account
- **Username:** demo
- **Password:** demo123

## 📊 Skin Conditions Detected

The app can analyze and provide recommendations for:

1. **Acne** - Breakouts and blemishes
2. **Dark Spots** - Hyperpigmentation and uneven tone
3. **Pigmentation** - Skin discoloration issues
4. **Wrinkles** - Fine lines and aging signs

## 🛠️ Training Your Own Model (Optional)

If you want to train a custom skin classification model:

1. Organize your dataset in the following structure:
```
data set/
├── acne/
├── dark spots/
├── pigmentation/
└── wrinkles/
```

2. Run the training script:
```bash
python train_skin_model.py
```

3. The trained model will be saved to `models/skin_classifier.pth`

**Note:** The app works in demo mode without a trained model, using simulated predictions for demonstration purposes.

## 📁 Project Structure

```
Aura_derm/
├── streamlit_app.py      # Main application
├── main.py               # Model architecture
├── recommender.py        # Product recommendations
├── food_map.py          # Dietary recommendations
├── acid_map.py          # Active ingredient mapping
├── train_skin_model.py  # Model training script
├── config.yaml          # Authentication configuration
├── requirements.txt     # Python dependencies
├── logo.png            # Application logo
└── README.md           # This file
```

## 🎨 UI Features

- **Gradient Backgrounds** - Modern pink/rose gradient theme
- **Responsive Layout** - Works on desktop and mobile
- **Interactive Elements** - Hover effects and smooth transitions
- **Visual Feedback** - Clear indication of analysis progress
- **Confidence Metrics** - Bar charts showing prediction confidence

## 🔒 Security

- Passwords are hashed using bcrypt
- Session-based authentication
- Secure cookie management

## 📝 Creating New Users

1. Click the "Register" button in the sidebar
2. Enter username, full name, and password
3. Submit to create your account
4. Login with your new credentials

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is created for educational and demonstration purposes.

## 👩‍💻 Author

Made with 💗 by **Pooja**

---

**Aura Derm 2025** - Your personalized AI skincare companion
