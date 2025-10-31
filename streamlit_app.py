import streamlit as st
import pandas as pd
import re

# Add funny animation background
st.markdown(
    """
    <style>
    body {
        background-color: #f0f8ff;
        overflow: hidden;
    }
    .circle {
        position: absolute;
        border-radius: 50%;
        animation: bounce 4s infinite;
    }
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-100px);
        }
    }
    .circle1 {
        width: 100px;
        height: 100px;
        background-color: rgba(255, 0, 0, 0.5);
        top: 20%;
        left: 10%;
        animation-delay: 0s;
    }
    .circle2 {
        width: 150px;
        height: 150px;
        background-color: rgba(0, 255, 0, 0.5);
        top: 50%;
        left: 30%;
        animation-delay: 1s;
    }
    .circle3 {
        width: 80px;
        height: 80px;
        background-color: rgba(0, 0, 255, 0.5);
        top: 70%;
        left: 70%;
        animation-delay: 2s;
    }
    </style>
    <div class="circle circle1"></div>
    <div class="circle circle2"></div>
    <div class="circle circle3"></div>
    """,
    unsafe_allow_html=True
)

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
    st.header("Profit Center Check")
    uploaded_file_pc = st.file_uploader("Upload your Excel file for profit center check", type=["xlsx"])
    if uploaded_file_pc:
        df_pc = pd.read_excel(uploaded_file_pc)
        result = check_profit_center(df_pc)
        if result is not None:
            st.write("Profit Center Check Results:", result)
        else:
            st.error("Column 'Profit Center' not found in your file.")

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
