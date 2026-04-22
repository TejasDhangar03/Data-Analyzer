#simpler version

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout="wide")

# ------------------ HEADER ------------------
st.markdown("<h1 style='text-align:center;'>📊 Data Visualizer EDA</h1>", unsafe_allow_html=True)
st.markdown("---")

# ------------------ DATA FUNCTION ------------------
def create_data(choice, custom_rows=None, file=None):
    if choice == '1':
        return pd.DataFrame(np.random.rand(100, 10), columns=list("ABCDEFGHIJ"))

    elif choice == '2' and custom_rows:
        return pd.DataFrame(custom_rows, columns=["A","B","C","D","E"])

    elif choice == '3' and file:
        return pd.read_csv(file)

    return None


# ------------------ PLOT FUNCTIONS ------------------
def plot_full(df, plot_type):
    if plot_type == '1':
        fig = px.line(df)
    elif plot_type == '2':
        fig = px.scatter(df)
    elif plot_type == '3':
        fig = px.bar(df)
    elif plot_type == '4':
        fig = px.histogram(df)
    elif plot_type == '5':
        fig = px.box(df)
    elif plot_type == '6':
        fig = go.Figure(data=[go.Surface(z=df.values)])
    else:
        return None

    fig.update_layout(height=500)
    return fig


def plot_columns(df, plot_type, cols):
    if len(cols) == 0:
        return None

    if plot_type == '1':
        fig = px.line(df, y=cols)
    elif plot_type == '2':
        fig = px.scatter(df, y=cols)
    elif plot_type == '3':
        fig = px.bar(df, y=cols)
    elif plot_type == '4':
        fig = px.histogram(df, x=cols[0])
    elif plot_type == '5':
        fig = px.box(df, y=cols)
    elif plot_type == '6':
        fig = go.Figure(data=[go.Surface(z=df[cols].values)])
    elif plot_type == '7' and len(cols) >= 2:
        fig = px.scatter(df, x=cols[0], y=cols[1], size=df[cols[-1]])
    else:
        return None

    fig.update_layout(height=500)
    return fig


# ------------------ UI ------------------

# SECTION 1: DATA SOURCE
st.subheader("🔹 Step 1: Select Data Source")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("1️. Random Data"):
        st.session_state.data_choice = '1'

with col2:
    if st.button("2️. Custom Data"):
        st.session_state.data_choice = '2'

with col3:
    if st.button("3️. Upload File"):
        st.session_state.data_choice = '3'


choice = st.session_state.get("data_choice", None)

custom_rows = []
uploaded_file = None

# CUSTOM DATA UI
if choice == '2':
    st.markdown("### Enter 5x5 Data")
    for i in range(5):
        row = st.text_input(f"Row {i+1}", key=f"row{i}")
        if row:
            try:
                values = list(map(float, row.split(",")))
                if len(values) == 5:
                    custom_rows.append(values)
            except:
                st.warning("Invalid input")

# FILE UPLOAD
if choice == '3':
    uploaded_file = st.file_uploader("Upload CSV File")

# CREATE DATA
df = create_data(choice, custom_rows, uploaded_file)

# ------------------ SHOW DATA ------------------
if df is not None:
    st.markdown("---")
    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)

    # ------------------ GRAPH SECTION ------------------
    st.markdown("---")
    st.subheader(" Step 2: Choose Graph Type")

    g1, g2 = st.columns(2)

    with g1:
        st.write("### Complete Graph")
        plot_full_choice = st.selectbox(
            "Select Graph",
            ["", "1 Line", "2 Scatter", "3 Bar", "4 Histogram", "5 Box", "6 Surface"],
            key="full_plot"
        )

    with g2:
        st.write("### Specific Columns Graph")
        plot_col_choice = st.selectbox(
            "Select Graph",
            ["", "1 Line", "2 Scatter", "3 Bar", "4 Histogram", "5 Box", "6 Surface", "7 Bubble"],
            key="col_plot"
        )

        cols = st.multiselect("Select Columns", df.columns)

    # ------------------ PLOT OUTPUT ------------------
    st.markdown("---")

    if plot_full_choice:
        fig = plot_full(df, plot_full_choice[0])
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    if plot_col_choice and cols:
        fig = plot_columns(df, plot_col_choice[0], cols)
        if fig:
            st.plotly_chart(fig, use_container_width=True)