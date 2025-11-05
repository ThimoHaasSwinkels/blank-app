import streamlit as st
import pandas as pd
import re

# Import the batch indicator function
from Batch_indicator_check import update_batch_indicator
from Profit_center_check import check_profit_centers

# Define the mapping for legal entity abbreviations
abbreviation_map = {
    r'\bnv\b|n\.v\.|nv\.': 'N.V.',
    r'\bbv\b|b\.v\.|bv\.': 'B.V.',
    r'\bcvba\b|c\.v\.b\.a\.|cvba\.': 'C.V.B.A.',
    r'\bvzw\b|v\.z\.w\.|vzw\.': 'V.Z.W.',
    r'\bsa\b|s\.a\.|sa\.': 'S.A.',
    r'\bsrl\b|s\.r\.l\.|srl\.': 'S.R.L.',
    r'\bsprl\b|s\.p\.r\.l\.|sprl\.': 'S.P.R.L.',
    r'\bltd\b|ltd\.': 'Ltd.',
    r'\bllc\b|llc\.': 'LLC',
    r'\bgmbh\b|gmbh\.': 'GmbH',
    r'\bvof\b|v\.o\.f\.|vof\.': 'V.O.F.',
    r'\bbvba\b|b\.v\.b\.a\.|bvba\.': 'B.V.B.A.'
}

# Function to standardise names
def standardise_name(name):
    def title_except_abbr(word):
        for pattern, replacement in abbreviation_map.items():
            if re.match(pattern, word, re.IGNORECASE):
                return replacement
        return word.capitalize()

    name = re.sub(r'\s+', ' ', name).strip()
    for pattern, replacement in abbreviation_map.items():
        name = re.sub(pattern, replacement, name, flags=re.IGNORECASE)
    
    words = name.split()
    processed_words = [title_except_abbr(word) for word in words]
    name = ' '.join(processed_words)
    name = re.sub(r'\.(?=\.)', '', name)
    
    return name

# Function to check profit center
def check_profit_center(df):
    if 'Profit Center' in df.columns:
        df['Profit Center Check'] = df['Profit Center'].apply(lambda x: 'Correct' if x == 'ExpectedValue' else 'Incorrect')
        return df[['Profit Center', 'Profit Center Check']]
    else:
        return None

st.title("Data Quality Tool")

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Material Master Data", "Business Partner Master Data"])

# Material Master Data Tab
with tab1:
    st.header("Material Master Data Checks")
    
    # Dropdown menu for selecting the type of check
    check_type = st.selectbox("Select the check to perform:", ["Profit Center Check", "Batch Indicator Check", "Base Unit of Measure Check"])
    
    # Profit Center Check
    if check_type == "Profit Center Check":
        uploaded_file_pc = st.file_uploader("Upload your Excel file for profit center check", type=["xlsx"])
        if uploaded_file_pc:
            try:
                result_df = check_profit_centers(uploaded_file_pc)  # Call the correct function
                if not result_df.empty:
                    st.write("Incorrect Profit Center Check Results:")
                    st.dataframe(result_df)  # Display the results in a dataframe
                else:
                    st.success("All profit centers are correct.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Batch Indicator Check
    elif check_type == "Batch Indicator Check":
        uploaded_file_batch = st.file_uploader("Upload your Excel file for batch indicator check", type=["xlsx"])
        if uploaded_file_batch:
            df_batch = pd.read_excel(uploaded_file_batch)
            report = update_batch_indicator(df_batch)
            
            if not report.empty:
                st.write("Batch Indicator Check Results:", report)
                output_file = "Batch_Indicator_Report.xlsx"
                report.to_excel(output_file, index=False)
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="Download Batch Indicator Report",
                        data=f,
                        file_name=output_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.error("No data found matching the criteria.")

    # Base Unit of Measure Check (Placeholder for future implementation)
    elif check_type == "Base Unit of Measure Check":
        uploaded_file_bum = st.file_uploader("Upload your Excel file for base unit of measure check", type=["xlsx"])
        if uploaded_file_bum:
            df_bum = pd.read_excel(uploaded_file_bum)
            # Implement your base unit of measure check logic here
            st.write("Base Unit of Measure Check is not yet implemented.")

# Business Partner Master Data Tab
with tab2:
    st.header("BP Name Standardisation")
    uploaded_file_bp = st.file_uploader("Upload your Excel file for standardisation", type=["xlsx"])
    if uploaded_file_bp:
        df_bp = pd.read_excel(uploaded_file_bp)
        if 'Name' in df_bp.columns:
            df_bp['Name_Standardised'] = df_bp['Name'].astype(str).apply(standardise_name)
            st.write("Preview of standardised names:", df_bp[['Name', 'Name_Standardised']].head())
            
            output_file = "BP_Names_Standardised.xlsx"
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df_bp.to_excel(writer, index=False)
            
            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download Standardised Excel",
                    data=f,
                    file_name=output_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("Column 'Name' not found in your file.")
