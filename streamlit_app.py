"""
MedSafe AI - Main Streamlit Application
Front-end interface and main application logic
"""

import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
from med_db import MedicineDatabase
from symptom import SymptomChecker
from ocr_utils import PrescriptionOCR
from risk_engine import RiskAssessment

# Page configuration
st.set_page_config(
    page_title="MedSafe AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def init_components():
    """Initialize all application components"""
    med_db = MedicineDatabase()
    symptom_checker = SymptomChecker()
    ocr_processor = PrescriptionOCR()
    risk_assessor = RiskAssessment()
    return med_db, symptom_checker, ocr_processor, risk_assessor

def main():
    """Main application entry point"""
    st.title("🏥 MedSafe AI - Medical Safety Assistant")
    st.markdown("---")
    
    # Initialize components
    med_db, symptom_checker, ocr_processor, risk_assessor = init_components()
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Select Service",
            ["🏠 Home", "💊 Medicine Check", "🔍 Symptom Analysis", 
             "📄 Prescription OCR", "⚠️ Risk Assessment"]
        )
    
    # Main content area
    if page == "🏠 Home":
        st.header("Welcome to MedSafe AI")
        st.write("""
        MedSafe AI is your intelligent medical safety companion that helps you:
        - Check medicine interactions and safety
        - Analyze symptoms with AI assistance
        - Extract prescription information using OCR
        - Assess health risks and provide recommendations
        """)
        
    elif page == "💊 Medicine Check":
        st.header("Medicine Interaction Checker")
        
        col1, col2 = st.columns(2)
        with col1:
            medicine_name = st.text_input("Enter medicine name:")
            if st.button("Check Interactions"):
                if medicine_name:
                    interactions = med_db.check_interactions(medicine_name)
                    st.write(interactions)
                    
    elif page == "🔍 Symptom Analysis":
        st.header("Symptom Checker")
        symptoms = st.text_area("Describe your symptoms:")
        if st.button("Analyze Symptoms"):
            if symptoms:
                analysis = symptom_checker.analyze(symptoms)
                st.write(analysis)
                
    elif page == "📄 Prescription OCR":
        st.header("Prescription Scanner")
        uploaded_file = st.file_uploader("Upload prescription image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Prescription", use_column_width=True)
            if st.button("Extract Text"):
                extracted_text = ocr_processor.extract_text(image)
                st.text_area("Extracted Text:", extracted_text, height=200)
                
    elif page == "⚠️ Risk Assessment":
        st.header("Health Risk Assessment")
        age = st.number_input("Age", min_value=1, max_value=120)
        conditions = st.multiselect("Existing conditions", 
                                   ["Diabetes", "Hypertension", "Heart Disease", "Asthma"])
        if st.button("Assess Risk"):
            risk_score = risk_assessor.calculate_risk(age, conditions)
            st.metric("Risk Score", f"{risk_score}/100")

if __name__ == "__main__":
    main()
