import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("swiggy.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# City filter
city_list = df["City"].dropna().unique()
selected_city = st.sidebar.selectbox("Select City", options=["All"] + sorted(city_list.tolist()))

# Food type filter
food_types = df["Food type"].dropna().unique()
selected_food_types = st.sidebar.multiselect("Select Food Types", options=sorted(food_types), default=sorted(food_types))

# Price range slider
min_price = int(df["Price"].min())
max_price = int(df["Price"].max())
selected_price_range = st.sidebar.slider("Select Price Range", min_price, max_price, (min_price, max_price))

# Apply filters
filtered_df = df[
    (df["Price"] >= selected_price_range[0]) &
    (df["Price"] <= selected_price_range[1]) &
    (df["Food type"].isin(selected_food_types))
]

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

# Page title
st.title("🍔 Swiggy Restaurant Dashboard")

# Show summary metrics
st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Restaurants", len(filtered_df))
col2.metric("Average Rating", round(filtered_df["Avg ratings"].mean(), 2) if not filtered_df.empty else "N/A")
col3.metric("Average Price", f"₹{int(filtered_df['Price'].mean())}" if not filtered_df.empty else "N/A")

# Show data table
st.subheader("📋 Restaurant Listings")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# Bar Chart: Average Rating per Top 10 Restaurants
st.subheader("⭐ Top Rated Restaurants (Bar Chart)")
if not filtered_df.empty:
    top_rated = filtered_df.sort_values(by="Avg ratings", ascending=False).head(10)
    st.bar_chart(top_rated.set_index("Restaurant")["Avg ratings"])

# Line Chart: Price Trend Across Restaurants
st.subheader("💰 Price Comparison (Line Chart)")
if not filtered_df.empty:
    st.line_chart(filtered_df.sort_values(by="Price").set_index("Restaurant")["Price"])

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Pandas")
