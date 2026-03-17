"""
MedSafe AI - Main Streamlit Application
Front-end interface and main application logic
"""

import streamlit as st
import pandas as pd
from PIL import Image

from med_db import MedicineDatabase
from symptom import SymptomChecker
from ocr_utils import PrescriptionOCR
from risk_engine import RiskAssessment
from side_effects import SideEffectAnalyzer


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MedSafe AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- SESSION STATE ----------------
def init_session():

    if "prescription_text" not in st.session_state:
        st.session_state.prescription_text = ""

    if "interaction_result" not in st.session_state:
        st.session_state.interaction_result = None

    if "symptom_result" not in st.session_state:
        st.session_state.symptom_result = None

    if "side_effect_log" not in st.session_state:
        st.session_state.side_effect_log = None

    if "risk_result" not in st.session_state:
        st.session_state.risk_result = None


# ---------------- INITIALIZE MODULES ----------------
@st.cache_resource
def init_components():

    med_db = MedicineDatabase()
    symptom_checker = SymptomChecker()
    ocr_processor = PrescriptionOCR()
    risk_assessor = RiskAssessment()
    side_effect_engine = SideEffectAnalyzer()

    return med_db, symptom_checker, ocr_processor, risk_assessor, side_effect_engine


# ---------------- MAIN APP ----------------
def main():

    init_session()

    st.title("🏥 MedSafe AI - Intelligent Medicine Safety Assistant")
    st.markdown("---")

    med_db, symptom_checker, ocr_processor, risk_assessor, side_effect_engine = init_components()

    # ---------------- SIDEBAR ----------------
    with st.sidebar:

        st.header("Navigation")

        page = st.selectbox(
            "Select Service",
            [
                "🏠 Home",
                "💊 Medicine Interaction Checker",
                "🔍 Symptom & Doubt Solver",
                "📄 Prescription OCR",
                "⚠️ Side-Effect Monitor",
                "🚨 Emergency Risk Predictor"
            ]
        )

    # ---------------- HOME ----------------
    if page == "🏠 Home":

        st.header("Welcome to MedSafe AI")

        st.write(
        """
        MedSafe AI helps you:

        • Check medicine interactions  
        • Analyze symptoms  
        • Extract prescription data using OCR  
        • Monitor medicine side-effects  
        • Predict emergency health risks
        """
        )

    # ---------------- MEDICINE CHECKER ----------------
    elif page == "💊 Medicine Interaction Checker":

        st.header("💊 Medicine Interaction Checker")

        medicines = st.text_input(
            "Enter medicines (comma separated)"
        )

        if st.button("Check Interactions"):

            if medicines.strip() == "":
                st.warning("Please enter at least one medicine.")

            else:

                med_list = [m.strip() for m in medicines.split(",")]

                result = med_db.check_interactions(med_list)

                st.session_state.interaction_result = result

        if st.session_state.interaction_result:

            st.success("Interaction Result")

            st.write(st.session_state.interaction_result)

    # ---------------- SYMPTOM ANALYSIS ----------------
    elif page == "🔍 Symptom & Doubt Solver":

        st.header("🔍 Symptom Interpretation")

        symptoms = st.text_area(
            "Describe your symptoms"
        )

        if st.button("Analyze Symptoms"):

            if symptoms.strip() == "":
                st.warning("Please describe your symptoms.")

            else:

                analysis = symptom_checker.analyze(symptoms)

                st.session_state.symptom_result = analysis

        if st.session_state.symptom_result:

            result = st.session_state.symptom_result

            st.subheader("Detected Symptoms")
            st.write(result["symptoms_detected"])

            st.subheader("Possible Conditions")
            st.write(result["possible_conditions"])

            st.subheader("Recommendations")
            st.write(result["recommendations"])

            if result["seek_immediate_help"]:
                st.error("⚠️ Seek Immediate Medical Attention")

    # ---------------- PRESCRIPTION OCR ----------------
    elif page == "📄 Prescription OCR":

        st.header("📄 Prescription Scanner")

        uploaded_file = st.file_uploader(
            "Upload prescription image",
            type=["png", "jpg", "jpeg"]
        )

        if uploaded_file:

            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Uploaded Prescription",
                use_column_width=True
            )

            if st.button("Extract Text"):

                text = ocr_processor.extract_text(image)

                st.session_state.prescription_text = text

        if st.session_state.prescription_text:

            st.text_area(
                "Extracted Text",
                st.session_state.prescription_text,
                height=200
            )

    # ---------------- SIDE EFFECT MONITOR ----------------
    elif page == "⚠️ Side-Effect Monitor":

        st.header("⚠️ Experience & Side-Effect Monitor")

        age = st.number_input(
            "Enter your age",
            min_value=1,
            max_value=120
        )

        gender = st.selectbox(
            "Select gender",
            ["Male", "Female", "Other"]
        )

        medicine = st.text_input(
            "Enter medicine(s) taken"
        )

        dosage = st.selectbox(
            "Dosage level",
            ["low", "normal", "high"]
        )

        side_effects = st.text_input(
            "Enter experienced side-effects (comma separated)"
        )

        if st.button("Analyze Side Effects"):

            if medicine == "" or side_effects == "":
                st.warning("Please enter medicine and side-effects.")

            else:

                effects = [e.strip() for e in side_effects.split(",")]

                result = side_effect_engine.analyze(
                    medicine,
                    effects,
                    age,
                    gender,
                    dosage
                )

                st.session_state.side_effect_log = result

        if st.session_state.side_effect_log:

            st.subheader("Side-Effect Analysis")

            st.write(st.session_state.side_effect_log)

    # ---------------- RISK PREDICTOR ----------------
    elif page == "🚨 Emergency Risk Predictor":

        st.header("🚨 Emergency Risk Predictor")

        age = st.number_input(
            "Enter Age",
            min_value=1,
            max_value=120
        )

        conditions = st.multiselect(
            "Existing Conditions",
            [
                "Diabetes",
                "Hypertension",
                "Heart Disease",
                "Asthma"
            ]
        )

        symptoms = st.text_input(
            "Current Symptoms (comma separated)"
        )

        if st.button("Assess Risk"):

            symptom_list = [s.strip() for s in symptoms.split(",") if s]

            risk_score = risk_assessor.calculate_risk(
                age,
                conditions,
                symptom_list
            )

            assessment = risk_assessor.assess_emergency(
                risk_score,
                symptom_list
            )

            st.session_state.risk_result = {
                "score": risk_score,
                "assessment": assessment
            }

        if st.session_state.risk_result:

            st.metric(
                "Risk Score",
                f"{st.session_state.risk_result['score']}/100"
            )

            st.write(
                st.session_state.risk_result["assessment"]
            )


if __name__ == "__main__":
    main()
