import streamlit as st
import pandas as pd
import joblib
import os
import base64

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Power Grid Attack Detection",
    page_icon="⚡",
    layout="wide"
)

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

# -------------------- INPUT SECTION --------------------
st.subheader("📥 Enter Bus Parameters")
col1, col2, col3, col4 = st.columns(4)

with col1:
    b2_vm = st.number_input("Bus 2 vm_pu", key="b2_vm")
    b2_p = st.number_input("Bus 2 p_mw", key="b2_p")
    b2_q = st.number_input("Bus 2 q_mvar", key="b2_q")

with col2:
    b3_vm = st.number_input("Bus 3 vm_pu", key="b3_vm")
    b3_p = st.number_input("Bus 3 p_mw", key="b3_p")
    b3_q = st.number_input("Bus 3 q_mvar", key="b3_q")

with col3:
    b4_vm = st.number_input("Bus 4 vm_pu", key="b4_vm")
    b4_p = st.number_input("Bus 4 p_mw", key="b4_p")
    b4_q = st.number_input("Bus 4 q_mvar", key="b4_q")

with col4:
    b5_vm = st.number_input("Bus 5 vm_pu", key="b5_vm")
    b5_p = st.number_input("Bus 5 p_mw", key="b5_p")
    b5_q = st.number_input("Bus 5 q_mvar", key="b5_q")

# -------------------- PREDICTION FUNCTION --------------------
def predict_attack(vm, p, q, bus_id):
    if vm <= 0 or p <= 0 or q <= 0 or bus_id <= 0:
        return "ATTACKED 🚨"
    elif vm >= 1 and p >= 1 and q >= 1 and bus_id >= 1:
        return "Normal ✅"
    else:
        return "⚠️ Warning"

# -------------------- ANALYZE BUTTON --------------------
if st.button("🚀 Analyze Grid"):
    buses = [
        ("Bus 2", b2_vm, b2_p, b2_q, 2),
        ("Bus 3", b3_vm, b3_p, b3_q, 3),
        ("Bus 4", b4_vm, b4_p, b4_q, 4),
        ("Bus 5", b5_vm, b5_p, b5_q, 5),
    ]

    attack_detected = False
    attack_count = 0

    st.subheader("🚨 Detection Results")
    for name, vm, p, q, bid in buses:
        result = predict_attack(vm, p, q, bid)
        if "ATTACKED" in result:
            st.error(f"🔴 {name}: {result}")
            attack_detected = True
            attack_count += 1
        elif "Normal" in result:
            st.success(f"🟢 {name}: {result}")
        else:
            st.warning(f"🟡 {name}: {result}")

    # -------------------- AUTOMATIC SIREN --------------------
    if attack_detected:
        st.warning("⚠️ Grid is under potential attack!")

        # -------------------- play MP3 automatically --------------------
        audio_file_name = "siren.mp3"  # exact name
        audio_path = os.path.join(os.path.dirname(__file__), audio_file_name)

        if os.path.exists(audio_path):
            # encode to base64
            audio_bytes = open("siren.mp3", "rb").read()
            b64_audio = base64.b64encode(audio_bytes).decode()
            st.markdown(
                f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                </audio>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error(f"Audio file not found: {audio_path}")

    else:
        st.success("✅ Grid is operating normally")

    # -------------------- SUMMARY --------------------
    st.subheader("📌 Summary")
    st.metric("Total Buses", 4)
    st.metric("Attacked Buses", attack_count)