import streamlit as st
from logic import extract_medicines_from_image, identify_medicine, check_interaction

# 1. Page Configuration
st.set_page_config(page_title="MedSafe AI", layout="centered", page_icon="💊")
st.title("MedSafe AI")
st.markdown("### AI-driven Medical Safety Assistant")

# 2. Activity 2.1: Manual Medicine Input
st.subheader("📝 Manual Medicine Input")
user_input = st.text_area("Enter medicines separated by commas (e.g., Paracetamol, Ibuprofen):")

if st.button("Check Manual Entry"):
    if user_input:
        raw_names = [name.strip() for name in user_input.split(",")]
        manual_meds = [identify_medicine(name) for name in raw_names if identify_medicine(name)]
        
        if manual_meds:
            st.success(f"Recognized: {', '.join(manual_meds)}")
            for w in check_interaction(manual_meds):
                st.warning(w)

st.divider()

# 3. Activity 2.2: AI-Powered OCR Scanner
st.subheader("📷 Prescription OCR Scanner")
uploaded_file = st.file_uploader("Upload a prescription image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    with st.spinner('AI is analyzing the prescription...'):
        structured_data, _ = extract_medicines_from_image(uploaded_file)
        
        if structured_data.get('medicines'):
            st.success("Detected Medicines & Active Salts")
            med_names = []
            for med in structured_data['medicines']:
                st.markdown(f"💊 **{med['name']}** → *{med['salt']}* ({med['dosage']})")
                med_names.append(med['name'])
            
            for w in check_interaction(med_names):
                st.warning(w)