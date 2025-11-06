import pandas as pd

# Profit Center Mapping
profit_center_mapping = {
    1002: 'PC016',
    1003: 'PC009',
    1004: 'PC009',
    1005: 'PC016',
    1007: 'PC021',
    1008: 'PC019',
    1009: 'PC020',
    1010: 'PC022',
    1011: 'PC016',
    1012: 'PC016',
    1013: 'PC016',
    1019: 'PC014',
    1020: 'PC014',
    1021: 'PC014',
    1022: 'PC014',
    1023: 'PC014',
    1024: 'PC014',
    1025: 'PC009',
    1026: 'PC009',
    1027: 'PC009',
    1028: 'PC009',
    1029: 'PC009',
    1030: 'PC016',
    1032: 'PC016',
    1035: 'PC009',
    1036: 'PC009',
    1037: 'PC016',
    1038: 'PC016',
    1039: 'PC014',
    1040: 'PC009',
    1041: 'PC019',
    1042: 'PC014',
    1043: 'PC009',
    1044: 'PC009',
    1045: 'PC009',
    1047: 'PC016',
    1101: 'PC017',
    1102: 'PC018',
    1201: 'PC011',
    1202: 'PC011',
    1301: 'PC012',
    1302: 'PC012',
    1303: 'PC012',
    1304: 'PC012',
    1401: 'PC013',
    1402: 'PC013',
    1500: 'PC031',
    1501: 'PC031',
    1502: 'PC031',
    1503: 'PC031',
    1504: 'PC031',
    1505: 'PC031',
    1506: 'PC031',
    1507: 'PC031'
}

def check_profit_centers(df):
    # Check if required columns are present
    profit_center_col = 'Profit Center' if 'Profit Center' in df.columns else 'PRCTR'
    plant_col = 'Plant' if 'Plant' in df.columns else 'WERKS'
    material_number_col = 'Material Number' if 'Material Number' in df.columns else 'MATNR'
    lvorm_col = 'LVORM' if 'LVORM' in df.columns else None
    mtart_col = 'MTART' if 'MTART' in df.columns else None  # New: material type column

    # Filter out rows where LVORM is 'X'
    if lvorm_col and lvorm_col in df.columns:
        df = df[df[lvorm_col] != 'X']

    # Filter out rows where MTART is 'NLAG' or 'DIEN' (out of scope)
    if mtart_col and mtart_col in df.columns:
        # Guard against non-string values and normalize case before comparison
        df = df[~df[mtart_col].astype(str).str.upper().isin(['NLAG', 'DIEN'])]

    if profit_center_col in df.columns and plant_col in df.columns and material_number_col in df.columns:
        # Initialize a list to store results
        results = []
        
        for index, row in df.iterrows():
            plant_code = row[plant_col]
            provided_profit_center = row[profit_center_col]
            material_number = row[material_number_col]
            expected_profit_center = profit_center_mapping.get(plant_code, 'PC016')  # Default to 'PC016' for other plants
            
            if provided_profit_center == expected_profit_center:
                results.append({'Material Number': material_number, 'Plant': plant_code, 'Profit Center': provided_profit_center, 'Check': 'Correct'})
            else:
                results.append({'Material Number': material_number, 'Plant': plant_code, 'Profit Center': provided_profit_center, 'Check': 'Incorrect', 'Expected': expected_profit_center})

        # Convert results to DataFrame
        results_df = pd.DataFrame(results)
        return results_df
    else:
        raise ValueError("Required columns not found in the DataFrame.")
