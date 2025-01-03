#
#  Helpful Links
#  https://docs.streamlit.io/develop/api-reference/configuration/config.toml
#

import streamlit as st

from utils import *
from make_pptx import create_pptx_v3

import os
import warnings

warnings.filterwarnings("ignore") # Let's live life on the edge. :)
TOP_N_ROWS = 6


# Initialize session state variables
if "balloons_shown" not in st.session_state:
    st.session_state["balloons_shown"] = False


def main():

    st.set_page_config(layout="wide", page_title="FalconEDA", page_icon="📈", 
                       menu_items={'About':None,  
                                   'Get Help':None,
                                   'Report a bug':None}
                      )
    
    st.title("Explore Your Data 🦅 📊 ")
    st.caption("Purpose of **FalconEDA**:  Quickly explore the Distributions and Trends in Your Data. Let's hunt for new insights!")

    colA, colB, colC = st.columns([ 0.45, 0.025, 0.525 ])
    with colA:
        uploaded_file = st.file_uploader("Step 1: Upload your Excel file", type=["xlsx", "xls", "csv"] , label_visibility="hidden")
        st.write(' ')

        if uploaded_file:

            df = load_excel(uploaded_file)
            new_col_order = reorder_columns_by_dtype(df)
            df = df[new_col_order]

            # Create Duplicate Copy
            dfc = df.copy()

            if not st.session_state["balloons_shown"]:
                st.balloons()
                st.session_state["balloons_shown"] = True

            col_names = df.columns
        else:
            df = None

    with colB:
        st.write('')

    with colC:
        if df is not None:
            st.write(' ')
            st.write(' ')
            if st.button("Generate PowerPoint", icon ='🎥', type = 'primary'):
                with st.spinner("Generating PowerPoint ... "):
                    ppt_bytes=create_pptx_v3(df)
                st.download_button(
                    label = "Download PowerPoint", 
                    data = ppt_bytes, 
                    icon = '💾',
                    type = 'primary',
                    file_name = "EDA_Presentation.pptx", 
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
                
            # if st.download_button(
            #     label="Generate PowerPoint",
            #     icon = '🎥',
            #     type= 'primary',
            #     data=create_pptx_v3(df),  # Function to generate PowerPoint
            #     file_name="EDA_Presentation.pptx",
            #     mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"):
            #         st.write('')
        else:
            st.write(' ')

    
    if df is None:
        st.write(' ')
    else:
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
            st.caption("Top 5 Rows")
            st.dataframe(df.set_index(col_names[0]).head(6) , use_container_width= True )

            ### BEGIN EDA ANALYSIS
            st.divider()
            

            ## Offer color options to users
            col1, col2 = st.columns([.25,.75])
            with col1:
                color_option = st.selectbox("Select a Color Theme", ("Color Blind Friendly","Blue Ocean", "Red Roses")  )
                st.write(' ') ; st.write(' ') ; st.write(' ')

                if color_option == "Color Blind Friendly":
                    BAR_COLORS = ["#826fc2","#001f80","#4d9b1e","#f865c6","#ecd378","#ba004c","#8f4400","#f65656"]*10000
                elif color_option =="Blue Ocean":
                    BAR_COLORS = ["#3c7ae7","#0362a0","#6195e2","#2d5192","#3570c5","#4b69ad"]*10000
                elif color_option =='Red Roses':
                    BAR_COLORS = ["#f5405f","#ffbaef","#bc0052","#ff52be","#8a2f6c"]*10000
            with col2:
                st.write(' ')

            for count, var_name in enumerate(col_names):
                
                t = dfc.dtypes[var_name]

                if t == object:
                    col1, col2, col3 = st.columns([ 2, 0.2, 1.5 ])
                    plot_data = bar_chart_data( dfc, var_name, top_n_rows=TOP_N_ROWS )

                    with col1:    
                        bar_chart =  alt.Chart(plot_data).mark_bar().encode(x=alt.X("Occurrences:Q", axis=alt.Axis(format='d',tickMinStep=1)) , y=alt.Y(var_name, sort='-x'), color=alt.value(BAR_COLORS[count]) ).properties(width = 500, height = 350).configure_axis(labelColor = "black",titleColor = "black").configure_legend(labelColor='black',titleColor='black')   
                        st.altair_chart(bar_chart, use_container_width=True)

                    with col2:
                        st.write('')

                    with col3:
                        #st.write(plot_data.set_index(var_name))
                        st.dataframe( plot_data.set_index(var_name), use_container_width=True )

                elif t==int or t==float:
                    col1, col2, col3 = st.columns([ 2, 0.2, 1.5 ])
                    with col1:
                        boxHist = boxplot_histogram(dfc, var_name, BAR_COLORS[count] )
                        st.altair_chart(boxHist, use_container_width=True)
                        st.write(' ')
                        st.write(' ')
                        st.write(' ')
                    with col2:
                        st.write('')
                    with col3:
                        STATS = calculate_numeric_stats(dfc, var_name )
                        st.dataframe( STATS.set_index('Statistic') , use_container_width=True )

        with tab2:

            n_row, n_col, DP = data_profile(df)

            st.dataframe(DP , use_container_width=True)



if __name__ == "__main__":
    main()

