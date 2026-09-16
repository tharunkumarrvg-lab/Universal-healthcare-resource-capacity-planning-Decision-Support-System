import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Hospital Capacity DSS")

st.title("🏥 Universal Healthcare Capacity DSS")
st.markdown("""
### 📖 The Organizational Problem
The hospital is experiencing an unprecedented surge in emergency admissions. 
* **Baseline Capacity:** 239 Standard Beds | 31 ICU Beds.
* **The Threat:** Simulation logic indicates a high probability of breaching max capacity, leading to critical care delays.

### 💡 The DSS Solution (Scenario Analysis)
Use the **Decision Controls (+ / -)** on the left to allocate emergency resources, convert idle floor space, and optimize the operational budget.
---""")

try:
    # Read the simulation data early to calculate idle beds dynamically
    df = pd.read_csv('simulation_results.csv')
    max_std_used = df['Standard_Beds_Occupied'].max()
    baseline_idle = max(0, 239 - max_std_used)

    # --- DECISION CONTROLS (NUMBER INPUTS) ---
    st.sidebar.header("⚙️ Decision Controls")
    
    st.sidebar.subheader("External Rentals")
    rent_standard = st.sidebar.number_input("Rent New Standard Beds ($500/ea)", min_value=0, value=0, step=5)
    rent_icu = st.sidebar.number_input("Rent New ICU Units ($2,000/ea)", min_value=0, value=0, step=5)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Strategic Conversion")
    st.sidebar.markdown("Convert unused standard floor space into makeshift ICU environments.")
    convert_beds = st.sidebar.number_input("Convert Idle Std Beds ($800/ea)", min_value=0, max_value=int(baseline_idle), value=0, step=1)

    # --- DYNAMIC CAPACITY CALCULATIONS ---
    simulated_standard_capacity = 239 + rent_standard - convert_beds
    simulated_icu_capacity = 31 + rent_icu + convert_beds
    current_idle = baseline_idle + rent_standard - convert_beds

    # --- DSS STRATEGIC SUGGESTION ---
    st.info(f"💡 **DSS Strategic Suggestion:** The predictive simulation detects **{baseline_idle}** unused standard beds during peak surge. Converting these to makeshift ICU units saves $1,200 per bed compared to external rentals.")

    # --- LIVE RESOURCE METRICS ---
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Active Standard Capacity", simulated_standard_capacity, delta=f"{rent_standard - convert_beds} from baseline")
    col_m2.metric("Active ICU Capacity", simulated_icu_capacity, delta=f"{rent_icu + convert_beds} from baseline")
    col_m3.metric("Idle Standard Beds (Buffer)", current_idle, delta=f"{-convert_beds} converted", delta_color="inverse")

    st.markdown("---")

    # --- FULL-WIDTH DATA VISUALIZATION ---
    st.subheader("ICU Bed Utilization (24h Surge)")
    fig2, ax2 = plt.subplots(figsize=(12, 4))
    ax2.plot(df['Hour'], df['ICU_Beds_Occupied'], marker='o', color='#ff7f0e', label='Active ICU Patients')
    ax2.axhline(y=simulated_icu_capacity, color='red', linestyle='--', linewidth=2, label=f'Decision Limit ({simulated_icu_capacity})')
    ax2.fill_between(df['Hour'], df['ICU_Beds_Occupied'], simulated_icu_capacity, where=(df['ICU_Beds_Occupied'] > simulated_icu_capacity), color='red', alpha=0.3)
    ax2.set_xlabel("Hour of Day")
    ax2.set_ylabel("Occupied ICU Beds")
    ax2.legend()
    st.pyplot(fig2)

    st.subheader("Standard Bed Utilization (24h Surge)")
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    ax1.plot(df['Hour'], df['Standard_Beds_Occupied'], marker='o', color='#1f77b4', label='Active Patients')
    ax1.axhline(y=simulated_standard_capacity, color='red', linestyle='--', linewidth=2, label=f'Decision Limit ({simulated_standard_capacity})')
    ax1.fill_between(df['Hour'], df['Standard_Beds_Occupied'], simulated_standard_capacity, where=(df['Standard_Beds_Occupied'] > simulated_standard_capacity), color='red', alpha=0.3)
    ax1.set_xlabel("Hour of Day")
    ax1.set_ylabel("Occupied Beds")
    ax1.legend()
    st.pyplot(fig1)

    # --- FINANCIAL IMPACT ---
    st.markdown("### 💰 Financial Impact")
    total_cost = (rent_standard * 500) + (rent_icu * 2000) + (convert_beds * 800)

    col3, col4 = st.columns(2)
    with col3:
        st.success("📊 **Emergency Operational Costs (24h)**")
        st.metric(label="Standard Bed Rentals", value=f"${rent_standard * 500:,}")
        st.metric(label="ICU Unit Rentals", value=f"${rent_icu * 2000:,}")
        st.metric(label="Makeshift Conversion Cost", value=f"${convert_beds * 800:,}")
        st.metric(label="Total Required Budget", value=f"${total_cost:,}", delta="Funds Allocated", delta_color="inverse")

    with col4:
        # OUTCOME EVALUATION
        df['Dynamic_Std_Breach'] = df['Standard_Beds_Occupied'] > simulated_standard_capacity
        df['Dynamic_ICU_Breach'] = df['ICU_Beds_Occupied'] > simulated_icu_capacity
        dynamic_breaches = df[(df['Dynamic_Std_Breach'] == True) | (df['Dynamic_ICU_Breach'] == True)]
        
        if not dynamic_breaches.empty:
            st.error(f"❌ **SYSTEM FAILURE:** Proposed resource allocation is insufficient. Maximum capacity breached during {len(dynamic_breaches)} hourly periods.")
        else:
            st.success("✅ **SYSTEM OPTIMIZED:** The proposed capacity adjustments successfully absorb the patient surge.")

except FileNotFoundError:
    st.warning("Simulation data not found. Please run the backend simulation cell first.")
