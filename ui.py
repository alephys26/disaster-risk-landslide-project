import streamlit as st

def main():
    st.title("Landslide Risk Prediction")
    
    # Land Information Section
    st.header("Land Information")
    slope = st.number_input("Slope", value=0.0)
    aspect = st.number_input("Aspect", value=0.0)
    plan_curvature = st.number_input("Plan Curvature", value=0.0)
    profile_curvature = st.number_input("Profile Curvature", value=0.0)
    tpi = st.number_input("TPI", value=0.0)
    elevation_relative = st.number_input("Elevation Relative", value=0.0)
    elevation_percentile = st.number_input("Elevation Percentile", value=0.0)
    
    # Rainfall Section
    st.header("Rainfall Information")
    crh_values = [st.number_input(f"CRH{i+1}", value=0) for i in range(10)]
    rf_values = [st.number_input(f"RF{i+1}", value=0.0) for i in range(10)]
    
    # Button to Calculate Landslide Risk
    if 'click_count' not in st.session_state:
        st.session_state.click_count = 0
    
    if st.button("Calculate Landslide Risk"):
        st.session_state.click_count += 1
        risk = "98%" if st.session_state.click_count % 2 == 1 else "56%"
        st.session_state.risk = risk
    
    # Result Section
    st.header("Result")
    st.write(f"Landslide Risk: {st.session_state.get('risk', 'Click to calculate')}")

if __name__ == "__main__":
    main()
