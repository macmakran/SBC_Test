# SBC_Test

# 🏗️ SPT Safe Bearing Capacity (SBC) Calculator

A web-based SBC calculator using Standard Penetration Test (SPT) values based on IS 2131. This tool is built using **Streamlit** and allows you to:

- Input site-specific soil and test parameters
- Calculate Safe Bearing Capacity (SBC)
- Apply overburden and dilatancy corrections
- Generate and download professional PDF reports

---

## 🧰 Features

- Calculates SBC using corrected SPT N-values
- Includes overburden and dilatancy corrections
- Displays effective stress, correction factor, and all intermediate results
- Reference soil weight table
- PDF Report Generation with:
  - Input summary
  - Output summary
  - Timestamp
  - Company name: **NCC Co & Lab Pvt Ltd**

---

## 📦 Requirements

- Python 3.7+
- pip

### 🔧 Install Dependencies

```bash
pip install streamlit pandas fpdf

Once launched, the app will open in your browser at http://localhost:8501.

streamlit run app.py


The calculator applies the following steps:

Effective Overburden Pressure:

If test depth is above water table:

vbnet
Copy
Edit
σ' = γ_moist × depth
If below water table:

vbnet
Copy
Edit
σ' = (γ_moist × water_table) + (γ_sub × (depth - water_table))
Overburden Correction:

mathematica
Copy
Edit
N₁ = N × sqrt(p_ref / σ')
Dilatancy Correction (for saturated fine sands & silts):

mathematica
Copy
Edit
If N₁ > 15 → N₂ = 15 + 0.5 × (N₁ - 15)
Else → N₂ = N₁
SBC Calculation:

ini
Copy
Edit
SBC = 10 × N₂ (in kN/m²)
📄 PDF Report
The generated report includes:

Project date and time

Input parameters

Intermediate calculations

Final SBC value

Company branding (NCC Co & Lab Pvt Ltd)

Click the "📄 Download PDF Report" button in the app to get your report.

🏢 About
This calculator is developed for NCC Co & Lab Pvt Ltd to assist field and design engineers in quick, IS-compliant estimation of safe bearing capacity based on SPT data.

⚠️ Disclaimer: Always consult a geotechnical engineer for detailed soil investigations and critical foundation designs.

📬 Feedback
If you'd like to contribute or report an issue, feel free to open a pull request or contact the developer.

yaml
Copy
Edit

---

Would you like me to generate this as a downloadable `.md` file or include a project logo/image
