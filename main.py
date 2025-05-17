import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("swiggy.csv")
    df.columns = df.columns.str.strip()  # Remove extra whitespace
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

# City filter
city_options = df["City"].dropna().unique()
selected_city = st.sidebar.selectbox("Select City", options=["All"] + list(city_options))

# Food Type filter
food_options = df["Food type"].dropna().unique()
selected_food = st.sidebar.multiselect("Select Food Type", options=food_options, default=list(food_options))

# Price filter
min_price = int(df["Price"].min())
max_price = int(df["Price"].max())
price_range = st.sidebar.slider("Select Price Range", min_price, max_price, (min_price, max_price))

# Filter data
filtered_df = df[
    (df["Price"] >= price_range[0]) &
    (df["Price"] <= price_range[1]) &
    (df["Food type"].isin(selected_food))
]

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

# Main Title
st.title("🍽️ Swiggy Restaurant Explorer")

# Summary metrics
st.markdown("### 📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Restaurants", len(filtered_df))
col2.metric("Avg. Rating", round(filtered_df["Avg ratings"].mean(), 2))
col3.metric("Avg. Price", f"₹{int(filtered_df['Price'].mean())}")

# Data Table
st.markdown("### 📋 Restaurant Listings")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# Bar Chart - Top restaurants by average rating
st.markdown("### ⭐ Top Rated Restaurants")
top_rated = filtered_df.sort_values(by="Avg ratings", ascending=False).head(10)
fig1 = px.bar(top_rated, x="Restaurant", y="Avg ratings", color="City", title="Top 10 Restaurants by Average Rating")
st.plotly_chart(fig1, use_container_width=True)

# Pie Chart - Distribution of Food Types
st.markdown("### 🥘 Food Type Distribution")
food_counts = filtered_df["Food type"].value_counts().reset_index()
food_counts.columns = ["Food type", "Count"]
fig2 = px.pie(food_counts, values="Count", names="Food type", title="Food Type Distribution")
st.plotly_chart(fig2, use_container_width=True)

# Box Plot - Price Distribution by City
st.markdown("### 💰 Price Distribution by City")
if selected_city == "All":
    fig3 = px.box(filtered_df, x="City", y="Price", color="City", title="Price Distribution Across Cities")
    st.plotly_chart(fig3, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit and Plotly")

