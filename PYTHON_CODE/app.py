import streamlit as st
import altair as alt

import pandas as pd
import numpy as np
import os
import warnings

from utils import *
from eda import *

def main():
    warnings.filterwarnings("ignore") # Let's live life on the edge. :)

    st.set_page_config(layout="wide", page_title="Explore!", page_icon="📈")
    st.title("Explore Your Data 📊")
    st.caption("Purpose: Explore the Distributions and Trends in Your Dataset")

    colA, colB = st.columns([ 0.35, 0.65 ])
    with colA:
        uploaded_file = st.file_uploader("Step 1: Upload your Excel file", type=["xlsx", "xls", "csv"] , label_visibility="hidden")
        st.write(' ')

    with colB:
        st.write(' ')

    TOP_N_ROWS = 6

    if uploaded_file:

        df = load_excel(uploaded_file)
        new_col_order = reorder_columns_by_dtype(df)
        df = df[new_col_order]

        st.balloons()
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
                #top_n = st.number_input("Top ___ Rows", 5, 50, value = 10)
                st.write(" ")


            st.write("### Data Preview ")
            st.caption("Top 20 Rows")
            st.dataframe(df.set_index(col_names[0]).head(6) , use_container_width= True )

            st.divider()
            st.write("#### EDA")
            blue_colors = ["#3c7ae7","#0362a0","#6195e2","#2d5192","#3570c5","#4b69ad"]*(len(col_names)*2)

            #####################################
            # CREATE DUPLICATE COPY
            dfc = df.copy()
            
            for count, var_name in enumerate(col_names):
                
                t = dfc.dtypes[var_name]

                if t == object:
                    col1, col2, col3 = st.columns([ 2, 0.2, 1.5 ])
                    plot_data = bar_chart_data( dfc, var_name, top_n_rows=TOP_N_ROWS )

                    with col1:    
                        bar_chart =  alt.Chart(plot_data).mark_bar().encode(x=alt.X("Occurrences:Q", axis=alt.Axis(format='d',tickMinStep=1)) , y=alt.Y(var_name, sort='-x'), color=alt.value(blue_colors[count]) ).properties(width = 500, height = 350).configure_axis(labelColor = "black",titleColor = "black").configure_legend(labelColor='black',titleColor='black')   
                        st.altair_chart(bar_chart, use_container_width=True)

                    with col2:
                        st.write('')

                    with col3:
                        #st.write(plot_data.set_index(var_name))
                        st.dataframe( plot_data.set_index(var_name), use_container_width=True )

                elif t==int or t==float:
                    col1, col2, col3 = st.columns([ 2, 0.2, 1.5 ])
                    with col1:
                        boxHist = boxplot_histogram(dfc, var_name, blue_colors[count] )
                        st.altair_chart(boxHist, use_container_width=True)
                        st.write(' ')
                        st.write(' ')
                        st.write(' ')
                    with col2:
                        st.write('')
                    with col3:
                        st.write('  ')

        with tab2:
            st.write(' ')
            n_row, n_col, DP = data_profile(df)

            st.dataframe(DP , use_container_width=True)



if __name__ == "__main__":
    main()

