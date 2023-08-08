import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import io

# 加载自定义字体
font_path = './SimHei.ttf'  # 调整为您的字体路径
prop = fm.FontProperties(fname=font_path)

def create_jiugongge_chart(data):
    plt.figure(figsize=(10, 8))

    # Scatter plot with labels
    for i, row in data.iterrows():
        plt.scatter(row.iloc[2], row.iloc[1], c='blue', marker='o', edgecolors='black')
        plt.text(row.iloc[2], row.iloc[1], row.iloc[0], fontsize=9, ha='right', fontproperties=prop)

    # Plot the quantile lines
    x_quantiles = data.iloc[:, 1].quantile([0.33, 0.66])
    y_quantiles = data.iloc[:, 2].quantile([0.33, 0.66])
    plt.axhline(y=x_quantiles[0.33], color='red', linestyle='--')
    plt.axhline(y=x_quantiles[0.66], color='red', linestyle='--')
    plt.axvline(x=y_quantiles[0.33], color='red', linestyle='--')
    plt.axvline(x=y_quantiles[0.66], color='red', linestyle='--')

    # Set labels and title using the headers from the data
    plt.ylabel(data.columns[1], fontproperties=prop)
    plt.xlabel(data.columns[2], fontproperties=prop)
    plt.title('九宫格', fontproperties=prop)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Save the plot to a BytesIO object to serve as a download
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

st.title("九宫格生成器")
uploaded_file = st.file_uploader("请上传一个Excel文件", type="xlsx")

if uploaded_file:
    data = pd.read_excel(uploaded_file)
    if data.shape[1] >= 3:
        buffer = create_jiugongge_chart(data)
        st.pyplot()
        st.download_button(
            label="下载九宫格图表",
            data=buffer,
            file_name="jiugongge_chart.png",
            mime="image/png"
        )
    else:
        st.warning("请确保您的Excel文件至少包含三列：系列、X轴数据和Y轴数据。")
