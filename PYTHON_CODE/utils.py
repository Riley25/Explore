##############################
#
#  NAME: utils.py
#  
#  PURPOSE: 
#           load_excel   ()

import pandas as pd
import numpy as np


def load_excel(uploaded_file):
    """
    Load an Excel file into a Pandas DataFrame.
    
    Parameters:
        uploaded_file: File-like object (Streamlit file uploader).
        
    Returns:
        pd.DataFrame: DataFrame containing the Excel data.
    """
    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        
        return df
    
    except Exception as e:
        raise ValueError(f"Error loading Excel file: {e}")
    

def bar_chart_data(dfc, var_name, top_n_rows = 6):
    """
    Efficiently generate bar chart data with counts, cumulative probability, and sorting.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        var_name (str): Column name to group by.

    Returns:
        pd.DataFrame: Processed DataFrame with top 6 counts and cumulative probabilities.
    """
    
    dfc[var_name] = dfc[var_name].fillna("N/A").astype(str)
    
    # Step 1: Group and count occurrences directly
    pivot_table = (
        dfc.groupby(var_name, as_index=False)
        .size()
        .rename(columns={'size': 'Occurrences'})
        .sort_values(by='Occurrences', ascending=False, ignore_index=True)
    )

    # Step 2: Calculate cumulative probabilities
    total_count = pivot_table['Occurrences'].sum()
    pivot_table['Percentage'] = ((pivot_table['Occurrences'] / total_count).round(4))*100
    pivot_table['Cumulative Percentage'] = ((pivot_table['Occurrences'] / total_count).cumsum().round(4))*100
    del(dfc)
    return ( pivot_table.head(top_n_rows) )




def highlight_missing(val):
    """
    Color code cells in '%_Blank' based on thresholds (0-100 scale).

    >90%    : #f8696b
    80-90%  : #f97f6f
    70-80%  : #fa9673
    60-70%  : #fbac67
    50-60%  : #fcc37c
    40-50%  : #feda80
    30-40%  : #f6e984
    20-30%  : #d2de82
    10-20%  : #add480
    0-10%   : #63be7b
    """

    if val > 90:
        color = '#f8696b'
    elif val > 80:
        color = '#f97f6f'
    elif val > 70:
        color = '#fa9673'
    elif val > 60:
        color = '#fbac67'
    elif val > 50:
        color = '#fcc37c'
    elif val > 40:
        color = '#feda80'
    elif val > 30:
        color = '#f6e984'
    elif val > 20:
        color = '#d2de82'
    elif val > 10:
        color = '#add480'
    else:
        color = '#63be7b'
    
    return f'background-color: {color}'


def data_profile(df):
    n_row, n_col = df.shape

    # Basic summary
    summary = pd.DataFrame({
        'Variable_Name': df.columns,
        'Variable_Type': df.dtypes,
        'Missing_Count': df.isnull().sum(),
        '%_Blank': (df.isnull().sum() / n_row * 100).round(0).astype(int),
        'Unique_Values': df.nunique(),
        'Most_Frequent_Value': df.apply(lambda col: col.mode().iloc[0] if not col.mode().empty else pd.NA)
    })

    # Numeric summary
    numeric_stats = (
        df.describe(include='number')
          .T
          .reset_index()
          .rename(columns={'index': 'Variable_Name'})
          .round(2)  # <--- Round numeric columns to 2 decimals
    )
    # Drop 'count' column if you don't need it
    if 'count' in numeric_stats.columns:
        numeric_stats.drop(columns='count', inplace=True)
    # Rename '50%' to 'Median'
    if '50%' in numeric_stats.columns:
        numeric_stats.rename(columns={'50%': 'Median'}, inplace=True)

    # Skewness
    numeric_skew = df.skew(numeric_only=True).reset_index()
    numeric_skew.columns = ['Variable_Name', 'Skewness']

    # Merge everything
    final_summary = summary.merge(numeric_stats, on='Variable_Name', how='left')
    final_summary = final_summary.merge(numeric_skew, on='Variable_Name', how='left')

    final_summary = final_summary.sort_values(by="Variable_Type").reset_index(drop=True)
    #final_summary = final_summary.set_index('Variable_Name')

    styled_summary = (
        final_summary.style.format("{:.2f}", subset=['mean', 'std', 'min', 'Median', '25%', '75%', 'max', 'Skewness'])
        .applymap(highlight_missing, subset=['%_Blank'])
    )

    return n_row, n_col, styled_summary

