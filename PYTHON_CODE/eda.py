import pandas as pd

def perform_eda(df):
    """
    Perform basic EDA on a DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        dict: A dictionary containing key EDA statistics.
    """
    try:
        # DataFrame Information
        num_rows, num_cols = df.shape
        missing_values = df.isnull().sum().to_frame("Missing Values")
        missing_values["Percentage"] = (missing_values["Missing Values"] / num_rows) * 100
        missing_values = missing_values[missing_values["Missing Values"] > 0]
        
        # Descriptive Statistics
        summary_stats = df.describe(include="all").T  # Transpose for better display
        
        # Data Types and Unique Values
        column_types = pd.DataFrame({
            "Data Type": df.dtypes,
            "Unique Values": df.nunique()
        })
        
        # Combine Results in a Dictionary
        eda_results = {
            "shape": {"Rows": num_rows, "Columns": num_cols},
            "missing_values": missing_values,
            "summary_statistics": summary_stats,
            "column_types": column_types
        }
        
        return eda_results
    
    except Exception as e:
        raise ValueError(f"Error performing EDA: {e}")