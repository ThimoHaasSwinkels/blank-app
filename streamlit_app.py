import streamlit as st
import pandas as pd
import re

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

    name = re.sub(r'\s+', ' ', str(name)).strip()
    for pattern, replacement in abbreviation_map.items():
        name = re.sub(pattern, replacement, name, flags=re.IGNORECASE)
    
    words = name.split()
    processed_words = [title_except_abbr(word) for word in words]
    name = ' '.join(processed_words)
    name = re.sub(r'\.(?=\.)', '', name)
    
    return name

# Function to check profit center
def check_profit_center(df, expected_value):
    if 'Profit Center' in df.columns:
        # coerce to string to avoid dtype issues
        df['Profit Center Check'] = df['Profit Center'].astype(str).apply(
            lambda x: 'Correct' if x == str(expected_value) else 'Incorrect'
        )
        return df[['Profit Center', 'Profit Center Check', *[c for c in df.columns if c not in ['Profit Center', 'Profit Center Check']]]]
    else:
        return None

# Function to check base unit of measure
def check_base_unit_of_measure(df, expected_unit):
    if 'Base Unit of Measure' in df.columns:
        df['Base Unit Check'] = df['Base Unit of Measure'].astype(str).apply(
            lambda x: 'Correct' if x == str(expected_unit) else 'Incorrect'
        )
        return df[['Base Unit of Measure', 'Base Unit Check', *[c for c in df.columns if c not in ['Base Unit of Measure', 'Base Unit Check']]]]
    else:
        return None

st.title("Data Quality Tool")

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Material Master Data", "Business Partner Master Data"])

# Material Master Data Tab
with tab1:
    st.header("Material Master Data Checks")
    
    # Option to select the type of check
    check_type = st.selectbox("Select the check type:", ["Profit Center Check", "Base Unit of Measure Check"])
    
    uploaded_file_pc = st.file_uploader("Upload your Excel file for material master data", type=["xlsx"])
    if uploaded_file_pc:
        df_pc = pd.read_excel(uploaded_file_pc)
        total_rows = len(df_pc)
        st.info(f"Total observations in uploaded file: {total_rows}")
        
        if check_type == "Profit Center Check":
            expected_value = st.text_input("Expected Profit Center value", value="ExpectedValue")
            if st.button("Run Profit Center Check"):
                result = check_profit_center(df_pc.copy(), expected_value)
                if result is not None:
                    # compute counts
                    correct_count = (df_pc['Profit Center'].astype(str) == str(expected_value)).sum()
                    incorrect_count = total_rows - correct_count
                    st.write("Profit Center Check Results (preview):")
                    st.dataframe(result.head(50))
                    st.success(f"Correct: {correct_count} / {total_rows}")
                    st.warning(f"To change (Incorrect): {incorrect_count} / {total_rows}")
                else:
                    st.error("Column 'Profit Center' not found in your file.")
        
        elif check_type == "Base Unit of Measure Check":
            expected_unit = st.text_input("Expected Base Unit of Measure", value="ExpectedUnit")
            if st.button("Run Base Unit of Measure Check"):
                result = check_base_unit_of_measure(df_pc.copy(), expected_unit)
                if result is not None:
                    correct_count = (df_pc['Base Unit of Measure'].astype(str) == str(expected_unit)).sum()
                    incorrect_count = total_rows - correct_count
                    st.write("Base Unit of Measure Check Results (preview):")
                    st.dataframe(result.head(50))
                    st.success(f"Correct: {correct_count} / {total_rows}")
                    st.warning(f"To change (Incorrect): {incorrect_count} / {total_rows}")
                else:
                    st.error("Column 'Base Unit of Measure' not found in your file.")

# Business Partner Master Data Tab
with tab2:
    st.header("BP Name Standardisation")
    uploaded_file_bp = st.file_uploader("Upload your Excel file for standardisation", type=["xlsx"])
    if uploaded_file_bp:
        df_bp = pd.read_excel(uploaded_file_bp)
        total_rows_bp = len(df_bp)
        st.info(f"Total observations in uploaded file: {total_rows_bp}")
        if 'Name' in df_bp.columns:
            df_bp['Name_Standardised'] = df_bp['Name'].astype(str).apply(standardise_name)
            changed_mask = df_bp['Name'].astype(str) != df_bp['Name_Standardised']
            changed_count = changed_mask.sum()
            st.write("Preview of standardised names:")
            st.dataframe(df_bp[['Name', 'Name_Standardised']].head(50))
            st.success(f"Unchanged: {total_rows_bp - changed_count} / {total_rows_bp}")
            st.warning(f"To change (different after standardisation): {changed_count} / {total_rows_bp}")
            
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
