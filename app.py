import streamlit as st

# Page configuration
st.set_page_config(page_title="MedSafe AI", layout="centered")

# Basic UI Elements
st.title("MedSafe AI")
st.header("AI-driven Medical Safety Assistant")
st.write("Streamlit application successfully initialized for MedSafe AI project.")

# Placeholder for interaction check (Requirement from your activity description)
st.subheader("Medicine Interaction Check")
medicine_name = st.text_input("Enter Medicine Name:")
if medicine_name:
    st.info(f"Checking interactions for: {medicine_name}...")