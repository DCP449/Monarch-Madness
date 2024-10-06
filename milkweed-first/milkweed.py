import pandas as pd
import plotly.express as px

def load_and_process_data(filename):
    df = pd.read_csv(filename)
    
    # Filter for US states only (excluding Canadian provinces)
    us_df = df[df['State/Province'].isin(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])]
    
    # Group by state and calculate total sightings, unique locations, and images
    state_data = us_df.groupby('State/Province').agg({
        'Town': 'nunique',
        'Image': 'sum'
    }).reset_index()
    
    state_data.columns = ['State', 'Unique Locations', 'Milkweed Sightings']
    
    return state_data

def create_map(state_data):
    fig = px.choropleth(state_data,
                        locations='State',
                        locationmode="USA-states",
                        color='Milkweed Sightings',
                        hover_name='State',
                        hover_data=['Milkweed Sightings', 'Unique Locations'],
                        color_continuous_scale='YlGn',
                        scope="usa",
                        labels={'Milkweed Sightings': 'Milkweed Sightings'},
                        title="Milkweed Sightings by State in 2023")

    # Add annotation for top 5 states with most sightings
    top_5_states = state_data.nlargest(5, 'Milkweed Sightings')
    top_5_text = "Top 5 States by Milkweed Sightings:<br>" + "<br>".join([
        f"{state}: {sightings} (in {locations} locations)"
        for state, sightings, locations in zip(top_5_states['State'], top_5_states['Milkweed Sightings'], top_5_states['Unique Locations'])
    ])

    fig.add_annotation(
        x=0.01,
        y=0.99,
        xref="paper",
        yref="paper",
        text=top_5_text,
        showarrow=False,
        font=dict(size=10),
        align="left",
        bgcolor="white",
        bordercolor="black",
        borderwidth=1,
        borderpad=4
    )

    fig.show()

def main():
    filename = "milkweed-first_2023.csv"
    state_data = load_and_process_data(filename)
    create_map(state_data)

if __name__ == "__main__":
    main()
