import streamlit as st
import altair as alt
import pandas as pd

# 1) Inject CSS for a white "card" container
st.markdown(
    """
    <style>
    .white-box {
        background-color: #FFFFFF; 
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #CCCCCC; 
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sample dataframe
df = pd.DataFrame({
    "Sex": ["male", "male", "male", "female", "female"],
    "Occurrences": [200, 70, 10, 100, 52]
})

# 2) Create a bar chart with a transparent background
bar_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(x="Occurrences:Q", y=alt.Y("Sex:N", sort="-x"))
    .properties(width=500, height=300)
    # Make chart background transparent so the white box is visible behind it
    .configure_view(stroke=None)      # remove border lines
)

# 3) Place the chart inside the white box
st.markdown('<div class="white-box">', unsafe_allow_html=True)
st.altair_chart(bar_chart, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
