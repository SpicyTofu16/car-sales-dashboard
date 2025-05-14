import streamlit as st
import pandas as pd
import plotly.express as px

# Loading data
df = pd.read_csv("vehicles_us.csv")

# Sidebar
st.sidebar.header("Filter Listings")
vehicle_types = st.sidebar.multiselect("Select Vehicle Type:", options=df["type"].unique(), default=df["type"].unique())
price_range = st.sidebar.slider("Select Price Range:", int(df["price"].min()), int(df["price"].max()), (5000, 50000))
conditions = st.sidebar.multiselect("Select Condition:", options=df["condition"].dropna().unique(), default=df["condition"].dropna().unique())

# Filtering data
filtered_df = df[
    (df["type"].isin(vehicle_types)) &
    (df["price"].between(*price_range)) &
    (df["condition"].isin(conditions))
]

# Title
st.title("Car Listings Dashboard")
st.markdown("Explore used car listings with filters and visuals.")

# Metricss
st.subheader("Summary Metrics")
col1, col2 = st.columns(2)
col1.metric("Average Price", f"${int(filtered_df['price'].mean()):,}")
col2.metric("Listings Count", f"{filtered_df.shape[0]:,}")

# Charts
st.subheader("Distribution of Vehicle Prices")
fig_price = px.histogram(filtered_df, x="price", nbins=50, title="Price Distribution")
st.plotly_chart(fig_price)

st.subheader("Price vs Odometer")
fig_scatter = px.scatter(filtered_df, x="odometer", y="price", title="Odometer vs Price")
st.plotly_chart(fig_scatter)

st.subheader("Average Price by Vehicle Type")
avg_price_type = filtered_df.groupby("type")["price"].mean().reset_index()
fig_bar = px.bar(avg_price_type, x="type", y="price", title="Average Price by Type")
st.plotly_chart(fig_bar)

# existing charts
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Dataset")
    st.write(filtered_df)
