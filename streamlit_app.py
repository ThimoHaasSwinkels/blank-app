import streamlit as st
import pandas as pd
import re

# Add beer pouring animation using HTML and CSS
st.markdown(
    """
    <style>
    body {
        background-color: #f0f8ff;
        overflow: hidden;
    }
    .container {
        position: relative;
        width: 200px;
        height: 300px;
        margin: auto;
    }
    .bottle {
        position: absolute;
        width: 40px;
        height: 120px;
        background-color: #8B4513; /* Brown color for the bottle */
        border-radius: 10px;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        animation: pour 3s infinite;
    }
    .bottle:before {
        content: '';
        position: absolute;
        width: 0;
        height: 0;
        border-left: 20px solid transparent;
        border-right: 20px solid transparent;
        border-bottom: 20px solid #8B4513; /* Bottle cap */
        top: -20px;
        left: 0;
    }
    .glass {
        position: absolute;
        width: 80px;
        height: 100px;
        background-color: #fff;
        border: 5px solid #000;
        border-radius: 10px;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
    }
    .beer {
        position: absolute;
        width: 80px;
        height: 0;
        background-color: #FFD700; /* Beer color */
        border-radius: 10px;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        animation: fill 3s infinite;
    }
    @keyframes pour {
        0% { transform: translateX(-50%) rotate(0deg); }
        50% { transform: translateX(-50%) rotate(-30deg); }
        100% { transform: translateX(-50%) rotate(0deg); }
    }
    @keyframes fill {
        0% { height: 0; }
        50% { height: 80px; }
        100% { height: 0; }
    }
    </style>
    <div class="container">
        <div class="bottle"></div>
        <div class="glass">
            <div class="beer"></div>
        </div>
    </div>
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
