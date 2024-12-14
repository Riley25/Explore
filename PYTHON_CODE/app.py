import streamlit as st
import altair as alt
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
                    col1, col2, col3 = st.columns([ 2, 0.2, 1.5 ])
                    plot_data = bar_chart_data( df, x_var_name )

                    with col1:    
                        bar_chart =  alt.Chart(plot_data).mark_bar().encode(x="count:Q",  y=alt.Y(x_var_name, sort='-x'), color=alt.value("#1e80e8") ).properties(height = 350).configure_axis(labelColor = "black",titleColor = "black").configure_legend(labelColor='black',titleColor='black')  
                        st.altair_chart(bar_chart, use_container_width=True)
                    
                    with col2:
                        st.write('   ')

                    with col3:
                        st.dataframe( plot_data.set_index(x_var_name) )


        with tab2:
            st.write(' ')
        #     n_row, n_col, DP = data_profile(df)

        #     col1, col2, col3 = st.columns(3)
        #     with col1:
        #         st.metric(label="Number of Rows",   value=f"{(n_row):,}")

        #     with col2: 
        #         st.metric(label="Number of columns", value=f"{(n_col):,}")

        #     with col3: 
        #         st.write(" ")

        #     st.dataframe(DP.set_index('Variable_Name'), use_container_width=True)
            #st.write("HELLO")

        #st.write(df.dtypes)
        #stats = perform_eda(df)
        #st.write(stats)

if __name__ == "__main__":
    main()