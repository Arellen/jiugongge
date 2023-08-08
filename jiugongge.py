import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def create_jiugongge_chart(data):
    # Determine the quantiles for sales and profit margin
    x_quantiles = data.iloc[:, 1].quantile([0.33, 0.66])
    y_quantiles = data.iloc[:, 2].quantile([0.33, 0.66])

    plt.figure(figsize=(10, 8))
    # Scatter plot with labels
    for i, row in data.iterrows():
        plt.scatter(row.iloc[2], row.iloc[1], c='blue', marker='o', edgecolors='black')
        plt.text(row.iloc[2], row.iloc[1], row.iloc[0], fontsize=9, ha='right')

    # Plot the quantile lines
    plt.axhline(y=x_quantiles[0.33], color='red', linestyle='--')
    plt.axhline(y=x_quantiles[0.66], color='red', linestyle='--')
    plt.axvline(x=y_quantiles[0.33], color='red', linestyle='--')
    plt.axvline(x=y_quantiles[0.66], color='red', linestyle='--')

    # Set labels and title
    plt.ylabel('X轴数据')
    plt.xlabel('Y轴数据')
    plt.title('九宫格')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    st.pyplot(plt)

st.title("九宫格生成器")
uploaded_file = st.file_uploader("请上传一个Excel文件", type="xlsx")

if uploaded_file:
    data = pd.read_excel(uploaded_file)
    if data.shape[1] >= 3:
        create_jiugongge_chart(data)
    else:
        st.warning("请确保您的Excel文件至少包含三列：系列、X轴数据和Y轴数据。")
