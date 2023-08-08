import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def create_jiugongge_chart(data, chart_title):
    # Determine the quantiles for sales and profit margin
    x_quantiles = data.iloc[:, 1].quantile([0.33, 0.66])
    y_quantiles = data.iloc[:, 2].quantile([0.33, 0.66])
    
    fig = go.Figure()

    # Add scatter points with modified text font for series labels
    fig.add_trace(go.Scatter(x=data.iloc[:, 2], y=data.iloc[:, 1], mode='markers+text', 
                             text=data.iloc[:, 0], textposition='top center',
                             textfont=dict(size=18, color='#000000', family='Arial')))

    # Add lines for quantiles
    fig.add_shape(
        type="line", line=dict(dash="dash", color="red"),
        x0=min(data.iloc[:, 2]), x1=max(data.iloc[:, 2]), y0=x_quantiles[0.33], y1=x_quantiles[0.33]
    )
    fig.add_shape(
        type="line", line=dict(dash="dash", color="red"),
        x0=min(data.iloc[:, 2]), x1=max(data.iloc[:, 2]), y0=x_quantiles[0.66], y1=x_quantiles[0.66]
    )
    fig.add_shape(
        type="line", line=dict(dash="dash", color="red"),
        x0=y_quantiles[0.33], x1=y_quantiles[0.33], y0=min(data.iloc[:, 1]), y1=max(data.iloc[:, 1])
    )
    fig.add_shape(
        type="line", line=dict(dash="dash", color="red"),
        x0=y_quantiles[0.66], x1=y_quantiles[0.66], y0=min(data.iloc[:, 1]), y1=max(data.iloc[:, 1])
    )
    
    # Add arrows for x and y axes with reduced size
    fig.add_annotation(
        axref='x', ayref='y', ax=0, ay=0, x=max(data.iloc[:, 2]), y=0,
        xref='x', yref='y', showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#636363'
    )
    fig.add_annotation(
        axref='x', ayref='y', ax=0, ay=0, x=0, y=max(data.iloc[:, 1]),
        xref='x', yref='y', showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#636363'
    )
    
    fig.update_layout(
        title=chart_title,
        xaxis=dict(title=data.columns[2], tickformat=".0%", titlefont=dict(size=18)),
        yaxis=dict(title=data.columns[1], titlefont=dict(size=18)),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig)

st.title("九宫格生成器")

# Get chart title from user
chart_title = st.text_input("请输入图表的标题：")

uploaded_file = st.file_uploader("请上传一个Excel文件", type="xlsx")

if uploaded_file:
    data = pd.read_excel(uploaded_file)
    if data.shape[1] >= 3:
        create_jiugongge_chart(data, chart_title)
    else:
        st.warning("请确保您的Excel文件至少包含三列：系列、X轴数据和Y轴数据。")
