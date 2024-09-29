import streamlit as st
from sklearn.preprocessing import LabelEncoder
import pickle
import gzip
import numpy as np

# Load the model
with gzip.open('model.pkl.gz', 'rb') as f:
    model = pickle.load(f)

contract_encoder = LabelEncoder()
contract_encoder.classes_ = np.array(['Month-to-month', 'One year', 'Two year'])

payment_method_encoder = LabelEncoder()
payment_method_encoder.classes_ = np.array(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])


def predict_churn(input_data):
    input_data[3] = contract_encoder.transform([input_data[3]])[0]
    input_data[4] = payment_method_encoder.transform([input_data[4]])[0]
    prediction = model.predict([input_data])
    return prediction

# Sidebar for menu navigation
menu = st.sidebar.selectbox("Menu", ["Home", "Churn Prediction"])

# Home Page
if menu == "Home":
    st.markdown("""
    <div style='text-align: center; color:white;background-color:black;'>
    <h1 style='color:white;'>Telco Churn Predcition App</h1>
    <h5 style='color:white;'>Built by Ezekiel Akuso</h5>
    </div>
    """, unsafe_allow_html=True)
    st.image('churn_img.png', use_column_width=True)
    
    st.markdown("""
    <h5 style='text-align: center; color: Blue;'>This app allows you to predict whether a customer will churn based on key features such as Total Charges, Monthly Charges, tenure, Contract, and Payment Method.</h5>
    <h6 style='text-align: center; color:green;'>Navigate to the Churn Prediction menu to make a prediction.</h6>
    """, unsafe_allow_html=True)

# Churn prediction page
elif menu == "Churn Prediction":
    st.title("Customer Churn Prediction")

    # User inputs with bold labels
    st.markdown("**TotalCharges**")
    total_charges = st.number_input('', label_visibility="collapsed")

    st.markdown("**MonthlyCharges**")
    monthly_charges = st.number_input('', key='monthly_charges', label_visibility="collapsed")

    st.markdown("**Tenure (in months)**")
    tenure = st.number_input('', min_value=1, max_value=500, step=1, label_visibility="collapsed")

    st.markdown("**Contract**")
    contract = st.selectbox('', ['Month-to-month', 'One year', 'Two year'], label_visibility="collapsed")

    st.markdown("**PaymentMethod**")
    payment_method = st.selectbox('', ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], key='payment_method', label_visibility="collapsed")

    try:
        if st.button('Predict Churn'):
            if total_charges > 0 and monthly_charges > 0 and tenure > 0:
                input_data = [total_charges, monthly_charges, tenure, contract, payment_method]
                predicted_churn = predict_churn(input_data)
                churn_outcome = "Yes" if predicted_churn[0] == 1 else "No"
                st.success(f"The predicted churn outcome is: {churn_outcome}")
            else:
                st.warning("Please fill in all the required fields.")
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
