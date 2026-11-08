
import streamlit as st
import joblib

from logic import generate_truth_table, expressions
from rules import (
    detect_gate_by_rules,
    detect_unsupported_description
)

# Page configuration
st.set_page_config(
    page_title="LogicGate AI",
    page_icon="⚡",
    layout="wide"
)

# Custom design
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #f8fafc;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

[data-testid="stSidebar"] {
    background-color: #111c31;
}

[data-testid="stSidebar"] * {
    color: #f1f5f9;
}

div.stButton > button {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

.result-card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 22px;
    margin: 15px 0;
}

.result-label {
    color: #94a3b8;
    font-size: 14px;
}

.result-value {
    color: #93c5fd;
    font-size: 30px;
    font-weight: 700;
}

.subtitle {
    color: #94a3b8;
    font-size: 17px;
}
</style>
""", unsafe_allow_html=True)


# Load machine learning model
@st.cache_resource
def load_model():
    return joblib.load("logic_gate_model.pkl")


model = load_model()


# Sidebar
with st.sidebar:
    st.title("⚡ LogicGate AI")
    st.caption("Digital Electronics | P2 Project")

    st.divider()

    st.subheader("About the Project")
    st.write(
        "This application identifies digital logic gates "
        "from natural-language descriptions using a "
        "hybrid rule-based and machine-learning system."
    )

    st.subheader("Supported Gates")
    st.write("AND · OR · NOT · NAND · NOR · XOR · XNOR")

    st.divider()

    st.subheader("Technologies")
    st.write("Python")
    st.write("Streamlit")
    st.write("Scikit-learn")
    st.write("TF-IDF + LinearSVC")

    st.divider()
    st.caption("Hybrid AI Logic Gate Identifier")


# Main heading
st.title("⚡ Digital Logic Gate Identifier")

st.markdown(
    '<p class="subtitle">'
    'Describe the behavior of a digital circuit and '
    'identify its logic gate using AI.'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# Example descriptions
examples = {
    "Custom Description": "",
    "AND Gate": "Output is high only when both inputs are high",
    "OR Gate": "Output is high when at least one input is high",
    "NOT Gate": "Invert the input signal",
    "NAND Gate": "Output is low only when both inputs are high",
    "NOR Gate": "Output is high only when both inputs are low",
    "XOR Gate": "The inputs are different",
    "XNOR Gate": "The inputs are equal",
    "Unsupported Circuit":
        "The circuit activates whenever a majority of three sensors detect motion"
}

st.subheader("Describe Your Logic Gate")

selected_example = st.selectbox(
    "Choose an example or enter your own description:",
    list(examples.keys())
)

description = st.text_area(
    "Logic gate description",
    value=examples[selected_example],
    height=120,
    placeholder="Example: Both inputs must be HIGH...",
    key=selected_example
)

identify = st.button(
    "🔍 Identify Logic Gate",
    type="primary",
    use_container_width=True
)


# Prediction
if identify:

    if not description.strip():
        st.warning("Please enter a description first.")

    elif detect_unsupported_description(description):
        st.warning("Unsupported circuit description")
        st.info(
            "This description appears to refer to a circuit "
            "outside the seven supported logic gates."
        )

    else:
        rule_prediction = detect_gate_by_rules(description)

        if rule_prediction is not None:
            prediction = rule_prediction
            method = "Rule-Based Detection"
        else:
            prediction = model.predict([description])[0]
            method = "Machine Learning (LinearSVC)"

        st.divider()
        st.subheader("Identification Result")

        # Display gate and method
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">PREDICTED LOGIC GATE</div>
                <div class="result-value">{prediction} Gate</div>
                <div class="result-label">Detection Method: {method}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Boolean expression
        st.subheader("Boolean Expression")
        st.code(expressions[prediction])

        # Truth table
        st.subheader("Truth Table")
        table = generate_truth_table(prediction)
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

        # Explanation
        explanations = {
            "AND": "The output is HIGH only when both inputs are HIGH.",
            "OR": "The output is HIGH when at least one input is HIGH.",
            "NOT": "The output is the opposite of the single input.",
            "NAND": "The output is LOW only when both inputs are HIGH.",
            "NOR": "The output is HIGH only when both inputs are LOW.",
            "XOR": "The output is HIGH when the inputs are different.",
            "XNOR": "The output is HIGH when the inputs are equal."
        }

        st.subheader("How This Gate Works")
        st.info(explanations[prediction])

        if method == "Machine Learning (LinearSVC)":
            st.warning(
                "No rule matched this description. "
                "The machine-learning prediction may be unreliable."
            )

st.divider()

st.caption(
    "P2 Project | Hybrid AI Digital Logic Gate Identifier"
)
