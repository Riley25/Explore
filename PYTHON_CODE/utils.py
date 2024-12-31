##############################
#
#  NAME: utils.py
#  
#  PURPOSE: 
#           load_excel   ()

import pandas as pd
import numpy as np
import altair as alt
import os


def load_excel(uploaded_file):
    #
    # PURPOSE: Load an Excel or CSV file into a Pandas DataFrame.


    # Extract the extension from the uploaded file's name
    _, file_extension = os.path.splitext(uploaded_file.name)
    file_extension = file_extension.lower()

    if file_extension in [".xlsx", ".xls"]:
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            return df
        except Exception as e:
            raise ValueError(f"Error loading Excel file: {e}")
    
    elif file_extension == ".csv":
        try:
            df = pd.read_csv(uploaded_file, engine="c", low_memory=False)
            return df
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {e}")
    
    else:
        raise ValueError(f"Unsupported file extension: '{file_extension}'")
    

def bar_chart_data(dfc, var_name, top_n_rows = 6):
    #
    # PURPOSE: Efficiently generate bar chart data with counts, cumulative probability, and sorting.

    
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


def boxplot_histogram(df, column, bar_color ):
    #
    # PURPOSE: Creates a box plot on top of a histogram for the same numeric column using Altair.
    #
    # Bottom: Histogram
    
    hist = (
        alt.Chart(df)
        .mark_bar(stroke='black', strokeWidth=0.05)
        .encode(
            x=alt.X(
                column,
                bin=alt.Bin(maxbins=30),
                scale = alt.Scale(domain = [np.min(df[column]), np.max(df[column])]) , 
                axis=alt.Axis(labelColor='black', titleColor='black', grid=True)  # Enable vertical grid lines
            ),
            y=alt.Y(
                "count()",
                title="Count",
                axis=alt.Axis(labelColor='black', titleColor='black')
            ), 
            color=alt.value(bar_color)
        )
        .properties(width=600, height=300)
    )

    # Top: Box Plot (white font)
    box = (
        alt.Chart(df)
        .mark_boxplot(ticks=True)
        .encode(
            x=alt.X(
                column,
                title=None,
                scale = alt.Scale(domain = [np.min(df[column]), np.max(df[column])]) ,
                axis=alt.Axis(labelColor='white', titleColor='white')  # white font
            ),
            color=alt.value(bar_color)
        )
        .properties(height=100)
    )

    # Vertically concatenate and share the x-axis scale
    combined_chart = (
        alt.vconcat(box, hist, spacing=5)
        .resolve_scale(x='shared')
    )

    return combined_chart


def highlight_missing(val):
    """
    Color code cells in '%_Blank' based on thresholds (0-100 scale).

    95-100 %    : #b80000
    90- 95 %    : #c11e11
    85- 90 %    : #c62d19
    80- 85 %    : #ca3b21
    75- 80 %    : #cf4a2a
    70- 75 %    : #d35932
    65- 70 %    : #d8673a
    60- 65 %    : #dc7643
    55- 60 %    : #e0854b
    50- 55 %    : #e59353
    45- 50 %    : #e9a25b
    40- 45 %    : #eeb164
    35- 40 %    : #f2bf6c 
    30- 35 %    : #f7ce74
    25- 30 %    : #fbdd7c
    20- 25 %    : #ffeb84
    15- 20 %    : #d7df81
    10- 15 %    : #b0d47f
     5- 10 %    : #8ac97d
     0-  5 %    : #63be7b
    """

    if val > 95:
        color = '#b80000'
    elif val > 90:
        color = '#c11e11'
    elif val > 85:
        color = '#c62d19'
    elif val > 80:
        color = '#ca3b21'
    elif val > 75:
        color = '#cf4a2a'
    elif val > 70:
        color = '#d35932'
    elif val > 65:
        color = '#d8673a'
    elif val > 60:
        color = '#dc7643'
    elif val > 55:
        color = '#e0854b'
    elif val > 50:
        color = '#e59353'
    elif val > 45:
        color = '#e9a25b'
    elif val > 40:
        color = '#eeb164'
    elif val > 35:
        color = '#f2bf6c'
    elif val > 30:
        color = '#f7ce74'
    elif val > 25:
        color = '#fbdd7c'
    elif val > 20:
        color = '#ffeb84'
    elif val > 15:
        color = '#d7df81'
    elif val > 10:
        color = '#b0d47f'
    elif val > 5:
        color = '#8ac97d'
    else:
        color = '#63be7b'
    
    return f'background-color: {color}'


def data_profile(df):
    n_row, n_col = df.shape

    # Basic summary
    summary = pd.DataFrame({
        'Variable Name': df.columns,
        'Variable Type': df.dtypes,
        'Missing Count': df.isnull().sum(),
        '% Blank': (df.isnull().sum() / n_row * 100).round(0).astype(int),
        'Unique Values': df.nunique(),
        'Most Frequent Value': df.apply(lambda col: col.mode().iloc[0] if not col.mode().empty else pd.NA)
    })

    # Numeric summary
    numeric_stats = (
        df.describe(include='number')
          .T
          .reset_index()
          .rename(columns={'index': 'Variable Name'})
          .round(2)  # <--- Round numeric columns to 2 decimals
    )


    # Drop & rename columns
    if 'count' in numeric_stats.columns:
        numeric_stats.drop(columns='count', inplace=True)
    
    if '50%' in numeric_stats.columns:
        numeric_stats.rename(columns={'50%': 'Median'}, inplace=True)

    if 'mean' in numeric_stats.columns:
        numeric_stats.rename(columns={'mean': 'Mean'}, inplace=True)

    if 'std' in numeric_stats.columns:
        numeric_stats.rename(columns={'std': 'Standard Deviation'}, inplace=True)

    if 'min' in numeric_stats.columns:
        numeric_stats.rename(columns={'min': 'Min'}, inplace=True)

    if 'max' in numeric_stats.columns:
        numeric_stats.rename(columns={'max': 'Max'}, inplace=True)


    # Skewness
    numeric_skew = df.skew(numeric_only=True).reset_index()
    numeric_skew.columns = ['Variable Name', 'Skewness']

    # Merge everything
    final_summary = summary.merge(numeric_stats, on='Variable Name', how='left')
    final_summary = final_summary.merge(numeric_skew, on='Variable Name', how='left')

    #final_summary = final_summary.sort_values(by="Variable Type").reset_index(drop=True)
    #final_summary = final_summary.set_index('Variable_Name')

    styled_summary = (
        final_summary.style.format("{:.2f}", subset=['Missing Count','Mean', 'Standard Deviation', 'Min', 'Median', '25%', '75%', 'Max', 'Skewness']).format("{:.0f}%", subset=['% Blank'])
        .applymap(highlight_missing, subset=['% Blank'])
    )
    
    return n_row, n_col, styled_summary



def reorder_columns_by_dtype(df):
    # PURPOSE:  Re-Order Columns in the following Order
    # 
    #       Date / Time
    #       Categorical
    #       Numeric

    date_cols = df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns.tolist()
    
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    
    return( date_cols + cat_cols + num_cols)


