import streamlit as st
import requests
from datetime import date, timedelta
import re
from integrations.google_genai_integration import fetch_travel_recommendations

# Set page configuration
st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")

# Inject CSS for Improved Font & Colors
st.markdown("""
    <style>
    body, div, input, select, textarea, button {
        font-family: 'Arial', sans-serif !important;
        font-size: 16px !important;
    }
    .stTextInput>div>div>input, 
    .stSelectbox>div>div>select, 
    .stDateInput>div>div>input, 
    .stNumberInput>div>div>input {
        font-size: 16px !important;
    }
    .stButton>button {
        background-color: #008CBA !important;
        font-size: 18px !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
    }
    .stButton>button:hover {
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for API keys if not already set
if "GENAI_API_KEY" not in st.session_state:
    st.session_state["GENAI_API_KEY"] = None

# Sidebar for API Keys
st.sidebar.markdown("### 🔑 API Keys Required")
st.sidebar.markdown("[📚 How to get a Google AI API Key?](https://aistudio.google.com/)")

GENAI_API_KEY = st.sidebar.text_input(
    "Enter Google AI API Key", type="password", value=st.session_state["GENAI_API_KEY"]
)

# Button to verify API keys
if st.sidebar.button("✅ Verify API Key"):
    if GENAI_API_KEY:
        st.session_state["GENAI_API_KEY"] = GENAI_API_KEY
        st.sidebar.success("✅ API key verified and saved!")
    else:
        st.sidebar.error("⚠️ Please enter a valid API key!")

# Button to reset API keys
if st.sidebar.button("🔄 Reset API Key"):
    st.session_state["GENAI_API_KEY"] = None
    st.sidebar.warning("⚠️ API key has been reset. Please re-enter it.")

def main():
    if not st.session_state["GENAI_API_KEY"]:
        st.warning("⚠️ Please verify your API key in the sidebar before proceeding.")
        return

    st.markdown("# 🌍 AI Travel Planner")

    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input("📍 **Source Location**")
        start_date = st.date_input("📅 **Start Date**", date.today())

    with col2:
        destination = st.text_input("📍 **Destination Location**")
        end_date = st.date_input("📅 **End Date**", date.today() + timedelta(days=5))

    mode = st.selectbox("✈️🚂🚌🚖 **Preferred Transport Mode**", ["Flight", "Train", "Bus", "Cab", "Any"])
    budget = st.selectbox("💰 **Budget Range**", ["Budget", "Standard", "Luxury"])
    time = st.selectbox("⏰ **Preferred Travel Time**", ["Morning", "Afternoon", "Evening", "Night"])
    travelers = st.number_input("👥 **Number of Travelers**", min_value=1, step=1)

    if st.button("🎒 **Plan My Trip**"):
        if not all([source, destination]):
            st.error("⚠️ Please fill in all fields before proceeding.")
            return

        date_range = f"{start_date} to {end_date}"

        # Fetch recommendations (assuming API returns prices in USD)
        recommendations = fetch_travel_recommendations(
            source, destination, mode, budget, time, travelers, date_range, st.session_state["GENAI_API_KEY"]
        )

        st.markdown("## ✨ **Travel Recommendations**")
        st.markdown(recommendations)

if __name__ == "__main__":
    main()
