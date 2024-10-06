import plotly.express as px
import pandas as pd
import csv
from collections import defaultdict

def calculate_state_data(filename):
    state_data = defaultdict(lambda: {'concentrations': [], 'pesticides': set()})
    all_pesticides = defaultdict(int)
    pesticide_state_count = defaultdict(set)

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            state = row['Sample ID'][:2]
            try:
                concentration = float(row['Concentration'])
                pesticide = row['Pesticide Name']
                state_data[state]['concentrations'].append(concentration)
                state_data[state]['pesticides'].add(pesticide)
                all_pesticides[pesticide] += 1
                pesticide_state_count[pesticide].add(state)
            except ValueError:
                continue

    result = []
    for state, data in state_data.items():
        avg_concentration = sum(data['concentrations']) / len(data['concentrations']) if data['concentrations'] else 0
        top_3_pesticides = sorted(data['pesticides'], key=lambda x: all_pesticides[x], reverse=True)[:3]
        top_3_pesticides = ', '.join(top_3_pesticides)
        result.append({
            'State': state,
            'Average Concentration': avg_concentration,
            'Top 3 Pesticides': top_3_pesticides
        })

    top_5_overall = sorted(all_pesticides.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5_overall = '<br>'.join([f"{p[0]}: {all_pesticides[p[0]]} (Used in {len(pesticide_state_count[p[0]])} states)" for p in top_5_overall])

    return result, top_5_overall

def create_map(state_data, top_5_overall):
    df = pd.DataFrame(state_data)

    fig = px.choropleth(df, 
                        locations='State',
                        locationmode="USA-states",
                        color='Average Concentration',
                        hover_name='State',
                        hover_data={'Average Concentration': ':.2f', 'Top 3 Pesticides': True},
                        scope="usa",
                        color_continuous_scale='Blues',
                        labels={'Average Concentration': 'Avg Pesticide Concentration'},
                        title="Average Pesticide Concentration by State")

    fig.add_annotation(
        x=0.000000001,
        y=0.99,
        xref="paper",
        yref="paper",
        text=f"Top 5 Pesticides Overall:<br>{top_5_overall}",
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
    csv_filename = "USDA_PDP_AnalyticalResults.csv"
    state_data, top_5_overall = calculate_state_data(csv_filename)
    create_map(state_data, top_5_overall)

if __name__ == "__main__":
    main()
