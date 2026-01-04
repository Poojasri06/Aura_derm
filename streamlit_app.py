import streamlit as st
import streamlit_authenticator as stauth
import torch
from torchvision import transforms
import yaml
from yaml.loader import SafeLoader
from PIL import Image
import os
import datetime
from fpdf import FPDF
import bcrypt
import matplotlib.pyplot as plt
import hashlib

# Custom imports
from main import SkinClassifier
from recommender import get_products
from food_map import get_diet
from acid_map import get_acids_for_skin_problem

# === Configuration ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")
MODEL_PATH = os.path.join(BASE_DIR, "models", "skin_classifier.pth")
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "prescriptions")
CLASS_NAMES = ['acne', 'dark spots', 'pigmentation', 'wrinkles']

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# === Load YAML Config ===
if not os.path.exists(CONFIG_PATH):
    st.error("Configuration file not found. Please ensure 'config.yaml' exists.")
    st.stop()

with open(CONFIG_PATH) as file:
    config = yaml.load(file, Loader=SafeLoader)

# === Initialize Authenticator ===
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# === Load Model ===
@st.cache_resource
def load_model():
    """Load the skin classification model"""
    if not os.path.exists(MODEL_PATH):
        st.warning("⚠️ Model file not found. Using demo mode with simulated predictions.")
        return None
    try:
        model = SkinClassifier()
        model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
        model.eval()
        return model
    except Exception as e:
        st.warning(f"⚠️ Error loading model: {e}. Using demo mode.")
        return None

model = load_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# === Session State Defaults ===
for key in ['authentication_status', 'page', 'user', 'image', 'prediction', 'register']:
    if key not in st.session_state:
        st.session_state[key] = None if key != 'register' else False
if st.session_state.page is None:
    st.session_state.page = 'login'

# === PDF Generator ===
def generate_pdf(predicted_class, products, acids, diet, username="user", probabilities=None):
    # === Setup filenames ===
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d_%H%M%S')
    filename = f"AuraDerm_{username}_{date_str}.pdf"
    path = os.path.join(DOWNLOAD_FOLDER, filename)
    
    # === Optional: Save bar chart of model probabilities ===
    chart_path = os.path.join(DOWNLOAD_FOLDER, f"chart_{date_str}.png")
    if probabilities:
        plt.figure(figsize=(6, 4))
        plt.bar(CLASS_NAMES, probabilities, color="#e75480")
        plt.xlabel("Skin Issues")
        plt.ylabel("Prediction Confidence")
        plt.title("Skin Issue Prediction Confidence")
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
    else:
        chart_path = None

    # === Generate PDF ===
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Aura Derm - Skin Analysis Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date: {now.strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"User: {username}", ln=True)
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt=f"Detected Skin Issue: {predicted_class.title()}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(5)

    for section, items in zip(
        ["Recommended Products", "Recommended Acids", "Foods to Eat", "Foods to Avoid"],
        [products, acids, diet['eat'], diet['avoid']]
    ):
        pdf.cell(200, 10, txt=section + ":", ln=True)
        for item in items:
            pdf.cell(200, 10, txt=f" - {item}", ln=True)
        pdf.ln(2)

    if chart_path and os.path.exists(chart_path):
        pdf.ln(5)
        pdf.cell(200, 10, txt="Prediction Confidence Chart:", ln=True)
        pdf.image(chart_path, x=10, y=None, w=180)
        
        # Clean up temporary chart file after adding to PDF
        try:
            os.remove(chart_path)
        except:
            pass  # Silently ignore if cleanup fails

    pdf.output(path)
    return path

# === Aesthetic Styling ===
st.set_page_config(page_title="Aura Derm - AI Skincare Advisor", page_icon="💆‍♀️", layout="wide")
st.markdown("""
    <style>
    /* Main background and layout */
    .main { 
        background: linear-gradient(135deg, #fff6f9 0%, #ffe4ec 100%);
    }
    
    /* Title styling */
    .title {
        font-size: 48px; 
        font-weight: 900; 
        color: #e91e63; 
        text-align: center;
        font-family: 'Trebuchet MS', sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 26px; 
        font-weight: bold; 
        color: #d6336c;
        margin-top: 25px; 
        margin-bottom: 15px; 
        font-family: 'Arial';
        border-left: 5px solid #ff69b4;
        padding-left: 15px;
    }
    
    /* Section cards */
    .section {
        background: linear-gradient(135deg, #ffffff 0%, #fff9fb 100%);
        padding: 20px 30px;
        border-radius: 20px; 
        box-shadow: 0 8px 20px rgba(233, 30, 99, 0.15);
        margin-bottom: 25px; 
        font-size: 18px;
        border: 1px solid rgba(255, 105, 180, 0.2);
        transition: transform 0.2s;
    }
    
    .section:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(233, 30, 99, 0.2);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
        color: white;
        border-radius: 15px; 
        font-size: 16px; 
        font-weight: 600;
        padding: 12px 30px;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff1493 0%, #c71585 100%);
        box-shadow: 0 6px 20px rgba(255, 105, 180, 0.4);
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #ffe4ec 0%, #fff0f5 100%);
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #ff69b4;
        border-radius: 15px;
        padding: 20px;
        background-color: #fff9fb;
    }
    
    /* Radio buttons */
    .stRadio > label {
        font-size: 18px;
        font-weight: 600;
        color: #d6336c;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 15px;
        border-left: 5px solid #ff69b4;
    }
    
    /* Image display */
    .stImage {
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Footer */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff69b4, transparent);
        margin: 40px 0 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# === Logo ===
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=250)
else:
    st.sidebar.title("Aura Derm")

# === Register Section ===
if st.session_state.register:
    st.markdown('<div class="title">📝 Register</div>', unsafe_allow_html=True)
    new_username = st.text_input("Username")
    new_name = st.text_input("Full Name")
    new_password = st.text_input("Password", type="password")
    if st.button("Register"):
        if new_username in config["credentials"]["usernames"]:
            st.error("Username already exists.")
        else:
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            config["credentials"]["usernames"][new_username] = {
                "name": new_name,
                "password": hashed_pw
            }
            with open(CONFIG_PATH, "w") as f:
                yaml.dump(config, f)
            st.success("✅ Registered Successfully! You can now log in.")
            st.session_state.register = False
else:
    st.sidebar.button("Register", on_click=lambda: st.session_state.update({"register": True}))

# === Login ===
if st.session_state.page == "login":
    st.markdown('<div class="title">💆‍♀️ Aura Derm</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 18px; color: #666; margin-bottom: 30px;">✨ Your AI-Powered Skincare Advisor ✨</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 16px; color: #888; margin-bottom: 30px;">Get personalized skincare recommendations based on AI analysis</p>', unsafe_allow_html=True)
    
    try:
        result = authenticator.login(location="main")
        if result is not None:
            name, auth_status, username = result
        else:
            name, auth_status, username = None, None, None
    except Exception as e:
        st.error(f"Login error: {e}")
        name, auth_status, username = None, False, None
    
    if auth_status:
        st.session_state.page = "upload"
        st.session_state.user = name
        st.rerun()
    elif auth_status is False:
        st.error("❌ Invalid username or password")
    elif auth_status is None:
        st.info("👋 Please enter your login credentials to continue")

# === Upload Page ===
elif st.session_state.page == "upload":
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"👤 Logged in as **{st.session_state.user}**")
    st.sidebar.markdown("---")
    st.sidebar.info("📸 **How to use:**\n\n1. Upload or capture an image\n2. Get AI-powered analysis\n3. Receive personalized recommendations\n4. Download your prescription")
    
    st.markdown('<div class="title">💆‍♀️ Upload or Capture Image</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 18px; color: #666; margin-bottom: 30px;">Upload a clear photo of your face for analysis</p>', unsafe_allow_html=True)
    
    input_method = st.radio("Select Image Input Method:", ['📄 Upload Image', '📸 Use Camera'], horizontal=True)
    
    image = None
    if input_method == "📄 Upload Image":
        uploaded = st.file_uploader("Choose a face image", type=["jpg", "jpeg", "png"], help="Upload a clear, well-lit photo of your face")
        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption="✅ Uploaded Image", width=400)
    else:
        cam = st.camera_input("📸 Take a clear face photo")
        if cam:
            image = Image.open(cam).convert("RGB")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption="✅ Captured Image", width=400)
    
    if image:
        st.session_state.image = image
        if st.button("🔍 Analyze My Skin", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()

# === Results Page ===
elif st.session_state.page == "results":
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"👤 Logged in as **{st.session_state.user}**")
    
    st.markdown('<div class="title">📊 Your Skin Analysis Results</div>', unsafe_allow_html=True)
    
    image = st.session_state.image
    
    # Display image in center
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Analyzed Image", width=400)
    
    # Predict skin condition
    probabilities = None
    output = None
    pred_class = None
    
    with st.spinner("🔬 Analyzing your skin..."):
        try:
            if model is not None:
                img_tensor = transform(image).unsqueeze(0)
                with torch.no_grad():
                    output = model(img_tensor)
                    _, pred = torch.max(output, 1)
                    pred_class = CLASS_NAMES[pred.item()]
                    st.session_state.prediction = pred_class
                    probabilities = torch.nn.functional.softmax(output, dim=1).numpy().flatten().tolist()
            else:
                # Demo mode - simulate prediction based on image hash for consistency
                img_hash = hashlib.md5(image.tobytes()).hexdigest()
                pred_idx = int(img_hash, 16) % len(CLASS_NAMES)
                pred_class = CLASS_NAMES[pred_idx]
                st.session_state.prediction = pred_class
                st.info("🔬 Running in demo mode - predictions are simulated for demonstration purposes")
                # Create simulated probabilities
                probabilities = [0.15, 0.20, 0.15, 0.15]
                probabilities[pred_idx] = 0.65
                output = torch.tensor([probabilities])
        except Exception as e:
            st.error(f"Error during analysis: {e}")
            # Fallback to acne as default
            pred_class = "acne"
            probabilities = [0.7, 0.1, 0.1, 0.1]
            output = torch.tensor([probabilities])

    # Show detection result with emphasis
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%); 
                    padding: 25px; 
                    border-radius: 20px; 
                    text-align: center; 
                    margin: 30px 0;
                    box-shadow: 0 8px 20px rgba(255, 105, 180, 0.3);">
            <h2 style="color: white; margin: 0; font-size: 28px;">
                🎯 Detected Skin Concern: <strong>{pred_class.title()}</strong>
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    products = get_products(pred_class)
    acids = get_acids_for_skin_problem(pred_class)
    diet = get_diet(pred_class)

    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'<div class="subtitle">🧴 Recommended Products</div>', unsafe_allow_html=True)
        st.markdown('<div class="section">', unsafe_allow_html=True)
        for i, item in enumerate(products, 1):
            st.markdown(f"**{i}.** {item}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="subtitle">🧪 Key Active Ingredients</div>', unsafe_allow_html=True)
        st.markdown('<div class="section">', unsafe_allow_html=True)
        for item in acids:
            st.markdown(f"💊 **{item}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="subtitle">🥗 Dietary Recommendations</div>', unsafe_allow_html=True)
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown("**✅ Foods to Eat:**")
        for item in diet['eat']:
            st.markdown(f"  • {item}")
        st.markdown("")
        st.markdown("**❌ Foods to Avoid:**")
        for item in diet['avoid']:
            st.markdown(f"  • {item}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show confidence chart
        st.markdown(f'<div class="subtitle">📊 Confidence Levels</div>', unsafe_allow_html=True)
        if probabilities:
            confidence_data = {CLASS_NAMES[i]: probabilities[i] for i in range(len(CLASS_NAMES))}
            st.bar_chart(confidence_data)

    st.subheader("📄 Download Prescription")
    if st.button("Generate PDF"):
        # Use already calculated probabilities or recalculate if needed
        if probabilities is None and output is not None:
            probabilities = torch.nn.functional.softmax(output, dim=1).numpy().flatten().tolist()
        elif probabilities is None:
            # Fallback probabilities
            probabilities = [0.25, 0.25, 0.25, 0.25]
        
        path = generate_pdf(
            pred_class, products, acids, diet,
            username=st.session_state.user,
            probabilities=probabilities
        )
        with open(path, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name=os.path.basename(path))
        st.success(f"Prescription generated: {os.path.basename(path)}")
        
    if st.button("🔄 Analyze Another Image"):
        st.session_state.page = "upload"
        st.rerun()

# === Footer ===
st.markdown("<hr><center>Made with 💗 by Pooja • Aura Derm 2025</center>", unsafe_allow_html=True)
