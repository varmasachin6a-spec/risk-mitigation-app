import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Risk Mitigation Tool",
    layout="wide"
)

st.title("🌐 AI-Based Risk Mitigation Matrix")

st.write(
    "This interactive web-based tool evaluates project risks using probability "
    "and impact, generates a mitigation matrix, visual risk assessment graphs, "
    "and an AI-style summary."
)

# -----------------------------
# Risk List
# -----------------------------
risk_names = [
    "Schedule Delay",
    "Cost Overrun",
    "Technical Failure",
    "Resource Shortage"
]

st.subheader("🔧 Enter Risk Parameters")

probabilities = []
impacts = []

# Input sliders
for risk in risk_names:
    col1, col2 = st.columns(2)

    with col1:
        p = st.slider(
            f"Probability – {risk}",
            min_value=1,
            max_value=5,
            value=3
        )

    with col2:
        i = st.slider(
            f"Impact – {risk}",
            min_value=1,
            max_value=5,
            value=3
        )

    probabilities.append(p)
    impacts.append(i)

# -----------------------------
# Risk Logic
# -----------------------------
def classify_risk(score):
    if score >= 6:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"

def mitigation(level):
    if level == "High":
        return "Avoid / Immediate Mitigation"
    elif level == "Medium":
        return "Monitor & Control"
    else:
        return "Accept & Review"

# -----------------------------
# Generate Output
# -----------------------------
if st.button("🚀 Generate Risk Assessment"):
    df = pd.DataFrame({
        "Risk": risk_names,
        "Probability": probabilities,
        "Impact": impacts
    })

    df["Risk Score"] = df["Probability"] * df["Impact"]
    df["Risk Level"] = df["Risk Score"].apply(classify_risk)
    df["Mitigation Strategy"] = df["Risk Level"].apply(mitigation)

    # -----------------------------
    # Risk Mitigation Matrix (Table)
    # -----------------------------
    st.subheader("📊 Risk Mitigation Matrix")
    st.dataframe(df, use_container_width=True)

    # -----------------------------
    # Risk Score Bar Chart
    # -----------------------------
    st.subheader("📈 Risk Assessment – Risk Score Graph")

    fig1, ax1 = plt.subplots()
    ax1.bar(df["Risk"], df["Risk Score"])
    ax1.set_xlabel("Risk")
    ax1.set_ylabel("Risk Score")
    ax1.set_title("Risk Score by Risk Type")
    plt.xticks(rotation=20)

    st.pyplot(fig1)

    # -----------------------------
    # Probability–Impact Heatmap
    # -----------------------------
    st.subheader("🔥 Probability–Impact Risk Heatmap")

    heatmap_data = pd.DataFrame(
        0,
        index=range(1, 6),
        columns=range(1, 6)
    )

    for p, i in zip(probabilities, impacts):
        heatmap_data.loc[p, i] += 1

    fig2, ax2 = plt.subplots()
    im = ax2.imshow(heatmap_data, cmap="YlOrRd")

    ax2.set_xlabel("Impact")
    ax2.set_ylabel("Probability")
    ax2.set_title("Risk Density Heatmap")

    ax2.set_xticks(range(5))
    ax2.set_yticks(range(5))
    ax2.set_xticklabels(range(1, 6))
    ax2.set_yticklabels(range(1, 6))

    plt.colorbar(im, ax=ax2, label="Number of Risks")
    st.pyplot(fig2)

    # -----------------------------
    # AI-Generated Summary
    # -----------------------------
    high = len(df[df["Risk Level"] == "High"])
    medium = len(df[df["Risk Level"] == "Medium"])
    low = len(df[df["Risk Level"] == "Low"])

    if high > 0:
        overall = "Critical risks are present and require immediate management attention."
    elif medium > 0:
        overall = "Moderate risks exist and should be continuously monitored."
    else:
        overall = "Overall project risk exposure is low and acceptable."

    st.subheader("🤖 AI-Generated Risk Summary")
    st.write(f"""
    **Total Risks Identified:** {len(df)}  
    **High Risks:** {high}  
    **Medium Risks:** {medium}  
    **Low Risks:** {low}

    **Interpretation:**  
    {overall}

    **Recommendation:**  
    Prioritize mitigation of high and medium risks to reduce overall project exposure.
    """)
