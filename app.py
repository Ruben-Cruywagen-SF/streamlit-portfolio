import streamlit as st
import io
import pandas as pd
import plotly.express as px
from datetime import datetime
from functions import generate_dummy_data, generate_excel_report, generate_ai_summary

st.markdown("""
<style>
body {
    background: linear-gradient(to right, #f0f2f5, #dbe7f7);
}
h1, h2, h3 {
    color: #8db4f2 !important;
}
.stButton>button {
    background-color: #8db4f2 !important;
    color: white !important;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


st.image("logo.jpg", width=300)
st.set_page_config(page_title="Sales Report Generator", layout="wide")
st.title("📊 Sales Report Generator")

generated_report = None

uploaded_file = st.file_uploader("Upload your custom data (CSV or Excel)", type=['csv', 'xlsx'])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state.df = df  # Save uploaded df
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()
else:
    if "df" not in st.session_state:
        st.session_state.df = generate_dummy_data()
    
    csv_buffer = io.StringIO()
    st.session_state.df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    # ---- Download Sample Data ----
    st.markdown("You can download the dummy sales data and replace the data with your own (columns must remain unchanged). <br>Reload the page to generate a new set of random data.", unsafe_allow_html=True)
    st.download_button(
        label="📥 Download Dummy Sales Data",
        data=csv_data,
        file_name="dummy_sales_data.csv",
        mime="text/csv"
        )

expected_columns = {'Date', 'Region', 'Rep', 'Product', 'Sales'}
if not expected_columns.issubset(st.session_state.df.columns):
    st.warning(f"Missing expected columns: {expected_columns - set(st.session_state.df.columns)}")
    st.stop()

st.session_state.df['Date'] = pd.to_datetime(st.session_state.df['Date'])

# ---- Filter Section ----
st.sidebar.header("Filters")

regions = st.sidebar.multiselect("Select Region(s):", options=st.session_state.df['Region'].unique(), default=list(st.session_state.df['Region'].unique()))
reps = st.sidebar.multiselect("Select Sales Rep(s):", options=st.session_state.df['Rep'].unique(), default=list(st.session_state.df['Rep'].unique()))
min_date, max_date = st.session_state.df['Date'].min(), st.session_state.df['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)


filtered_df = st.session_state.df[
    (st.session_state.df['Region'].isin(regions)) &
    (st.session_state.df['Rep'].isin(reps)) &
    (st.session_state.df['Date'] >= pd.to_datetime(date_range[0])) &
    (st.session_state.df['Date'] <= pd.to_datetime(date_range[1]))
]

st.markdown(f"### Filtered Data ({len(filtered_df)} rows)")
st.dataframe(filtered_df)


# ---- Visuals ----
st.markdown("## 📈 Visualizations")

grid_color = 'rgba(200, 200, 200, 0.5)'


# Top Regions
st.subheader("Sales by Region")
product_sales = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=True).reset_index()
fig0 = px.bar(product_sales, x='Sales', y='Region', title="Sales by Region", orientation='h')
fig0.update_layout(
    xaxis=dict(
        showgrid=True,
        gridcolor=grid_color
    )
)
st.plotly_chart(fig0, use_container_width=True)

# Sales by Rep (Pie Chart)
st.subheader("Sales by Rep")
rep_sales = filtered_df.groupby('Rep')['Sales'].sum().sort_values(ascending=False).reset_index()
fig1 = px.pie(rep_sales, names='Rep', values='Sales', title="Sales by Rep")
st.plotly_chart(fig1, use_container_width=True)

# Sales Over Time
st.subheader("Sales Over Time")
filtered_df['Cumulative Sales'] = filtered_df['Sales'].cumsum()
fig2 = px.line(filtered_df, x='Date', y='Cumulative Sales', color='Region', markers=True, title="Cumulative Sales Trend by Region")
fig2.update_layout(
    yaxis=dict(
        showgrid=True,
        gridcolor=grid_color
    )
)
st.plotly_chart(fig2, use_container_width=True)

# Top Products
st.subheader("Top Products")
product_sales = filtered_df.groupby('Product')['Sales'].sum().sort_values(ascending=False).reset_index()
fig3 = px.bar(product_sales, x='Product', y='Sales', title="Total Sales by Product")
fig3.update_layout(
    yaxis=dict(
        showgrid=True,
        gridcolor=grid_color
    )
)
st.plotly_chart(fig3, use_container_width=True)


# ---- Generate Report ----
st.markdown("---")
st.subheader("📥 Excel Report")
generated_report = generate_excel_report(filtered_df.reset_index(drop=True))
with st.spinner("Generating Excel Report..."):
    st.download_button(
        label="Generate and Download Excel Report (selected filters will be applied)",
        data=generated_report,
        file_name=f"Executive Summary Report {datetime.strftime(datetime.now(), '%y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ---- Generate AI Summary ----
st.markdown("---")
st.subheader("🧠 AI Data Summary")
if st.button("Generate"):
    with st.spinner("Generating insight summary..."):
        try:
            generated_ai_summary = generate_ai_summary(filtered_df.reset_index(drop=True))
            st.markdown(generated_ai_summary)
        except Exception as e:
            st.markdown("<span style='color:red'>AI quota limit reached for this dashboard – could not generate insight summary.</span>",
                        unsafe_allow_html=True
                        )

