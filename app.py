import streamlit as st
import pandas as pd
import joblib
import os
import base64
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Power Grid Attack Detection",
    page_icon="⚡",
    layout="wide"
)

# -------------------- PROFESSIONAL BACKGROUND --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
    color: white;
}
h1, h2, h3, h4 {
    color: #ffffff;
}
[data-testid="stMetricValue"] {
    color: #00ffcc;
}
div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
}
div.stButton > button:hover {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.title("⚡ Power Grid Attack Detection System")
st.markdown("### Real-time Monitoring & Anomaly Detection 🚨")
st.markdown("---")

# -------------------- LOAD MODEL --------------------
model = joblib.load("cyber_attack_model.pkl")
scaler = joblib.load("scaler.pkl")

# -------------------- SIDEBAR --------------------
st.sidebar.title("⚙️ Settings")
st.sidebar.info("Enter bus parameters and detect anomalies")

# -------------------- RESET FUNCTION --------------------
def reset_values():
    keys = [
        "b2_vm", "b2_p", "b2_q",
        "b3_vm", "b3_p", "b3_q",
        "b4_vm", "b4_p", "b4_q",
        "b5_vm", "b5_p", "b5_q"
    ]
    for key in keys:
        st.session_state[key] = 0.0

# -------------------- INPUT SECTION --------------------
st.subheader("📥 Enter Bus Parameters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    b2_vm = st.number_input("Bus 2 vm_pu", value=0.0, key="b2_vm")
    b2_p = st.number_input("Bus 2 p_mw", value=0.0, key="b2_p")
    b2_q = st.number_input("Bus 2 q_mvar", value=0.0, key="b2_q")

with col2:
    b3_vm = st.number_input("Bus 3 vm_pu", value=0.0, key="b3_vm")
    b3_p = st.number_input("Bus 3 p_mw", value=0.0, key="b3_p")
    b3_q = st.number_input("Bus 3 q_mvar", value=0.0, key="b3_q")

with col3:
    b4_vm = st.number_input("Bus 4 vm_pu", value=0.0, key="b4_vm")
    b4_p = st.number_input("Bus 4 p_mw", value=0.0, key="b4_p")
    b4_q = st.number_input("Bus 4 q_mvar", value=0.0, key="b4_q")

with col4:
    b5_vm = st.number_input("Bus 5 vm_pu", value=0.0, key="b5_vm")
    b5_p = st.number_input("Bus 5 p_mw", value=0.0, key="b5_p")
    b5_q = st.number_input("Bus 5 q_mvar", value=0.0, key="b5_q")

# -------------------- BUTTONS --------------------
st.markdown("---")

btn1, btn2 = st.columns(2)

with btn1:
    analyze = st.button("🚀 Analyze Grid", use_container_width=True)

with btn2:
    reset = st.button("🔄 Reset", use_container_width=True)

if reset:
    reset_values()
    st.rerun()

# -------------------- PREDICTION FUNCTION --------------------
def predict_attack(vm, p, q):
    if vm <= 0 or p <= 0 or q <= 0:
        return "ATTACKED"
    elif vm >= 1 and p >= 1 and q >= 1:
        return "Normal"
    else:
        return "Warning"

# -------------------- ANALYZE --------------------
if analyze:

    buses = {
        "Bus 2": [b2_vm, b2_p, b2_q],
        "Bus 3": [b3_vm, b3_p, b3_q],
        "Bus 4": [b4_vm, b4_p, b4_q],
        "Bus 5": [b5_vm, b5_p, b5_q]
    }

    results = []
    attack_count = 0

    st.subheader("🚨 Detection Results")

    for bus, values in buses.items():

        vm, p, q = values
        status = predict_attack(vm, p, q)

        results.append([bus, vm, p, q, status])

        if status == "ATTACKED":
            st.error(f"🔴 {bus}: ATTACKED 🚨")
            attack_count += 1

        elif status == "Normal":
            st.success(f"🟢 {bus}: Normal ✅")

        else:
            st.warning(f"🟡 {bus}: Warning")

    # -------------------- DATAFRAME --------------------
    df = pd.DataFrame(results, columns=["Bus", "Voltage", "Power MW", "Reactive Power", "Status"])

    st.markdown("---")
    st.subheader("📊 Grid Data Table")
    st.dataframe(df, use_container_width=True)

    # -------------------- BAR GRAPH --------------------
    st.subheader("📈 Bus Power Analysis")

    fig = px.bar(
        df,
        x="Bus",
        y=["Power MW", "Reactive Power"],
        barmode="group",
        title="Bus Power Comparison"
    )

    fig.update_layout(
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------- PIE CHART --------------------
    st.subheader("📌 Attack Summary")

    pie_df = pd.DataFrame({
        "Status": ["Attacked", "Safe"],
        "Count": [attack_count, 4 - attack_count]
    })

    pie = px.pie(
        pie_df,
        names="Status",
        values="Count",
        title="Grid Security Status"
    )

    pie.update_layout(
        paper_bgcolor="#0f172a",
        font_color="white"
    )

    st.plotly_chart(pie, use_container_width=True)

    # -------------------- ALERT SOUND --------------------
    if attack_count > 0:

        st.warning("⚠️ Grid is under potential cyber attack!")

        audio_path = "siren.mp3"

        if os.path.exists(audio_path):
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            b64 = base64.b64encode(audio_bytes).decode()

            st.markdown(
                f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """,
                unsafe_allow_html=True
            )

    else:
        st.success("✅ Grid is operating normally.")

    # -------------------- METRICS --------------------
    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Total Buses", 4)

    with c2:
        st.metric("Attacked Buses", attack_count)

