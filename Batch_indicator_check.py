import pandas as pd

def update_batch_indicator(df):
    # Filter out deleted materials
    df_active = df[df['LVORM'] != 'X']

    # Filter for material type 'Hawa' (assuming 1604 is correct)
    df_hawa = df_active[df_active['MATKL'] == 1604]

    # Segmentation Level 3 values to include
    segmentation_levels = [
        172, 173, 174, 175, 176, 177, 178, 179,
        180, 181, 137, 138, 139, 140, 141, 142, 143
    ]

    # Initialize an empty DataFrame for the report
    report = pd.DataFrame()

    # Check for Material Group = 1603 and Segmentation Level in the list, and Batch Indicator is 'Selected'
    df_selected = df_hawa[
        (df_hawa['MATKL'] == 1603) &
        (df_hawa['ZZ1_SEGMENTL3_PRD'].isin(segmentation_levels)) &
        (df_hawa['XCHPF'] == 'X')
    ]
    
    if not df_selected.empty:
        df_selected['Update'] = 'Update'
        report = pd.concat([report, df_selected[['MATNR', 'MATKL', 'ZZ1_SEGMENTL3_PRD', 'XCHPF', 'Update']]])

    # Check for Material Group = 1603 and Segmentation Level not in the list, and Batch Indicator is not 'Selected'
    df_not_selected = df_hawa[
        (df_hawa['MATKL'] == 1603) &
        (~df_hawa['ZZ1_SEGMENTL3_PRD'].isin(segmentation_levels)) &
        (df_hawa['XCHPF'] != 'X')
    ]
    
    if not df_not_selected.empty:
        df_not_selected['Update'] = 'Not Selected'
        report = pd.concat([report, df_not_selected[['MATNR', 'MATKL', 'ZZ1_SEGMENTL3_PRD', 'XCHPF', 'Update']]])

    return report
