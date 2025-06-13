import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Create Dash app instance
app = dash.Dash(__name__)

# Suppress callback exceptions for dynamic callbacks
app.config.suppress_callback_exceptions = True

# Load wildfire data into pandas dataframe
df = pd.read_csv("../data/australia_wildfire.csv")

# Extract month name and year from Date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Define layout of the Dash app
app.layout = html.Div(children=[
    # Dashboard title
    html.H1(
        'Australia Wildfire Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}
    ),

    # Outer div container for inputs and outputs
    html.Div([
        # Region selection radio buttons
        html.Div([
            html.H2('Select Region:', style={'margin-right': '2em'}),
            dcc.RadioItems(
                options=[
                    {"label": "New South Wales", "value": "NSW"},
                    {"label": "Northern Territory", "value": "NT"},
                    {"label": "Queensland", "value": "QL"},
                    {"label": "South Australia", "value": "SA"},
                    {"label": "Tasmania", "value": "TA"},
                    {"label": "Victoria", "value": "VI"},
                    {"label": "Western Australia", "value": "WA"},
                ],
                value="NSW",
                id='region',
                inline=True
            ),
        ]),

        # Year selection dropdown
        html.Div([
            html.H2('Select Year:', style={'margin-right': '2em'}),
            dcc.Dropdown(
                options=[{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
                value=2005,
                id='year'
            )
        ]),

        # Divisions for output plots
        html.Div([
            html.Div(id='plot1'),
            html.Div(id='plot2')
        ], style={'display': 'flex'}),
    ]),
])

# Define callback with inputs and outputs
@app.callback(
    [Output('plot1', 'children'),
     Output('plot2', 'children')],
    [Input('region', 'value'),
     Input('year', 'value')]
)
def reg_year_display(input_region, input_year):
    # Filter data based on region and year selections
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]

    # Prepare pie chart data: Monthly average estimated fire area
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(
        est_data,
        values='Estimated_fire_area',
        names='Month',
        title=f"{input_region} : Monthly Average Estimated Fire Area in year {input_year}"
    )

    # Prepare bar chart data: Monthly average count of vegetation fires
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(
        veg_data,
        x='Month',
        y='Count',
        title=f"{input_region} : Average Count of Pixels for Presumed Vegetation Fires in year {input_year}"
    )

    # Return two graphs as Dash Core Components
    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]


# Run the Dash app
if __name__ == '__main__':
    app.run()