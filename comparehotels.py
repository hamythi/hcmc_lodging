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
        "Street": ["Downtown", "Arts District", "Beachfront", "Historic Quarter", "Financial District"],
        "District": [5,6,10,11,5],
        "Price ($/Night)": [280, 195, 340, 150, 210],
        "Star Rating": [4.8, 4.5, 4.9, 4.2, 4.4],
        "Review": [10,20,30,40,50],
        "Lift :elevator:": [True, False, True, True, False],
        "Breakfast :ramen:": [True, False, True, True, False],
        "Microwave :hotsprings:": [True, True, False, False, True],
        "Free Wi-Fi :signal_strength:": [True, True, True, True, True],
        "Website": [
            "https://marriott.com",
            "https://hilton.com",
            "https://hyatt.com",
            "https://ihg.com",
            "https://fourseasons.com"
        ]
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
req_lift = st.sidebar.checkbox("Lift")
req_breakfast = st.sidebar.checkbox("Breakfast")
req_microwave = st.sidebar.checkbox("Microwave")
req_wifi = st.sidebar.checkbox("Free Wi-Fi")


# 3. Filtering the Data Logic
filtered_df = df[df["Price ($/Night)"] <= budget]
if req_lift:
    filtered_df = filtered_df[filtered_df["Lift"] == True]
if req_breakfast:
    filtered_df = filtered_df[filtered_df["Breakfast"] == True]
if req_microwave:
    filtered_df = filtered_df[filtered_df["Microwave"] == True]
if req_wifi:
    filtered_df = filtered_df[filtered_df["Free Wifi"] == True]

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
st.subheader("📋 Available Hotel Profiles")

if filtered_df.empty:
    st.warning("No hotels match your filters.")
else:
    # Text-only card layout
    for index, row in filtered_df.iterrows():
        with st.container(border=True):
            # Header info
            st.subheader(row["Hotel Name"])
            st.caption(f"📍 Location: {row['Street']} | ⭐ Rating: {row['Star Rating']}/5")
            st.markdown(f"### **${row['Price ($/Night)']}** / night")
            
            # Amenities row
            lift_status = "✅ Lift" if row["Lift"] else "❌ No Lift"
            bfast_status = "✅ Breakfast" if row["Breakfast"] else "❌ No Breakfast"
            micro_status = "✅ Microwave" if row["Microwave"] else "❌ No Microwave"
            wifi_status = "✅ Free Wi-Fi" if row["Free Wi-Fi"] else "❌ No Wi-Fi"
            st.markdown(f"{lift_status}  •  {bfast_status}  •  {micro_status}  •  {wifi_status}")
            
            # Clickable website link button
            st.link_button(label="🔗 View Hotel Website", url=row["Website"])
