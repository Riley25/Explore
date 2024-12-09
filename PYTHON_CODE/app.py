import streamlit as st
import pandas as pd
from utils import *
from eda import *

def main():

    st.set_page_config(layout="wide", page_title="Explore!", page_icon="📈")
    st.title("EDA with Excel 📊")
    
    # Upload Excel file
    uploaded_file = st.file_uploader("Step 1: Upload your Excel file", type=["xlsx", "xls", "csv"])

    if uploaded_file:
        st.balloons()

        df = load_excel(uploaded_file)
        col_names = df.columns

        tab1, tab2 = st.tabs(["Overview" , "Data Profile"])

        with tab1:

            st.write("### Data Preview:")
            st.caption("Top 20 Rows")

            #df_no_index = df.reset_index(drop = True)
            st.dataframe(df.set_index(col_names[0]).head(20) , use_container_width= True )
            #st.dataframe(df.style.hide_index().head(8) , use_container_width= True )

            st.divider()
            st.write("### EDA")

            for x_var_name in col_names: 

                t = df.dtypes[x_var_name]

                if t == object:
                    col1, col2 = st.columns([1,1.5])
                    plot_data = bar_chart_data( df, x_var_name )

                    with col1:    
                        st.dataframe( plot_data.set_index(x_var_name) )
                    with col2:
                        st.bar_chart(plot_data, x = str(x_var_name), y = 'count' )

                    #st.write(x_var_name) 
                    #st.dataframe(df[x_var_name])

        with tab2:
            n_row, n_col, DP = data_profile(df)

            st.dataframe(DP.set_index('Variable_Name'), use_container_width=True)
            #st.write("HELLO")

        #st.write(df.dtypes)
        #stats = perform_eda(df)
        #st.write(stats)

if __name__ == "__main__":
    main()