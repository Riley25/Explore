import streamlit as st
import altair as alt

import pandas as pd
import numpy as np

from utils import *
from eda import *

def main():

    st.set_page_config(layout="wide", page_title="Explore!", page_icon="📈")
    st.title("EDA with Excel 📊")
    
    # Upload Excel file
    uploaded_file = st.file_uploader("Step 1: Upload your Excel file", type=["xlsx", "xls", "csv"] , label_visibility="hidden")

    TOP_N_ROWS = 6

    if uploaded_file:
        st.balloons()

        df = load_excel(uploaded_file)
        col_names = df.columns

        tab1, tab2 = st.tabs(["Overview" , "Data Profile"])

        with tab1:
            
            n_row, n_col, DP = data_profile(df)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Number of Rows",   value=f"{(n_row):,}"  , border=True)

            with col2: 
                st.metric(label="Number of columns", value=f"{(n_col):,}" , border=True)

            with col3: 
                st.write(" ")


            st.write("### Data Preview:")
            st.caption("Top 20 Rows")
            st.dataframe(df.set_index(col_names[0]).head(6) , use_container_width= True )

            st.divider()
            st.write("#### EDA")

            for x_var_name in col_names: 

                t = df.dtypes[x_var_name]

                if t == object:
                    col1, col2, col3 = st.columns([ 2, 0.2, 1.5 ])
                    plot_data = bar_chart_data( df, x_var_name, top_n_rows=TOP_N_ROWS )

                    with col1:    
                        bar_chart =  alt.Chart(plot_data).mark_bar().encode(x="Occurrences:Q",  y=alt.Y(x_var_name, sort='-x'), color=alt.value("#1e80e8") ).properties(height = 350).configure_axis(labelColor = "black",titleColor = "black").configure_legend(labelColor='black',titleColor='black')  
                        st.altair_chart(bar_chart, use_container_width=True)
                    
                    with col2:
                        st.write('   ')

                    with col3:
                        st.dataframe( plot_data.set_index(x_var_name) )


        with tab2:
            st.write(' ')
            n_row, n_col, DP = data_profile(df)


            st.dataframe(DP.set_index('Variable_Name'), use_container_width=True)
            st.write("HELLO")


if __name__ == "__main__":
    main()