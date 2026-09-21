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
        "Hotel Name": ["Golda Hotel", "Zazz Urban Ho Chi Minh Hotel", 
                       "Tuong Vi", "Hong Phat", "Everich Infinity - China Town Apartment", 
                       "DHTS Business Hotel & Apartment"],
        "Street": ["Thuan Kieu", "An Dong, Cho Lon & Pho Co Dieu", 
                   "3 Thang 2 & Ngo Quyen", "Cho Thiet & Ly Thuong Kiet", 
                   "An Duong Vuong", "3 Thang 2 & Ly Thuong Kiet"],
        "District": [5,5,10,11,5,10],
        "Price ($/Night)": [28, 40, 30, 17, 42, 57],
        "Star Rating": [7.8, 9.0, 8.6, 7.8, 9.0, 9.8],
        "Review": [96,280,168,236,29,37],
        "Year": [2018,2019,2018,2022,2016,2021],
        "Lift": [True, True, True, True, True, True],
        "Breakfast": [True, True, True, True, True, True],
        "Fridge": [True, True, True, True, True, True],
        "AC": [True, True, True, True, True, True],        
        "Microwave": [False, False, False, False, True, True],
        "Free Wi-Fi": [True, True, True, True, True, True],
        "Website": [
            "https://www.expedia.com/Ho-Chi-Minh-City-Hotels-Golda-Hotel.h29505017.Hotel-Information?chkin=2026-09-21&chkout=2026-09-27&x_pwa=1&rfrr=HSR&pwa_ts=1789942903312&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jb20vSG90ZWwtU2VhcmNo&useRewards=false&rm1=a1&regionId=959752201732198400&destination=Ho+Chi+Minh+Municipality%2C+Vietnam&destType=MARKET&neighborhoodId=1035688369375793152&selected=29505017&latLong=9.668504%2C107.170894&sort=RECOMMENDED&top_dp=186&top_cur=USD&userIntent=&selectedRoomType=216619306&selectedRatePlan=264072331&categorySearch=any_option&searchId=7a21ea43-2362-4fe9-9d98-ca1ea717c727",
            "https://www.expedia.com/Ho-Chi-Minh-City-Hotels-Zazz-Urban-Ho-Chi-Minh-Hotel.h36469140.Hotel-Information?chkin=2026-09-29&chkout=2026-09-30&x_pwa=1&rfrr=HSR&pwa_ts=1789943758133&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jb20vSG90ZWwtU2VhcmNo&useRewards=false&rm1=a2&regionId=959752201732198400&destination=Ho+Chi+Minh+Municipality%2C+Vietnam&destType=MARKET&neighborhoodId=1035688369627467776&selected=36469140&latLong=9.668504%2C107.170894&mpo=EC&sort=RECOMMENDED&top_dp=52&top_cur=USD&gclid=EAIaIQobChMI6vLZipz-lgMV3dbCBB11MSldEAoYASABEgJpa_D_BwE&mctc=10&userIntent=&selectedRoomType=218151427&selectedRatePlan=274184616&categorySearch=any_option&searchId=f3581831-6e3c-497a-973e-c55b085813df&containsVideo=false",
            "https://www.expedia.com/Ho-Chi-Minh-City-Hotels-Tuong-Vi-Corner-Hotel.h122452827.Hotel-Information?chkin=2026-09-29&chkout=2026-09-30&x_pwa=1&rfrr=HSR&pwa_ts=1789943771765&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jb20vSG90ZWwtU2VhcmNo&useRewards=false&rm1=a2&regionId=959752201732198400&destination=Ho+Chi+Minh+Municipality%2C+Vietnam&destType=MARKET&neighborhoodId=1035688371733016576&selected=122452827&latLong=9.668504%2C107.170894&mpo=EC&sort=RECOMMENDED&top_dp=39&top_cur=USD&gclid=EAIaIQobChMIrs3Vkpz-lgMV7AytBh0OJBHSEAoYASABEgJ2ZfD_BwE&mctc=10&userIntent=&selectedRoomType=327607736&selectedRatePlan=405626787&categorySearch=any_option&searchId=a1b66080-a922-4c0f-8367-377eed00c253&containsVideo=false",
            "https://www.booking.com/hotel/vn/khach-san-hong-phat.html?aid=356929&label=metagha-link-MRUS-hotel-8783638_dev-desktop_los-1_bw-13_dow-Sunday_defdate-1_room-0_gstadt-2_rateid-public_aud-0_gacid-21411073835_mcid-10_ppa-0_clrid-0_ad-1_gstkid-0_checkin-20261004_ppt-Bd_lp-2840_r-9566502847788394632&sid=882e85a9e9b837dac8fdfe5cd6029ee3&all_sr_blocks=878363805_356917939_2_0_0&checkin=2026-10-04&checkout=2026-10-05&dest_id=8783638&dest_type=hotel&dist=0&group_adults=2&group_children=0&hapos=1&highlighted_blocks=878363805_356917939_2_0_0&hpos=1&matching_block_id=878363805_356917939_2_0_0&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&sr_pri_blocks=878363805_356917939_2_0_0__42950000&srepoch=1789943921&srpvid=45bf9f08306f01fc&type=total&ucfs=1&",
            "https://www.booking.com/hotel/vn/everich-infinity-290-adv.html?aid=318615&label=New_English_EN_CA%3A_California_23537601985-3kcHFhwdf%2AgW7%2AEv3C_0FgS813130216034%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwl-64415224945%3Alp9060360%3Ali%3Adec%3Adm%3Aag23537601985%3Acmp363161665&sid=882e85a9e9b837dac8fdfe5cd6029ee3&all_sr_blocks=1136735201_386287934_2_0_0&checkin=2026-09-29&checkout=2026-09-30&dest_id=-3730078&dest_type=city&dist=0&group_adults=2&group_children=0&hapos=1&highlighted_blocks=1136735201_386287934_2_0_0&hpos=1&matching_block_id=1136735201_386287934_2_0_0&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&sr_pri_blocks=1136735201_386287934_2_0_0__108333333&srepoch=1789944969&srpvid=33c5a142dac70308&type=total&ucfs=1&#tab-main",
            "https://www.expedia.com/Ho-Chi-Minh-City-Hotels-DHTS-Business-Hotel-Apartment.h110693772.Hotel-Information?chkin=2026-09-23&chkout=2026-09-24&x_pwa=1&rfrr=HSR&pwa_ts=1789965626582&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jb20vSG90ZWwtU2VhcmNo&useRewards=false&rm1=a2&regionId=959752201732198400&destination=Ho+Chi+Minh+Municipality%2C+Vietnam&destType=MARKET&neighborhoodId=553248635976386566&selected=110693772&latLong=9.668504%2C107.170894&mpo=EC&sort=RECOMMENDED&top_dp=52&top_cur=USD&gclid=EAIaIQobChMIje2Qxu3-lgMVquTCBB3b-RXOEAoYAiABEgJDh_D_BwE&mctc=10&userIntent=&selectedRoomType=325662442&selectedRatePlan=401285161&categorySearch=any_option&searchId=bea5e1bf-e0c2-4362-9b97-5b413e9c07f2&containsVideo=false"
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
req_fridge = st.sidebar.checkbox("Fridge")
req_ac = st.sidebar.checkbox("AC")
req_microwave = st.sidebar.checkbox("Microwave")
req_wifi = st.sidebar.checkbox("Free Wi-Fi")


# 3. Filtering the Data Logic
filtered_df = df[df["Price ($/Night)"] <= budget]
if req_lift:
    filtered_df = filtered_df[filtered_df["Lift"] == True]
if req_breakfast:
    filtered_df = filtered_df[filtered_df["Breakfast"] == True]
if req_fridge:
    filtered_df = filtered_df[filtered_df["Fridge"] == True]
if req_ac:
    filtered_df = filtered_df[filtered_df["AC"] == True]
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
            st.caption(f"📍 Location: {row['Street']} | ⭐ Rating: {row['Star Rating']}/10 | Review: {row['Review']}")
            st.caption(f"Year: {row['Street']}")
            st.markdown(f"### **${row['Price ($/Night)']}** / night")
            
            # Amenities row
            lift_status = "✅ Lift" if row["Lift"] else "❌ No Lift"
            bfast_status = "✅ Breakfast" if row["Breakfast"] else "❌ No Breakfast"
            fridge_status = "✅ Fridge" if row["Fridge"] else "❌ No Fridge"
            ca_status = "✅ Fridge" if row["AC"] else "❌ No AC"
            micro_status = "✅ Microwave" if row["Microwave"] else "❌ No Microwave"
            wifi_status = "✅ Free Wi-Fi" if row["Free Wi-Fi"] else "❌ No Wi-Fi"
            st.markdown(f"{lift_status}  •  {bfast_status}  •  {micro_status}  •  {wifi_status}")
            
            # Clickable website link button
            st.link_button(label="🔗 View Hotel Website", url=row["Website"])
