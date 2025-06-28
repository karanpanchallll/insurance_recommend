import streamlit as st
import pandas as pd
import re
import markdown

from serp_search import get_policy_recommendations_from_serpapi
from utils import build_prompt_with_search
from gemini_llm import query_gemini
from risk_assesment import calculate_risk_score
from customer_support_agent import get_support_response

# Load dataset
df = pd.read_csv("data_synthetic.csv")

# Page setup
st.set_page_config(page_title="PolicyPal – Real-Time Insurance Advisor", layout="centered")
st.title("🧠 PolicyPal – Real-Time Insurance Advisor")

# Insurance types
insurance_types = [
    "Term Life Insurance",
    "Health Insurance",
    "Family Floater Plan",
    "Critical Illness Cover",
    "Group Health Insurance",
    "Group Life Insurance",
    "Personal Accident Insurance",
]

# Diseases
disease_options = [
    "None", "Diabetes", "Hypertension", "Asthma", "Heart Disease",
    "Cancer", "Thyroid", "Obesity", "Other"
]

# Tabs
tabs = st.tabs(["🧠 Policy Recommendation", "🤝 Customer Support"])

# -----------------------------------------------
# Tab 1: Policy Recommendation
# -----------------------------------------------
with tabs[0]:
    st.markdown("## 📌 Step 1: Insurance Plan Type")
    policy_type = st.selectbox("Preferred Insurance Type", insurance_types)

    # Conditional input for Family Plan
    family_members = 0
    family_diseases = []
    if policy_type == "Family Floater Plan":
        family_members = st.slider("👨‍👩‍👧‍👦 Number of Family Members to Cover", 1, 10, 2)
        st.markdown("### 🏥 Family Members' Pre-existing Conditions:")
        for i in range(family_members):
            disease = st.selectbox(
                f"Member {i+1} – Pre-existing Condition", disease_options, key=f"disease_{i}"
            )
            family_diseases.append(disease)
    else:
        disease = st.selectbox("🏥 Your Pre-existing Condition", disease_options)

    # Main form
    with st.form("policy_form"):
        st.markdown("## 🧾 Step 2: Personal & Lifestyle Info")
        age = st.slider("Age", 18, 80)
        gender = st.selectbox("Gender", df["Gender"].dropna().unique())
        marital_status = st.selectbox("Marital Status", df["Marital Status"].dropna().unique())
        occupation = st.selectbox("Occupation", df["Occupation"].dropna().unique())
        income = st.number_input("Annual Income (₹)", min_value=10000, step=1000)
        education = st.selectbox("Education Level", df["Education Level"].dropna().unique())
        location = st.selectbox("Geographic Information", df["Geographic Information"].dropna().unique())
        smoker = st.radio("Do you smoke?", ["Yes", "No"])
        driving_record = st.selectbox("Driving Record", df["Driving Record"].dropna().unique())
        submitted = st.form_submit_button("🔍 Find My Policy")

    if submitted:
        # Risk assessment
        risk_score = calculate_risk_score(age, income, driving_record, smoker)

        user_profile = {
            "Age": age,
            "Gender": gender,
            "Marital Status": marital_status,
            "Occupation": occupation,
            "Income Level": income,
            "Education Level": education,
            "Geographic Information": location,
            "Preferred Policy Type": policy_type,
            "Smoker": smoker,
            "Driving Record": driving_record,
            "Risk Score": risk_score,
            "Family Members": family_members if policy_type == "Family Floater Plan" else "N/A",
            "Pre-existing Condition": family_diseases if policy_type == "Family Floater Plan" else disease,
        }

        with st.spinner("🔍 Searching best insurance policies for you in real-time..."):
            search_results = get_policy_recommendations_from_serpapi(user_profile)

        if not search_results:
            st.error("❌ No policy data found from the web. Please try again later.")
        else:
            prompt = build_prompt_with_search(user_profile, search_results)
            with st.spinner("🤖 Analyzing with Gemini to recommend the best policy..."):
                try:
                    recommendation = query_gemini(prompt)
                    st.success("✅ Recommendation ready!")

                    # Display recommendations with readable cards
                    try:
                        underwriting_section, policy_section = recommendation.split("### 🏆 Top 7 Recommended Policies:")
                        st.markdown(underwriting_section)

                        policies = policy_section.strip().split("\n\n")
                        for idx, p in enumerate(policies, 1):
                            if p.strip():
                                p_cleaned = re.sub(r"^\d+\.\s*", "", p.strip())
                                html_content = markdown.markdown(f"**{idx}.** {p_cleaned}", extensions=["extra"])

                                st.markdown(
                                    f"""
                                    <div style='
                                        border: 1px solid #ddd;
                                        border-radius: 10px;
                                        padding: 15px;
                                        margin-bottom: 15px;
                                        background-color: #f5f9ff;
                                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                                        color: #1a202c;
                                        font-size: 15px;
                                    '>
                                        {html_content}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                    except ValueError:
                        st.markdown(recommendation)

                except Exception as e:
                    st.error(f"Gemini API Error: {e}")

# -----------------------------------------------
# Tab 2: Customer Support GenAI Agent
# -----------------------------------------------
with tabs[1]:
    st.markdown("### 🤝 Ask our AI Assistant (Customer Support)")
    user_question = st.text_input("Ask your insurance-related question (e.g., What is deductible?)")

    if st.button("💬 Get Support"):
        if user_question.strip():
            with st.spinner("🤖 Thinking..."):
                try:
                    response = get_support_response(user_question)
                    st.success("🗨️ Response:")
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please type a question to proceed.")
