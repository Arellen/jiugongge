import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_jiugongge_chart(data, chart_title):
    # Determine the quantiles for sales and profit margin
    x_quantiles = data.iloc[:, 1].quantile([0.33, 0.66])
    y_quantiles = data.iloc[:, 2].quantile([0.33, 0.66])
    
    fig = px.scatter(data, x=data.columns[2], y=data.columns[1])

    # Move text above the marker
    fig.update_traces(textposition='top center')

    # Add lines for quantiles
    line_properties = dict(color="red", dash="dash")
    fig.add_shape(
        type="line", line=line_properties,
        x0=min(data.iloc[:, 2]), x1=max(data.iloc[:, 2]), y0=x_quantiles[0.33], y1=x_quantiles[0.33]
    )
    fig.add_shape(
        type="line", line=line_properties,
        x0=min(data.iloc[:, 2]), x1=max(data.iloc[:, 2]), y0=x_quantiles[0.66], y1=x_quantiles[0.66]
    )
    fig.add_shape(
        type="line", line=line_properties,
        x0=y_quantiles[0.33], x1=y_quantiles[0.33], y0=min(data.iloc[:, 1]), y1=max(data.iloc[:, 1])
    )
    fig.add_shape(
        type="line", line=line_properties,
        x0=y_quantiles[0.66], x1=y_quantiles[0.66], y0=min(data.iloc[:, 1]), y1=max(data.iloc[:, 1])
    )

    # Update layout based on user requirements
    fig.update_layout(
        title=chart_title, 
        xaxis_title=data.columns[2], 
        yaxis_title=data.columns[1],
        plot_bgcolor="white",
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_ticks="",
        yaxis_ticks="",
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
        showlegend=False
    )
    st.plotly_chart(fig)

st.title("九宫格生成器")
chart_title = st.text_input("请输入图表标题（如不输入则显示为空白）:", "")
uploaded_file = st.file_uploader("请上传一个Excel文件", type="xlsx")

if uploaded_file:
    data = pd.read_excel(uploaded_file)
    if data.shape[1] >= 3:
        create_jiugongge_chart(data, chart_title)
    else:
        st.warning("请确保您的Excel文件至少包含三列：系列、X轴数据和Y轴数据。")
