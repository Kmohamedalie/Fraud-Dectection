import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime

# --- CONFIGURATION & UI SETUP ---
st.set_page_config(
    page_title="Real-Time Fraud Monitoring Dashboard",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Live Financial Transaction Fraud Monitoring")
st.markdown("This dashboard simulates a live real-time stream of credit card transactions and flags anomalies instantly.")

# Initialize session state for storing historical live data stream
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = pd.DataFrame(columns=[
        "Timestamp", "Transaction_ID", "User_ID", "Amount", "Location", "Is_Fraud", "Risk_Score"
    ])

# --- HELPER FUNCTIONS ---
def generate_mock_transaction():
    """Generates a single synthetic transaction with occasional fraudulent behavior."""
    is_fraud = np.random.choice([0, 1], p=[0.94, 0.06])  # 6% fraud rate simulation
    
    if is_fraud:
        amount = round(float(np.random.uniform(800, 5000)), 2)  # High transaction amounts
        location = np.random.choice(["International/Proxy", "Unknown IP", "Suspicious Merchant"])
        risk_score = round(float(np.random.uniform(75, 99.9)), 1)
    else:
        amount = round(float(np.random.exponential(scale=50) + 5), 2)  # Mostly small daily amounts
        location = np.random.choice(["New York", "London", "Paris", "Tokyo", "San Francisco"])
        risk_score = round(float(np.random.uniform(0, 30)), 1)
        
    return {
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "Transaction_ID": f"TX{np.random.randint(100000, 999999)}",
        "User_ID": f"USR{np.random.randint(1000, 9999)}",
        "Amount": amount,
        "Location": location,
        "Is_Fraud": is_fraud,
        "Risk_Score": risk_score
    }

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Dashboard Controls")
run_simulation = st.sidebar.toggle("Start Live Monitoring Stream", value=True)
simulation_speed = st.sidebar.slider("Stream Speed (Seconds per TX)", 0.1, 2.0, 0.5)
clear_data = st.sidebar.button("Clear Dashboard Data")

if clear_data:
    st.session_state.transaction_history = pd.DataFrame(columns=[
        "Timestamp", "Transaction_ID", "User_ID", "Amount", "Location", "Is_Fraud", "Risk_Score"
    ])
    st.rerun()

# --- LIVE DASHBOARD CONTAINERS ---
# We use empty containers so placeholders dynamically re-render on screen
metric_row = st.empty()
chart_row = st.empty()
log_row = st.empty()

# --- CONTINUOUS STREAM LOOP ---
while run_simulation:
    new_tx = generate_mock_transaction()
    
    # OLD CODE:
    # st.session_state.transaction_history = pd.concat([
    #     pd.DataFrame([new_tx]), st.session_state.transaction_history
    # ]).head(100)
    
    # NEW FIXED CODE:
    st.session_state.transaction_history = pd.concat([
        pd.DataFrame([new_tx]), st.session_state.transaction_history
    ]).reset_index(drop=True).head(100) # Added .reset_index(drop=True) here!
    
    df = st.session_state.transaction_history
    
    # Calculate key metrics
    total_tx = len(df)
    fraud_df = df[df["Is_Fraud"] == 1]
    total_fraud = len(fraud_df)
    fraud_rate = (total_fraud / total_tx * 100) if total_tx > 0 else 0
    total_volume = df["Amount"].sum()
    
    # 3. Update Metric Cards
    with metric_row.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Processed (Window)", f"{total_tx}")
        col2.metric("Fraud Alerts Detected", f"{total_fraud}", delta=f"+1" if new_tx["Is_Fraud"] == 1 else None, delta_color="inverse")
        col3.metric("Current Fraud Rate", f"{fraud_rate:.1f}%")
        col4.metric("Monitored Volume", f"${total_volume:,.2f}")
        
    # 4. Update Charts
    with chart_row.container():
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Live Risk Score vs Transaction Amount")
            fig_scatter = px.scatter(
                df, x="Amount", y="Risk_Score", color=df["Is_Fraud"].astype(str),
                color_discrete_map={"0": "#1f77b4", "1": "#ef553b"},
                labels={"color": "Flagged Fraud"},
                title="Real-time Anomaly Cluster Mapping"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col_right:
            st.subheader("Alert Breakdown by Location")
            if total_fraud > 0:
                fig_pie = px.pie(fraud_df, names="Location", title="High Risk Locations Source")
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No fraudulent activities detected yet in this stream window.")

    # 5. Update Live Alert Logs
    with log_row.container():
        st.subheader("Activity Feed (Latest First)")
        
        # Color code rows or safely display dataframes
        def highlight_fraud(row):
            return ['background-color: #ffcccc' if row.Is_Fraud == 1 else '' for _ in row]
        
        styled_df = df.style.apply(highlight_fraud, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=300)
        
    # Pause for specified interval before repeating the loop
    time.sleep(simulation_speed)
    st.rerun()

# If user turns off the toggle
if not run_simulation:
    st.info("Streaming paused. Toggle 'Start Live Monitoring Stream' in the sidebar to resume.")
