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

# Custom imports
from app.main import SkinClassifier
from app.recommender import get_products
from app.food_map import get_diet
from app.acid_map import get_acids_for_skin_problem

# === Configuration ===
CONFIG_PATH = "config.yaml"
MODEL_PATH = "D:/Aura_derm/models/skin_classifier.pth"
LOGO_PATH = "D:/Aura_derm/logo.png"
DOWNLOAD_FOLDER = "D:/Aura_derm/prescriptions"
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
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# === Load Model ===
if not os.path.exists(MODEL_PATH):
    st.error("Model file not found. Please ensure 'skin_classifier.pth' exists.")
    st.stop()

model = SkinClassifier()
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()

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
import matplotlib.pyplot as plt

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

    pdf.output(path)
    return path

# === Aesthetic Styling ===
st.set_page_config(page_title="Aura Derm", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #fff6f9; }
    .title {
        font-size: 40px; font-weight: 800; color: #e91e63; text-align: center;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .subtitle {
        font-size: 24px; font-weight: bold; color: #d6336c;
        margin-top: 20px; margin-bottom: 10px; font-family: 'Arial';
    }
    .section {
        background-color: #ffffff; padding: 15px 25px;
        border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 25px; font-size: 18px;
    }
    .stButton>button {
        background-color: #ff69b4; color: white;
        border-radius: 12px; font-size: 16px; padding: 10px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff85c1;
    }
    .sidebar .sidebar-content {
        background-color: #ffe4ec;
    }
    </style>
""", unsafe_allow_html=True)

# === Logo ===
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_column_width=True)
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
    name, auth_status, username = authenticator.login("Login", location="main")
    if auth_status:
        st.session_state.page = "upload"
        st.session_state.user = name
        st.rerun()
    elif auth_status is False:
        st.error("Invalid username or password")
    elif auth_status is None:
        st.warning("Please enter login credentials.")

# === Upload Page ===
elif st.session_state.page == "upload":
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Logged in as {st.session_state.user}")
    st.markdown('<div class="title">💆‍♀️ Upload or Capture Image</div>', unsafe_allow_html=True)
    input_method = st.radio("Select Image Input", ['📄 Upload Image', '📸 Camera'])
    image = None
    if input_method == "📄 Upload Image":
        uploaded = st.file_uploader("Upload face image", type=["jpg", "jpeg", "png"])
        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        cam = st.camera_input("Take a clear face photo")
        if cam:
            image = Image.open(cam).convert("RGB")
            st.image(image, caption="Captured Image", use_column_width=True)
    if image:
        st.session_state.image = image
        st.session_state.page = "results"
        st.rerun()

# === Results Page ===
elif st.session_state.page == "results":
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Logged in as {st.session_state.user}")
    image = st.session_state.image
    img_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(img_tensor)
        _, pred = torch.max(output, 1)
        pred_class = CLASS_NAMES[pred.item()]
        st.session_state.prediction = pred_class

    st.markdown(f'<div class="subtitle">🧐 Detected: <span style="color:#e75480">{pred_class.title()}</span></div>', unsafe_allow_html=True)
    products = get_products(pred_class)
    acids = get_acids_for_skin_problem(pred_class)
    diet = get_diet(pred_class)

    st.markdown(f'<div class="subtitle">🧴 Recommended Products</div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    for item in products:
        st.markdown(f"✔️ {item}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="subtitle">🧪 Acids to Look For</div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    for item in acids:
        st.markdown(f"🔹 {item}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="subtitle">🥗 Food Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("✅ Eat: " + ", ".join(diet['eat']))
    st.markdown("❌ Avoid: " + ", ".join(diet['avoid']))
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("📄 Download Prescription")
    if st.button("Generate PDF"):
        # Calculate probabilities (optional)
        probabilities = torch.nn.functional.softmax(output, dim=1).numpy().flatten().tolist()
        
        path = generate_pdf(
            pred_class, products, acids, diet,
            username=st.session_state.user,
            probabilities=probabilities
        )
        with open(path, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name=os.path.basename(path))
        st.success(f"Prescription generated: {os.path.basename(path)}")
# === Footer ===
st.markdown("<hr><center>Made with 💗 by Pooja • Aura Derm 2025</center>", unsafe_allow_html=True)
