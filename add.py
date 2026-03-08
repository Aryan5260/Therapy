import streamlit as st

from modules.symptom_analyzer import analyze_symptoms
from modules.risk_scoring import calculate_risk
from modules.ai_explainer import generate_explanation
from utils.logger import log_event

st.title("MedSafe AI - Symptom Checker")
st.warning("This tool provides educational information only and does not replace professional medical advice.")
symptoms = st.text_input("Enter symptoms separated by comma")

if st.button("Analyze"):

    symptom_list = [s.strip() for s in symptoms.split(",")]

    analysis = analyze_symptoms(symptom_list)

    risk = calculate_risk(symptom_list)

    explanation = generate_explanation(symptom_list)

    st.subheader("Symptom Analysis")
    st.write(analysis)

    st.subheader("Risk Score")
    st.write(f"{risk}%")

    st.subheader("AI Explanation")
    st.write(explanation)

    log_event(f"Symptoms analyzed: {symptom_list}")
