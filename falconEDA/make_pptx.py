

from utils import *

from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN

import io



def create_pptx_v3(df):

    POWERPOINT_PIXEL_PER_INCH = 96    # DO NOT CHANGE
    PIXEL_PER_INCH = 250              # Resolution of our images
    
    plot_width_pixels = 800
    plot_height_pixels = 450

    width_inches = plot_width_pixels / POWERPOINT_PIXEL_PER_INCH 
    height_inches = plot_height_pixels /POWERPOINT_PIXEL_PER_INCH 

    # Create Presentation
    prs = Presentation()
    slide_width = Inches(13.33); prs.slide_width = slide_width
    slide_height = Inches(7.5) ; prs.slide_height = slide_height
    
    #center_x = slide_width / 2
    #center_y = slide_height / 2
    #left = center_x - (width_inches / 2)
    #top = center_y - (height_inches / 2)

    

    slide_layout = prs.slide_layouts[5]     # Blank layout
    BAR_COLORS = ["#826fc2","#001f80","#4d9b1e","#f865c6","#ecd378","#ba004c","#8f4400","#f65656"]*10000

    # Loop through each column in the DataFrame
    for count, col_name in enumerate(df.columns):
        slide = prs.slides.add_slide(slide_layout)
        title = slide.shapes.title
        title.text = f"{col_name}"

        # Left-align the title
        text_frame = title.text_frame
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.LEFT

        col_type = df[col_name].dtype

        # Categorical column
        if col_type == 'object':
            plot_data = bar_chart_data(df, col_name, top_n_rows=5)

            # Generate Altair bar chart
            chart = alt.Chart(plot_data).mark_bar().encode(
                x=alt.X("Occurrences:Q", axis=alt.Axis(format='d', title="Occurrences")),
                y=alt.Y(col_name, sort='-x', title=None),
                color=alt.value(BAR_COLORS[count])
            ).properties(width=plot_width_pixels, height=plot_height_pixels)   # <---- Bar Graph Dimenstions

            # Save image
            img_buffer = io.BytesIO()
            chart.save(img_buffer, format="png", ppi = PIXEL_PER_INCH)
            img_buffer.seek(0)

            left = Inches(2.5)
            top = Inches(2.0)
            
            slide.shapes.add_picture(img_buffer, left, top, width = Inches(width_inches) )

        # Numeric column
        elif col_type in ['int64', 'float64']:

            plot_width_pixels = 700
            plot_height_pixels = 350

            left = Inches(2.5)
            top = Inches(1.5)

            chart = boxplot_histogram(df, col_name, bar_color=BAR_COLORS[count], WIDTH=plot_width_pixels, HEIGHT=plot_height_pixels)

            # Save image
            img_buffer = io.BytesIO()
            chart.save(img_buffer, format="png", ppi = PIXEL_PER_INCH)
            img_buffer.seek(0)

            slide.shapes.add_picture( img_buffer, left, top,  width=Inches(width_inches)  )

    ppt_buffer = io.BytesIO()
    prs.save(ppt_buffer)
    ppt_buffer.seek(0)  # Move to the beginning of the buffer

    return ppt_buffer.getvalue()

    # ppt_file = "EDA_Presentation_v3.pptx"
    # prs.save(ppt_file)
    # # Return PowerPoint file as bytes
    # with open(ppt_file, "rb") as f:
    #     ppt_bytes = f.read()
    # return ppt_bytes







