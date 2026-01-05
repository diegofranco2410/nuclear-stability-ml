import pandas as pd
import streamlit as st
import joblib

# Configuration
st.set_page_config(page_title="Nuclear Stability AI", page_icon="⚛️")

st.title("⚛️ Prediction of Nuclear Stability")
st.markdown("""
            This AI uses a **XGBoost** model to predict 
            if an isotope is stable or unstable. 
            Type the number of protons (Z) and neutrons (N) and press Enter.
            """)
            
# Load model
@st.cache_resource
def load_model():
    return joblib.load('models/nuclear_forest.pkl')

try:
    model = load_model()
except:
    st.error("Error: 'models/nuclear_forest.pkl' not found.")
    st.stop()
    
# Sidebar (inputs)
st.sidebar.header("Nuclei configuration")

# CAMBIO 1: Usamos number_input en lugar de slider
# number_input allows the user to input a number with the keyboard, and step=1 changes this value by 1 unit.
# the default value is set to 1 for protons, and the number of protons is the default value for neutrons.
Z = st.sidebar.number_input("Number of protons (Z)", min_value=0, max_value=118, value=1, step=1)
N = st.sidebar.number_input("Number of neutrons (N)", min_value=0, max_value=177, value=Z, step=1)

# Computing relevant data
A = Z + N
if Z == 0:
    NZ_ratio = 0
else:
    NZ_ratio = N/Z

# Display metrics
col1, col2 = st.columns(2)
col1.metric("Mass (A)", A)
col2.metric("Ratio N/Z", f"{NZ_ratio:.2f}")

st.divider()

# To update every time N or Z changes

input_data = pd.DataFrame({
    'Z': [Z],
    'N': [N],
    'A': [A],
    'NZ_ratio': [NZ_ratio],
    'Mass_Excess': [0] # Dummy value
})

# Prediction
prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0]

# Results
if prediction == 1:
    st.success(f"✅ **STABLE**: The isotope Z={Z}, N={N} is stable.")
    st.progress(float(probability[1]), text=f"AI Confidence: {probability[1]*100:.1f}%")
else:
    st.error(f"☢️ **UNSTABLE**: The isotope Z={Z}, N={N} is unstable.")
    st.progress(float(probability[0]), text=f"AI Confidence: {probability[0]*100:.1f}%")
