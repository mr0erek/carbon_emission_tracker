####################################
#  Summer Intership Project Day-1  #
#  Author     : @m0erek            #
#  Written By : Claude.ai          # 
#  Instructor : @Arjunvankani      #
####################################

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="🌱 Carbon Emission Tracker",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2d5a3d;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
            
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }

    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'weekly_data' not in st.session_state:
    st.session_state.weekly_data = {
        'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [],
        'Friday': [], 'Saturday': [], 'Sunday': []
    }

if 'user_info' not in st.session_state:
    st.session_state.user_info = {'name': '', 'city': ''}

# Vehicle emission factors (kg CO2 per km) and fuel costs (₹ per km)
VEHICLE_DATA = {
    'Car (Petrol)': {'emission': 0.21, 'cost': 8.5, 'icon': '🚗'},
    'Car (Diesel)': {'emission': 0.17, 'cost': 7.2, 'icon': '🚗'},
    'Motorcycle': {'emission': 0.12, 'cost': 3.5, 'icon': '🏍️'},
    'Bus': {'emission': 0.08, 'cost': 2.0, 'icon': '🚌'},
    'Train': {'emission': 0.04, 'cost': 1.5, 'icon': '🚆'},
    'Bicycle': {'emission': 0.0, 'cost': 0.0, 'icon': '🚴'},
    'Walking': {'emission': 0.0, 'cost': 0.0, 'icon': '🚶'},
    'Electric Car': {'emission': 0.05, 'cost': 1.8, 'icon': '⚡'},
    'Auto Rickshaw': {'emission': 0.15, 'cost': 4.5, 'icon': '🛺'},
    'Taxi/Cab': {'emission': 0.19, 'cost': 12.0, 'icon': '🚕'}
}

DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def main():
    # Header
    st.markdown('<h1 class="main-header">🌱 Carbon Emission Tracker</h1>', unsafe_allow_html=True)
    
    # Sidebar for user information and navigation
    with st.sidebar:
        st.header("👤 Personal Information")
        name = st.text_input("Name", value=st.session_state.user_info['name'])
        city = st.text_input("City", value=st.session_state.user_info['city'])
        
        if name and city:
            st.session_state.user_info = {'name': name, 'city': city}
            st.success(f"Hello {name} from {city}!")
        
        st.markdown("---")
        
        # Navigation
        st.header("📍 Navigation")
        page = st.selectbox("Choose Section:", 
                           ["📝 Add Travel Data", "📊 Weekly Overview", "📈 Analytics", "📋 Detailed Report"])
    
    # Main content based on selected page
    if page == "📝 Add Travel Data":
        add_travel_data_page()
    elif page == "📊 Weekly Overview":
        weekly_overview_page()
    elif page == "📈 Analytics":
        analytics_page()
    elif page == "📋 Detailed Report":
        detailed_report_page()

def add_travel_data_page():
    st.header("📝 Add Your Daily Travel Data")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🗓️ Select Day")
        selected_day = st.selectbox("Choose day of the week:", DAYS_OF_WEEK)
        
        st.subheader("🚗 Vehicle Information")
        vehicle_options = list(VEHICLE_DATA.keys())
        vehicle_display = [f"{VEHICLE_DATA[v]['icon']} {v}" for v in vehicle_options]
        
        selected_vehicle_display = st.selectbox("Select Vehicle Type:", vehicle_display)
        selected_vehicle = vehicle_options[vehicle_display.index(selected_vehicle_display)]
        
        destination = st.text_input("🎯 Destination/Location", placeholder="e.g., Bardoli to Rngpit")
        distance = st.number_input("📏 Distance (km)", min_value=0.1, max_value=1000.0, value=1.0, step=0.1)
    
    with col2:
        st.subheader("💡 Trip Preview")
        if destination and distance > 0:
            emission = distance * VEHICLE_DATA[selected_vehicle]['emission']
            cost = distance * VEHICLE_DATA[selected_vehicle]['cost']
            
            st.info(f"""
            **Trip Summary:**
            - 📅 Day: {selected_day}
            - {VEHICLE_DATA[selected_vehicle]['icon']} Vehicle: {selected_vehicle}
            - 🎯 Destination: {destination}
            - 📏 Distance: {distance} km
            - 💰 Estimated Fuel Cost: ₹{cost:.2f}
            - 🌿 CO₂ Emission: {emission:.2f} kg
            """)
            
            # Environmental impact
            if emission > 0:
                trees_needed = max(1, int(emission / 22))  # 1 tree absorbs ~22kg CO2/year
                st.warning(f"🌳 Trees needed to offset this trip: {trees_needed} tree(s) per year")
        
        if st.button("➕ Add Trip", type="primary", use_container_width=True):
            if destination and distance > 0:
                trip_data = {
                    'vehicle': selected_vehicle,
                    'destination': destination,
                    'distance': distance,
                    'emission': distance * VEHICLE_DATA[selected_vehicle]['emission'],
                    'cost': distance * VEHICLE_DATA[selected_vehicle]['cost'],
                    'timestamp': datetime.now().strftime("%H:%M")
                }
                
                st.session_state.weekly_data[selected_day].append(trip_data)
                st.success(f"✅ Trip added successfully for {selected_day}!")
                st.rerun()
            else:
                st.error("❌ Please fill in all fields!")
    
    # Display current day's trips
    if st.session_state.weekly_data[selected_day]:
        st.subheader(f"📋 {selected_day}'s Trips")
        trips_df = pd.DataFrame(st.session_state.weekly_data[selected_day])
        
        # Format the dataframe for display
        display_df = trips_df.copy()
        display_df['Vehicle'] = display_df['vehicle'].apply(lambda x: f"{VEHICLE_DATA[x]['icon']} {x}")
        display_df['Distance (km)'] = display_df['distance'].round(1)
        display_df['Cost (₹)'] = display_df['cost'].round(2)
        display_df['CO₂ (kg)'] = display_df['emission'].round(2)
        display_df['Time Added'] = display_df['timestamp']
        
        st.dataframe(display_df[['Vehicle', 'destination', 'Distance (km)', 'Cost (₹)', 'CO₂ (kg)', 'Time Added']], 
                    use_container_width=True)
        
        # Option to clear day's data
        if st.button(f"🗑️ Clear {selected_day}'s Data", type="secondary"):
            st.session_state.weekly_data[selected_day] = []
            st.success(f"✅ {selected_day}'s data cleared!")
            st.rerun()

def weekly_overview_page():
    st.header("📊 Weekly Overview")
    
    # Calculate daily totals
    daily_totals = {}
    for day in DAYS_OF_WEEK:
        trips = st.session_state.weekly_data[day]
        if trips:
            daily_totals[day] = {
                'trips': len(trips),
                'distance': sum(trip['distance'] for trip in trips),
                'emission': sum(trip['emission'] for trip in trips),
                'cost': sum(trip['cost'] for trip in trips)
            }
        else:
            daily_totals[day] = {'trips': 0, 'distance': 0, 'emission': 0, 'cost': 0}
    
    # Overall metrics
    total_emission = sum(day['emission'] for day in daily_totals.values())
    total_cost = sum(day['cost'] for day in daily_totals.values())
    total_distance = sum(day['distance'] for day in daily_totals.values())
    total_trips = sum(day['trips'] for day in daily_totals.values())
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌿 Total CO₂ Emission", f"{total_emission:.2f} kg")
    with col2:
        st.metric("💰 Total Fuel Cost", f"₹{total_cost:.2f}")
    with col3:
        st.metric("🛣️ Total Distance", f"{total_distance:.1f} km")
    with col4:
        st.metric("🚗 Total Trips", f"{total_trips}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily emissions chart
        emission_data = [daily_totals[day]['emission'] for day in DAYS_OF_WEEK]
        
        # Create DataFrame for proper plotting
        chart_df = pd.DataFrame({
            'Day': DAYS_OF_WEEK,
            'Emission': emission_data
        })
        
        fig_emission = px.bar(
            chart_df,
            x='Day', 
            y='Emission',
            title="📈 Daily CO₂ Emissions (kg)",
            labels={'Emission': 'CO₂ Emission (kg)'},
            color='Emission',
            color_continuous_scale='Reds'
        )
        fig_emission.update_layout(showlegend=False)
        st.plotly_chart(fig_emission, use_container_width=True)
    
    with col2:
        # Daily costs chart
        cost_data = [daily_totals[day]['cost'] for day in DAYS_OF_WEEK]
        
        # Create DataFrame for proper plotting
        chart_df = pd.DataFrame({
            'Day': DAYS_OF_WEEK,
            'Cost': cost_data
        })
        
        fig_cost = px.bar(
            chart_df,
            x='Day', 
            y='Cost',
            title="💰 Daily Fuel Costs (₹)",
            labels={'Cost': 'Cost (₹)'},
            color='Cost',
            color_continuous_scale='Blues'
        )
        fig_cost.update_layout(showlegend=False)
        st.plotly_chart(fig_cost, use_container_width=True)
    
    # Weekly summary table
    st.subheader("📋 Weekly Summary Table")
    summary_df = pd.DataFrame(daily_totals).T
    summary_df.index.name = 'Day'
    summary_df.columns = ['Trips', 'Distance (km)', 'CO₂ (kg)', 'Cost (₹)']
    summary_df = summary_df.round(2)
    st.dataframe(summary_df, use_container_width=True)

def analytics_page():
    st.header("📈 Advanced Analytics")
    
    # Collect all trip data
    all_trips = []
    for day, trips in st.session_state.weekly_data.items():
        for trip in trips:
            trip_copy = trip.copy()
            trip_copy['day'] = day
            all_trips.append(trip_copy)
    
    if not all_trips:
        st.warning("⚠️ No data available. Please add some travel data first!")
        return
    
    trips_df = pd.DataFrame(all_trips)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Vehicle usage pie chart
        vehicle_usage = trips_df['vehicle'].value_counts()
        fig_pie = px.pie(
            values=vehicle_usage.values,
            names=vehicle_usage.index,
            title="🚗 Vehicle Usage Distribution"
        )
        fig_pie.update_traces(hovertemplate='<b>%{label}</b><br>Trips: %{value}<br>Percentage: %{percent}<extra></extra>')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Top destinations
        st.subheader("🎯 Top Destinations")
        dest_counts = trips_df['destination'].value_counts().head(5)
        for i, (dest, count) in enumerate(dest_counts.items(), 1):
            st.write(f"{i}. **{dest}** - {count} trip(s)")
    
    with col2:
        # Emission by vehicle type
        vehicle_emissions = trips_df.groupby('vehicle')['emission'].sum().sort_values(ascending=True)
        
        # Create DataFrame for horizontal bar chart
        vehicle_chart_df = pd.DataFrame({
            'Vehicle': vehicle_emissions.index,
            'Total_Emission': vehicle_emissions.values
        })
        
        fig_vehicle_emission = px.bar(
            vehicle_chart_df,
            x='Total_Emission',
            y='Vehicle',
            orientation='h',
            title="🌿 CO₂ Emissions by Vehicle Type",
            labels={'Total_Emission': 'Total CO₂ (kg)', 'Vehicle': 'Vehicle Type'},
            color='Total_Emission',
            color_continuous_scale='RdYlGn_r'
        )
        fig_vehicle_emission.update_layout(showlegend=False)
        st.plotly_chart(fig_vehicle_emission, use_container_width=True)
        
        # Environmental impact
        st.subheader("🌍 Environmental Impact")
        total_emission = trips_df['emission'].sum()
        trees_needed = max(1, int(total_emission / 22))
        petrol_equivalent = total_emission / 2.3
        
        st.info(f"""
        **Weekly Environmental Impact:**
        - 🌳 Trees needed for offset: {trees_needed} trees/year
        - ⛽ Equivalent petrol burned: {petrol_equivalent:.1f} liters
        - 🏠 Equivalent to powering a home for: {total_emission/10:.1f} days
        """)
    
    # Distance vs Emission scatter plot
    st.subheader("📊 Distance vs CO₂ Emission Analysis")
    fig_scatter = px.scatter(
        trips_df, 
        x='distance', 
        y='emission',
        color='vehicle',
        size='cost',
        hover_name='destination',
        title="Distance vs CO₂ Emission by Vehicle Type",
        labels={'distance': 'Distance (km)', 'emission': 'CO₂ Emission (kg)'}
    )
    fig_scatter.update_traces(
        hovertemplate='<b>%{hovertext}</b><br>' +
                     'Distance: %{x} km<br>' +
                     'CO₂: %{y:.2f} kg<br>' +
                     'Vehicle: %{fullData.name}<br>' +
                     '<extra></extra>'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

def detailed_report_page():
    st.header("📋 Detailed Carbon Emission Report")
    
    if not st.session_state.user_info['name'] or not st.session_state.user_info['city']:
        st.warning("⚠️ Please fill in your personal information in the sidebar first!")
        return
    
    # Calculate comprehensive statistics
    all_trips = []
    daily_emissions = []
    
    for day, trips in st.session_state.weekly_data.items():
        day_emission = sum(trip['emission'] for trip in trips)
        daily_emissions.append(day_emission)
        
        for trip in trips:
            trip_copy = trip.copy()
            trip_copy['day'] = day
            all_trips.append(trip_copy)
    
    if not all_trips:
        st.warning("⚠️ No travel data available. Please add some trips first!")
        return
    
    trips_df = pd.DataFrame(all_trips)
    
    # Calculate statistics
    total_emission = trips_df['emission'].sum()
    total_cost = trips_df['cost'].sum()
    total_distance = trips_df['distance'].sum()
    avg_daily_emission = total_emission / 7
    
    non_zero_emissions = [e for e in daily_emissions if e > 0]
    max_emission = max(non_zero_emissions) if non_zero_emissions else 0
    min_emission = min(non_zero_emissions) if non_zero_emissions else 0
    
    # Display report
    st.markdown(f"""
    ## 🌱 Carbon Footprint Report
    
    **Personal Information:**
    - 👤 **Name:** {st.session_state.user_info['name']}
    - 🏙️ **City:** {st.session_state.user_info['city']}
    - 📅 **Report Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M')}
    
    ---
    
    ## 📊 Weekly Summary
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌿 Total CO₂ Emission", f"{total_emission:.2f} kg")
        st.metric("📈 Max Daily Emission", f"{max_emission:.2f} kg")
    with col2:
        st.metric("💰 Total Fuel Cost", f"₹{total_cost:.2f}")
        st.metric("📉 Min Daily Emission", f"{min_emission:.2f} kg")
    with col3:
        st.metric("🛣️ Total Distance", f"{total_distance:.1f} km")
        st.metric("📊 Avg Daily Emission", f"{avg_daily_emission:.2f} kg")
    
    # Environmental impact analysis
    st.markdown("## 🌍 Environmental Impact Analysis")
    
    trees_needed = max(1, int(total_emission / 22))
    petrol_equivalent = total_emission / 2.3
    home_power_days = total_emission / 10
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        **Carbon Offset Requirements:**
        - 🌳 Trees needed: **{trees_needed} trees/year**
        - ⛽ Petrol equivalent: **{petrol_equivalent:.1f} liters**
        - 🏠 Home power equivalent: **{home_power_days:.1f} days**
        """)
    
    with col2:
        # Environmental rating
        if avg_daily_emission < 2:
            rating = "🟢 Excellent"
            message = "Great job! Your carbon footprint is very low."
        elif avg_daily_emission < 5:
            rating = "🟡 Good"
            message = "Good work! Consider using more eco-friendly transport."
        elif avg_daily_emission < 10:
            rating = "🟠 Moderate"
            message = "Room for improvement. Try reducing car usage."
        else:
            rating = "🔴 High"
            message = "High emissions. Consider sustainable alternatives."
        
        st.warning(f"""
        **Environmental Rating:** {rating}
        
        {message}
        """)
    
    # Recommendations
    st.markdown("## 💡 Personalized Recommendations")
    
    # Analyze most used vehicle
    most_used_vehicle = trips_df['vehicle'].mode().iloc[0] if not trips_df.empty else None
    highest_emission_vehicle = trips_df.groupby('vehicle')['emission'].sum().idxmax() if not trips_df.empty else None
    
    recommendations = []
    
    if most_used_vehicle in ['Car (Petrol)', 'Car (Diesel)']:
        recommendations.append("🚌 Consider using public transport for daily commutes")
        recommendations.append("🚴 Try cycling or walking for short distances (<5km)")
    
    if highest_emission_vehicle in ['Car (Petrol)', 'Car (Diesel)']:
        recommendations.append("⚡ Consider switching to an electric or hybrid vehicle")
        recommendations.append("🚗 Practice eco-driving: maintain steady speeds and proper tire pressure")
    
    if total_distance > 200:  # High weekly distance
        recommendations.append("🏠 Consider working from home some days to reduce commuting")
        recommendations.append("🛒 Combine multiple trips into single journeys")
    
    recommendations.extend([
        "🚶 Walk or cycle for trips under 3km",
        "🚇 Use public transportation when available",
        "🚗 Carpool with colleagues or friends",
        "🌱 Plant trees to offset your carbon footprint",
        "⚡ Consider electric vehicles for future purchases"
    ])
    
    for i, rec in enumerate(recommendations[:8], 1):
        st.write(f"{i}. {rec}")
    
    # Detailed breakdown table
    st.markdown("## 📋 Detailed Trip Breakdown")
    
    display_df = trips_df.copy()
    display_df['Vehicle'] = display_df['vehicle'].apply(lambda x: f"{VEHICLE_DATA[x]['icon']} {x}")
    display_df = display_df[['day', 'Vehicle', 'destination', 'distance', 'cost', 'emission', 'timestamp']]
    display_df.columns = ['Day', 'Vehicle', 'Destination', 'Distance (km)', 'Cost (₹)', 'CO₂ (kg)', 'Time Added']
    display_df = display_df.round(2)
    
    st.dataframe(display_df, use_container_width=True)
    
    # Export options
    st.markdown("## 📁 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Download as CSV", use_container_width=True):
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV File",
                data=csv,
                file_name=f"carbon_report_{st.session_state.user_info['name'].replace(' ', '_')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Generate Text Report", use_container_width=True):
            report_text = generate_text_report(st.session_state.user_info, total_emission, total_cost, 
                                             total_distance, max_emission, min_emission, avg_daily_emission,
                                             trees_needed)
            st.download_button(
                label="💾 Download Text Report",
                data=report_text,
                file_name=f"carbon_report_{st.session_state.user_info['name'].replace(' ', '_')}.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("🔄 Clear All Data", use_container_width=True):
            if st.checkbox("⚠️ I confirm I want to delete all data"):
                st.session_state.weekly_data = {day: [] for day in DAYS_OF_WEEK}
                st.success("✅ All data cleared!")
                st.rerun()

def generate_text_report(user_info, total_emission, total_cost, total_distance, 
                        max_emission, min_emission, avg_daily_emission, trees_needed):
    return f"""
🌱 CARBON EMISSION REPORT 🌱

Personal Information:
👤 Name: {user_info['name']}
🏙️ City: {user_info['city']}
📅 Report Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}

Weekly Summary:
📊 Total CO₂ Emission: {total_emission:.2f} kg
💰 Total Fuel Cost: ₹{total_cost:.2f}
🛣️ Total Distance: {total_distance:.1f} km

Daily Analysis:
📈 Highest Emission Day: {max_emission:.2f} kg CO₂
📉 Lowest Emission Day: {min_emission:.2f} kg CO₂
📊 Average Daily Emission: {avg_daily_emission:.2f} kg CO₂

Environmental Impact:
🌳 Trees needed to offset: {trees_needed} trees/year
⛽ Equivalent petrol burned: {total_emission/2.3:.1f} liters
🏠 Home power equivalent: {total_emission/10:.1f} days

Recommendations:
• Consider using public transport or cycling for short distances
• Combine multiple trips into one journey when possible
• Try carpooling or ride-sharing options
• Consider electric or hybrid vehicles for future purchases
• Plant trees to offset your carbon footprint
• Practice eco-driving techniques

Generated by Carbon Emission Tracker
"""

if __name__ == "__main__":
    main()