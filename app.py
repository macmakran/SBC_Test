import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import io

# Page configuration
st.set_page_config(page_title="SPT SBC Calculator", page_icon="🏗️")
st.title("Safe Bearing Capacity Calculator (IS 2131)")
st.write("This app calculates Safe Bearing Capacity (SBC) using SPT N-value with corrections for overburden and dilatancy.")

# Company header
st.markdown("### 🏢 NCC Co & Lab Pvt Ltd")

# Reference data table
st.subheader("Typical Soil Unit Weights (kN/m³)")
soil_data = {
    "Soil Type": ["Sandy Soil", "Clayey Soil", "Silty Soil", "Gravel"],
    "Moist Weight": ["16–20", "14–18", "15–19", "19–22"],
    "Submerged Weight": ["9–11", "6–8", "7–9", "10–12"]
}
df = pd.DataFrame(soil_data)
st.table(df)
st.caption("Reference pressure for overburden correction is typically 100 kN/m²")

# Input sidebar
with st.sidebar:
    st.header("Input Parameters")
    moist_unit = st.number_input("Moist Unit Weight (kN/m³)", 10.0, 25.0, 18.0, 0.5)
    submerged_unit = st.number_input("Submerged Unit Weight (kN/m³)", 5.0, 15.0, 8.0, 0.5)
    ref_pressure = st.number_input("Reference Pressure (kN/m²)", 50, 200, 100, 10)
    st.divider()
    water_table = st.number_input("Water Table Depth (m)", 0.0, value=2.0, step=0.5)
    test_depth = st.number_input("Test Depth (m)", 0.5, value=3.0, step=0.5)
    blows = st.number_input("Blows per 30 cm (N-value)", 1, 100, 25)

# Calculations
try:
    if test_depth <= water_table:
        effective_stress = moist_unit * test_depth
    else:
        effective_stress = (moist_unit * water_table) + (submerged_unit * (test_depth - water_table))

    correction_factor = min(max((ref_pressure / effective_stress) ** 0.5, 0.45), 2.0)
    corrected_n1 = blows * correction_factor

    if test_depth > water_table and corrected_n1 > 15:
        corrected_n2 = 15 + 0.5 * (corrected_n1 - 15)
    else:
        corrected_n2 = corrected_n1

    sbc = 10 * corrected_n2

except ZeroDivisionError:
    st.error("Error: Test depth cannot be zero for stress calculation")

else:
    st.subheader("Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Effective Stress", f"{effective_stress:.2f} kN/m²")
    with col2:
        st.metric("Correction Factor", f"{correction_factor:.2f}")
    with col3:
        st.metric("Corrected N-value", f"{corrected_n2:.2f}")

    st.divider()
    st.success(f"## Safe Bearing Capacity (SBC): {sbc:.2f} kN/m²")

    with st.expander("Show calculation details"):
        st.write(f"""
        - Raw N-value: {blows}
        - Overburden Corrected N-value: {corrected_n1:.2f}
        - Final Corrected N-value: {corrected_n2:.2f}
        - SBC Formula: 10 × N = 10 × {corrected_n2:.2f}
        """)

    # PDF Report Generation
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "NCC Co & Lab Pvt Ltd", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, "SPT-Based Safe Bearing Capacity Report", ln=True, align='C')
        pdf.ln(10)
        
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        pdf.cell(200, 10, f"Date: {date_str}", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Input Parameters", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, f"""
Moist Unit Weight: {moist_unit} kN/m³
Submerged Unit Weight: {submerged_unit} kN/m³
Reference Pressure: {ref_pressure} kN/m²
Water Table Depth: {water_table} m
Test Depth: {test_depth} m
Raw N-value: {blows}
""")
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Results", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, f"""
Effective Stress: {effective_stress:.2f} kN/m²
Correction Factor: {correction_factor:.2f}
Corrected N-value: {corrected_n2:.2f}
Safe Bearing Capacity (SBC): {sbc:.2f} kN/m²
""")
        pdf.set_font("Arial", 'I', 10)
        pdf.ln(5)
        pdf.cell(0, 10, "Note: Based on IS 2131 - Always verify with a geotechnical engineer.", ln=True)

        # ✅ Export as string and encode to bytes
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        return pdf_bytes

    st.download_button(
    label="📄 Download PDF Report",
    data=generate_pdf(),
    file_name="SBC_Report_NCC_Lab.pdf",
    mime="application/pdf"
)
st.caption("Note: This calculator follows IS 2131 guidelines for SPT-based bearing capacity estimation. "
           "Always verify with a geotechnical engineer for critical projects.")
