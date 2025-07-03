import streamlit as st

st.title("Antibody Dilution Calculator")

# Staining type: Single or Double
staining_type = st.selectbox("Staining type:", ["Single", "Double"])

# Inputs
total_volume = st.number_input("Total volume (µl):", min_value=0.0, value=1000.0, step=10.0)

# Antibody 1 dilution
ratio_input_1 = st.text_input("Antibody 1 dilution ratio (e.g., 1:500):", value="1:500")

# Antibody 2 only if double
if staining_type == "Double":
    ratio_input_2 = st.text_input("Antibody 2 dilution ratio (e.g., 1:1000):", value="1:1000")
else:
    ratio_input_2 = None  # Not used for single

# NGS percentage
ngs_percentage = st.number_input("NGS percentage (%):", min_value=0.0, max_value=100.0, value=10.0)

if st.button("Calculate"):
    try:
        # Parse Antibody 1
        num1, denom1 = ratio_input_1.split(':')
        num1 = float(num1.strip())
        denom1 = float(denom1.strip())
        if denom1 == 0:
            st.error("Antibody 1: Denominator cannot be zero.")
            st.stop()
        dilution_rate_1 = num1 / denom1

        antibody_1 = total_volume * dilution_rate_1

        # If Double staining, parse Antibody 2
        if staining_type == "Double":
            num2, denom2 = ratio_input_2.split(':')
            num2 = float(num2.strip())
            denom2 = float(denom2.strip())
            if denom2 == 0:
                st.error("Antibody 2: Denominator cannot be zero.")
                st.stop()
            dilution_rate_2 = num2 / denom2
            antibody_2 = total_volume * dilution_rate_2
        else:
            antibody_2 = 0

        ngs = total_volume * (ngs_percentage / 100)
        tbst = total_volume - ngs - antibody_1 - antibody_2

        if tbst < 0:
            st.warning("Warning: Total volume exceeded! Reduce antibody or NGS amounts.")
        else:
            st.success(
                f"""**TBST:** {tbst:.2f} µl  
            **NGS:** {ngs:.2f} µl  
            **Antibody 1:** {antibody_1:.2f} µl"""
                + (f"  \n**Antibody 2:** {antibody_2:.2f} µl" if staining_type == "Double" else "")
            )

    except Exception as e:
        st.error(f"Invalid input: {e}")