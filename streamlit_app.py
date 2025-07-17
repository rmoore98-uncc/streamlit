import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
option = st.selectbox(
    "Select a Category",
    df["Category"].unique()
)
filtered_df = df[df["Category"] == option]

# Multi-select for Sub_Category within selected Category
sub_options = filtered_df["Sub_Category"].unique()
selected_subs = st.multiselect("Select Sub-Categories", sub_options)

# Filter by selected Sub_Categories
if selected_subs:
    filtered_df = filtered_df[filtered_df["Sub_Category"].isin(selected_subs)]

# Display the filtered data
st.dataframe(filtered_df)

filtered_df = df[df["Category"] == option]

st.write("### Input Data and Examples")


# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(filtered_df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(filtered_df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(filtered_df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
filtered_df["Order_Date"] = pd.to_datetime(filtered_df["Order_Date"])
filtered_df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

# Filter by Category
filtered_df = df[df["Category"] == option]

# Optionally filter by selected Sub-Categories
if selected_subs:
    filtered_df = filtered_df[filtered_df["Sub_Category"].isin(selected_subs)]

# Convert Order_Date to datetime and set as index
filtered_df["Order_Date"] = pd.to_datetime(filtered_df["Order_Date"])
filtered_df.set_index('Order_Date', inplace=True)

# Group by Sub-Category and Month, sum Sales
sales_by_sub_month = (
    filtered_df
    .groupby([pd.Grouper(freq='M'), 'Sub_Category'])['Sales']
    .sum()
    .unstack('Sub_Category')
)

# Sub-category Line Chart Display
st.line_chart(sales_by_sub_month)

# Create st.metrics

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
overall_profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

# Calculate overall average profit margin (for all data)
overall_avg_profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100 if df['Sales'].sum() != 0 else 0
delta_margin = overall_profit_margin - overall_avg_profit_margin

st.metric(
    label="Profit Margin (%)",
    value=f"{overall_profit_margin:.2f}%",
    delta=f"{delta_margin:.2f}%"
)

# Metric Display
st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
st.metric(label="Profit Margin (%)", value=f"{overall_profit_margin:.2f}%")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
