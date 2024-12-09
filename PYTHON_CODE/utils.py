import pandas as pd
import io

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
    

def bar_chart_data( df, x_var_name ):

    n_row, n_col = df.shape
    new_col = [1]* n_row

    try:
        df.insert(1, 'temp_count_id',new_col)
    except ValueError:
        print("WARNING: cannot insert temp_count_id already exists.")
    
    pivot_table = pd.pivot_table(df, values = ['temp_count_id'], index = [x_var_name],
                                 aggfunc = {'temp_count_id':'count'}) 
    
    try:
        df = df.drop(['temp_count_id'], axis=1)
    except ValueError:
        print("cannot drop temp_count_id")

    pivot_table = pivot_table.reset_index()
    pivot_table.columns = [x_var_name, 'count']
    pivot_table = pivot_table.sort_values(by = ['count'], ascending= False)

    # Take the top 8 rows!
    sub_pivot = pivot_table[:6]

    n_row, n_col = sub_pivot.shape
    total_count = sum(pivot_table['count'])

    prob = []
    cum_prob = []
    for i in range(0, n_row):
        value = pivot_table['count'].iloc[i]
        prob.append(round(value / total_count, ndigits = 2))

        if i==0:
            cum_prob.append(prob[i])
        else:
            cum_prob.append(round(sum(prob),ndigits=2))

    sub_pivot.insert(2, 'cumulative', cum_prob)
    #sub_pivot = sub_pivot.set_index(x_var_name)

    return(sub_pivot)



def data_profile(df):
    """
    Generate a comprehensive profile summary for the given DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: A summary DataFrame containing data types, missing values,
                      unique counts, and extended summary statistics.
    """
    # Shape of the DataFrame
    n_row, n_col = df.shape
    print(f"ROW TOTAL = {n_row:,} | COLUMNS = {n_col}")

    # Step 1: Data Type, Missing Values, and Unique Values
    summary = pd.DataFrame({
        'Variable_Name': df.columns,
        'Variable_Type': df.dtypes,
        'Missing_Count': df.isnull().sum(),
        '%_Blank': (df.isnull().sum() / n_row * 100).round(2),
        'Unique_Values': df.nunique(),
        'Most_Frequent_Value': df.apply(lambda col: col.mode().iloc[0] if not col.mode().empty else np.nan)
    })

    # Step 2: Summary Statistics for Numeric Columns
    numeric_stats = df.describe(include='number').T
    numeric_stats = numeric_stats.reset_index().rename(columns={'index': 'Variable_Name'})

    # Step 3: Add Skewness for Numeric Columns
    numeric_skew = df.skew(numeric_only=True).reset_index()
    numeric_skew.columns = ['Variable_Name', 'Skewness']

    # Step 4: Memory Usage for Each Column
    #memory_usage = df.memory_usage(deep=True).reset_index()
    #memory_usage.columns = ['Variable_Name', 'Memory_Bytes']

    # Step 5: Combine All Results
    final_summary = summary.merge(numeric_stats, on='Variable_Name', how='left')
    final_summary = final_summary.merge(numeric_skew, on='Variable_Name', how='left')
    #final_summary = final_summary.merge(memory_usage, on='Variable_Name', how='left')

    final_summary = final_summary.sort_values(by="Variable_Type")

    return( n_row, n_col, final_summary )

