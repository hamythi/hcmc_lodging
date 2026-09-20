import streamlit as st
import pandas as pd
import plotly.express as px

# Set up clean, professional page layout
st.set_page_config(page_title="Hotel Comparison Dashboard", layout="wide")

st.title("🏨 Client Hotel Comparison Dashboard")
st.markdown("Use the filters on the left sidebar to narrow down choices based on budget and must-have amenities.")

# 1. Mock Data Set (Replace this with your client's curated list or CSV)
@st.cache_data
def load_hotel_data():
    data = {
        "Hotel Name": ["The Grand Luminary", "Urban Oasis Suites", "Coastal Crest Resort", "The Heritage Inn", "Metro Horizon Stay"],
        "Neighborhood": ["Downtown", "Arts District", "Beachfront", "Historic Quarter", "Financial District"],
        "Price ($/Night)": [280, 195, 340, 150, 210],
        "Star Rating": [4.8, 4.5, 4.9, 4.2, 4.4],
        "Pool": [True, True, True, False, False],
        "Free Breakfast": [True, False, True, True, False],
        "Gym": [True, True, False, False, True],
        "Free Wi-Fi": [True, True, True, True, True]
    }
    return pd.DataFrame(data)

df = load_hotel_data()

# 2. Sidebar Controls for Your Client
st.sidebar.header("Filter Options")

# Budget slider
max_price = int(df["Price ($/Night)"].max())
min_price = int(df["Price ($/Night)"].min())
budget = st.sidebar.slider("Maximum Price per Night ($)", min_price, max_price, max_price)

# Amenity checkboxes
st.sidebar.subheader("Required Amenities")
req_pool = st.sidebar.checkbox("Pool")
req_breakfast = st.sidebar.checkbox("Free Breakfast")
req_gym = st.sidebar.checkbox("Gym")

# 3. Filtering the Data Logic
filtered_df = df[df["Price ($/Night)"] <= budget]
if req_pool:
    filtered_df = filtered_df[filtered_df["Pool"] == True]
if req_breakfast:
    filtered_df = filtered_df[filtered_df["Free Breakfast"] == True]
if req_gym:
    filtered_df = filtered_df[filtered_df["Gym"] == True]

# 4. Display Overview Metric Cards
st.subheader("Quick Overview")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Options Found", value=len(filtered_df))
if not filtered_df.empty:
    kpi2.metric(label="Average Price", value=f"${int(filtered_df['Price ($/Night)'].mean())}/night")
    kpi3.metric(label="Top Rated Option", value=filtered_df.loc[filtered_df['Star Rating'].idxmax()]['Hotel Name'])
else:
    kpi2.metric(label="Average Price", value="N/A")
    kpi3.metric(label="Top Rated Option", value="N/A")

st.markdown("---")

# 5. Interactive Comparison Table & Price Visuals
if filtered_df.empty:
    st.warning("No hotels match your current filter combination. Try loosening your budget or amenity criteria!")
else:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("📋 Hotel Features Matrix")
        # Format true/false values into clean checkmarks for client readability
        display_df = filtered_df.copy()
        for amenity in ["Pool", "Free Breakfast", "Gym", "Free Wi-Fi"]:
            display_df[amenity] = display_df[amenity].apply(lambda x: "✅" if x else "❌")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("💰 Price vs. Rating Value")
        # Generate chart to show client value optimization
        fig = px.scatter(
            filtered_df, 
            x="Price ($/Night)", 
            y="Star Rating", 
            text="Hotel Name",
            size=[15]*len(filtered_df), 
            color="Neighborhood",
            hover_name="Hotel Name",
            labels={"Price ($/Night)": "Price ($/Night)", "Star Rating": "Guest Rating (Out of 5)"}
        )
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)