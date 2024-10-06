import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
import ssl
import certifi

# Create a custom SSL context
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def load_and_process_data(state_code):
    df = pd.read_csv("monarch-larva-first_2024.csv")
    
    # Filter for the specified state data
    state_df = df[df['State/Province'] == state_code]
    
    return state_df

def get_state_counties(state_fips):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json', context=ssl_context) as response:
        counties = json.load(response)
    
    # Filter for the specified state counties
    state_counties = [county for county in counties['features'] if county['properties']['STATE'] == state_fips]
    
    return {'type': 'FeatureCollection', 'features': state_counties}

def create_map(state_data, state_counties, state_name):
    fig = go.Figure()

    # Add state counties
    fig.add_choroplethmapbox(
        geojson=state_counties,
        locations=[county['properties']['GEO_ID'][9:] for county in state_counties['features']],
        z=[0] * len(state_counties['features']),  # Placeholder values
        colorscale="Greens",
        marker_opacity=0.5,
        marker_line_width=0,
        showscale=False
    )

    # Create a color scale
    max_butterflies = state_data['Number'].max()
    colorscale = px.colors.sequential.Viridis

    # Add butterfly sightings as scatter points
    fig.add_scattermapbox(
        lat=state_data['Latitude'],
        lon=state_data['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color=state_data['Number'],
            colorscale=colorscale,
            cmin=0,
            cmax=max_butterflies,
            colorbar=dict(
                title="Number of Butterflies",
                thickness=15,
                len=0.5,
                x=0.95
            ),
            opacity=0.7
        ),
        text=state_data.apply(lambda row: f"Town: {row['Town']}<br>Number: {row['Number']}<br>Date: {row['Date']}", axis=1),
        hoverinfo='text'
    )

    # Set the map center to the mean of latitudes and longitudes
    center_lat = state_data['Latitude'].mean()
    center_lon = state_data['Longitude'].mean()

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=6,
        mapbox_center={"lat": center_lat, "lon": center_lon},
        title=f"Monarch Butterfly Sightings in {state_name}",
        height=800,
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )

    fig.show()

def main():
    # Dictionary of state codes and their FIPS codes
    state_fips = {
        'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06', 'CO': '08', 'CT': '09',
        'DE': '10', 'FL': '12', 'GA': '13', 'HI': '15', 'ID': '16', 'IL': '17', 'IN': '18',
        'IA': '19', 'KS': '20', 'KY': '21', 'LA': '22', 'ME': '23', 'MD': '24', 'MA': '25',
        'MI': '26', 'MN': '27', 'MS': '28', 'MO': '29', 'MT': '30', 'NE': '31', 'NV': '32',
        'NH': '33', 'NJ': '34', 'NM': '35', 'NY': '36', 'NC': '37', 'ND': '38', 'OH': '39',
        'OK': '40', 'OR': '41', 'PA': '42', 'RI': '44', 'SC': '45', 'SD': '46', 'TN': '47',
        'TX': '48', 'UT': '49', 'VT': '50', 'VA': '51', 'WA': '53', 'WV': '54', 'WI': '55',
        'WY': '56'
    }
    
    # Dictionary of state names
    state_names = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
        'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
        'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
        'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire',
        'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina',
        'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
        'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
        'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
        'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    
    # Get user input for state
    state_code = input("Enter the two-letter state code (e.g., CA for California): ").upper()
    
    if state_code not in state_fips:
        print("Invalid state code. Please enter a valid two-letter state code.")
        return
    
    state_data = load_and_process_data(state_code)
    state_counties = get_state_counties(state_fips[state_code])
    create_map(state_data, state_counties, state_names[state_code])

if __name__ == "__main__":
    main()
