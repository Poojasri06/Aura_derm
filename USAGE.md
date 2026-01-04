# Aura Derm - Usage Guide

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Poojasri06/Aura_derm.git
cd Aura_derm

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

```bash
# Start the Streamlit application
streamlit run streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`

### 3. Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Demo Account:**
- Username: `demo`
- Password: `demo123`

## 📱 Using the Application

### Step 1: Login
1. Enter your username and password
2. Click the "Login" button
3. You'll be redirected to the upload page

### Step 2: Upload or Capture Image
1. Choose between uploading an image or using your camera
2. **Upload Option**: Click "Browse files" and select a clear face photo
3. **Camera Option**: Allow camera access and take a photo
4. Click "Analyze My Skin" button

### Step 3: View Results
The application will analyze your image and display:
- **Detected Skin Concern**: The primary skin issue identified
- **Recommended Products**: Specific skincare products for your condition
- **Key Active Ingredients**: Important acids and compounds to look for
- **Dietary Recommendations**: Foods to eat and avoid
- **Confidence Chart**: Visual representation of the analysis confidence

### Step 4: Download Prescription
1. Click "Generate PDF" button
2. A downloadable PDF prescription will be created
3. Click "Download PDF" to save it to your device

### Step 5: Analyze Another Image
Click "Analyze Another Image" to go back and upload a new photo

## 🎨 Features Overview

### ✨ AI-Powered Analysis
The application uses a deep learning model to analyze skin conditions. The current implementation includes:
- **4 Skin Conditions**: Acne, Dark Spots, Pigmentation, Wrinkles
- **Demo Mode**: When no trained model is available, uses simulated predictions for demonstration

### 🧴 Personalized Recommendations
Each skin condition comes with:
- 5 specific product recommendations with types
- 3-4 key active ingredients to look for
- Customized dietary advice (foods to eat and avoid)

### 📄 PDF Prescriptions
Generated prescriptions include:
- User information and date/time
- Detected skin condition
- All recommendations (products, ingredients, diet)
- Confidence chart showing prediction probabilities

### 🔐 User Management
- Secure authentication with bcrypt password hashing
- User registration capability
- Session-based authentication with cookies

## 🎯 Demo Mode

To test the core functionality without the UI:

```bash
python demo.py
```

This will show you example recommendations for all four skin conditions.

## 📊 Skin Conditions Supported

### 1. Acne
**Symptoms**: Breakouts, pimples, blemishes
**Recommendations**:
- Salicylic Acid Cleanser
- Benzoyl Peroxide treatments
- Niacinamide serums
- Diet: Avoid dairy and sugar, eat zinc-rich foods

### 2. Dark Spots
**Symptoms**: Hyperpigmentation, uneven skin tone
**Recommendations**:
- Vitamin C Serum
- Kojic Acid Cream
- Glycolic Acid Toner
- Diet: Eat citrus fruits, avoid sugary drinks

### 3. Pigmentation
**Symptoms**: Skin discoloration, melasma
**Recommendations**:
- Niacinamide + Zinc Serum
- Azelaic Acid Cream
- Tranexamic Acid Solution
- Diet: Eat carrots and spinach, avoid soda

### 4. Wrinkles
**Symptoms**: Fine lines, aging signs, loss of elasticity
**Recommendations**:
- Retinol Serum
- Peptide Cream
- Hyaluronic Acid Moisturizer
- Diet: Eat omega-3 rich foods, avoid alcohol

## 🛠️ Training Your Own Model

If you want to train a custom model with your own dataset:

### 1. Prepare Dataset
Organize images in this structure:
```
data set/
├── acne/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── dark spots/
│   └── ...
├── pigmentation/
│   └── ...
└── wrinkles/
    └── ...
```

### 2. Run Training
```bash
python train_skin_model.py
```

### 3. Model Location
The trained model will be saved to:
```
models/skin_classifier.pth
```

## ⚙️ Configuration

### config.yaml
Contains authentication settings:
- User credentials (username, name, hashed password)
- Cookie configuration
- Session settings

### Adding New Users Programmatically
```python
import bcrypt
import yaml

# Generate password hash
password = "newpassword"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Add to config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

config["credentials"]["usernames"]["newuser"] = {
    "email": "user@example.com",
    "name": "New User",
    "password": hashed
}

with open("config.yaml", "w") as f:
    yaml.dump(config, f)
```

## 🐛 Known Issues & Troubleshooting

### Issue: "Model file not found" warning
**Solution**: This is expected if you haven't trained a model yet. The app will run in demo mode with simulated predictions.

### Issue: Login not working
**Solution**: 
1. Ensure config.yaml exists with correct user credentials
2. Clear browser cookies and try again
3. Check that password hashes are correctly formatted

### Issue: Camera not working
**Solution**:
1. Grant camera permissions in your browser
2. Use HTTPS or localhost (required by browsers for camera access)
3. Try the upload option instead

### Issue: PDF generation fails
**Solution**:
1. Ensure the `prescriptions/` directory exists
2. Check write permissions
3. Verify fpdf is installed correctly

## 📝 Tips for Best Results

1. **Image Quality**: Use clear, well-lit photos for better analysis
2. **Face Position**: Ensure your face is centered and fully visible
3. **Lighting**: Natural daylight provides the best results
4. **Distance**: Take photos from a comfortable distance (not too close)
5. **Clean Skin**: Analyze bare skin without makeup for accurate results

## 🔒 Security Notes

- Passwords are hashed using bcrypt (never stored in plain text)
- Session cookies expire after 30 days
- User data is stored locally in config.yaml
- No external data transmission (all processing is local)

## 🆘 Getting Help

If you encounter issues:
1. Check the console/terminal for error messages
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Ensure Python 3.8+ is being used
4. Try running the demo script to test core functionality
5. Check the GitHub repository for updates

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the README.md for setup instructions

---

Made with 💗 by Pooja • Aura Derm 2025
