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

# Add a set of words that should always be uppercase
always_uppercase = {'DC', 'IT', 'HR', 'CEO', 'CFO', 'CTO', 'COO'}

def standardise_name(name):
    def title_except_abbr(word):
        # Check for legal entity abbreviations
        for pattern, replacement in abbreviation_map.items():
            if re.match(pattern, word, re.IGNORECASE):
                return replacement
        return word.capitalize()

    # Step 1: Normalize spaces and punctuation
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Step 2: Standardise abbreviations
    for pattern, replacement in abbreviation_map.items():
        name = re.sub(pattern, replacement, name, flags=re.IGNORECASE)
    
    # Step 3: Split and process words
    words = name.split()
    processed_words = [title_except_abbr(word) for word in words]
    
    name = ' '.join(processed_words)
    
    # Step 4: Remove duplicate periods in abbreviations
    name = re.sub(r'\.(?=\.)', '', name)
    
    return name

# Function to check profit center
def check_profit_center(df):
    # Assuming 'Profit Center' is a column in the DataFrame
    if 'Profit Center' in df.columns:
        # Perform your checks here (this is just a placeholder)
        df['Profit Center Check'] = df['Profit Center'].apply(lambda x: 'Correct' if x == 'ExpectedValue' else 'Incorrect')
        return df[['Profit Center', 'Profit Center Check']]
    else:
        return None

st.title("Data Quality Tool")

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["BP Name Standardisation", "Profit Center Check"])

with tab1:
    uploaded_file = st.file_uploader("Upload your Excel file for standardisation", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if 'Name' in df.columns:
            df['Name_Standardised'] = df['Name'].astype(str).apply(standardise_name)
            st.write("Preview of standardised names:", df[['Name', 'Name_Standardised']].head())
            
            # Create a BytesIO object to save the Excel file in memory
            output_file = "BP_Names_Standardised.xlsx"
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            
            # Read the file back into memory
            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download Standardised Excel",
                    data=f,
                    file_name=output_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("Column 'Name' not found in your file.")

with tab2:
    uploaded_file_pc = st.file_uploader("Upload your Excel file for profit center check", type=["xlsx"])
    if uploaded_file_pc:
        df_pc = pd.read_excel(uploaded_file_pc)
        result = check_profit_center(df_pc)
        if result is not None:
            st.write("Profit Center Check Results:", result)
        else:
            st.error("Column 'Profit Center' not found in your file.")
