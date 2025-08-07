
import streamlit as st
import pandas as pd

# Use relative path so it works on Streamlit Cloud
df = pd.read_csv("ece_subjects_all_years_FINAL_BIOMED_HOTFIX.csv")

st.set_page_config(page_title="ECE Subject Selector", layout="wide")
st.title("📚 ECE Subject Selector")
st.caption("Select subjects from any year and term. Maximum of 21 units.")

# Track selected subjects
selected_rows = []
total_units = 0.0
unit_status_placeholder = st.empty()

# Specialization block (separate section)
st.markdown("## 🔬 Specialization Subjects")
specialization_codes = ["ECESPEC1", "ECESPEC2", "ECESPEC3"]
spec_df = df[df["Course Code"].isin(specialization_codes)]

for idx, row in spec_df.iterrows():
    label = f"{row['Course Code']} - {row['Course Title']} ({row['Credit Units']} units)"
    if st.checkbox(label, key=f"spec_{row['Course Code']}_{idx}"):
        selected_rows.append(row)
        total_units += row["Credit Units"]

# Display subjects grouped by Year → Term (excluding specializations)
for year in sorted(df["Year"].unique()):
    year_df = df[(df["Year"] == year) & (~df["Course Code"].isin(specialization_codes))]
    if year_df.empty:
        continue
    st.markdown(f"## 🧭 Year {year}")

    for term in sorted(year_df["Term"].unique()):
        term_df = year_df[year_df["Term"] == term]
        with st.expander(f"📘 Term {term}", expanded=bool((year == 1) and (term == 1))):
            for idx, row in term_df.iterrows():
                label = f"{row['Course Code']} - {row['Course Title']} ({row['Credit Units']} units)"
                if st.checkbox(label, key=f"{row['Course Code']}_{idx}"):
                    selected_rows.append(row)
                    total_units += row["Credit Units"]

# Display total unit summary
st.markdown("---")
st.subheader(f"🎓 Total Units Selected: {total_units:.2f}")

# Updated unit logic
if total_units > 21:
    unit_status_placeholder.error("❌ OVERLOAD!")
elif total_units >= 16:
    unit_status_placeholder.success("✅ EXACT LOAD")
elif total_units > 0:
    unit_status_placeholder.warning("⚠️ UNDERLOAD BUT APPLICABLE")
else:
    unit_status_placeholder.info("ℹ️ No subjects selected.")

# Display selected subject table
if selected_rows:
    st.markdown("### 📋 Selected Subjects")
    selected_df = pd.DataFrame(selected_rows)
    st.dataframe(selected_df[["Course Code", "Course Title", "Lec Hrs", "Lab Hrs", "Credit Units"]])
else:
    st.info("No subjects selected yet.")
