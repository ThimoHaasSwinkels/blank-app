import streamlit as st
import pandas as pd
import re

# Import the batch indicator function
from Batch_indicator_check import update_batch_indicator

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
    st.header("Profit Center Check and Batch Indicator Check")
    
    # Profit Center Check
    uploaded_file_pc = st.file_uploader("Upload your Excel file for profit center check", type=["xlsx"], key="pc_uploader")
    if uploaded_file_pc:
        df_pc = pd.read_excel(uploaded_file_pc)
        result = check_profit_center(df_pc)
        if result is not None:
            st.write("Profit Center Check Results:", result)
        else:
            st.error("Column 'Profit Center' not found in your file.")

    # Batch Indicator Check
    uploaded_file_batch = st.file_uploader("Upload your Excel file for batch indicator check", type=["xlsx"], key="batch_uploader")
    if uploaded_file_batch:
        df_batch = pd.read_excel(uploaded_file_batch)
        report = update_batch_indicator(df_batch)
        
        if not report.empty:
            st.write("Batch Indicator Check Results:", report)
            output_file
