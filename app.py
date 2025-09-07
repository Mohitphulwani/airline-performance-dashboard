# app.py
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Load airline data
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding="ISO-8859-1",
    dtype={'Div1Airport': str, 'Div1TailNum': str, 'Div2Airport': str, 'Div2TailNum': str}
)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Airline Performance Dashboard"

# Layout
app.layout = html.Div([
    html.H1(
        "Airline Performance Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 40, 'margin-bottom': '30px'}
    ),

    html.Div([
        html.Label("Enter Year:", style={'fontSize': 24, 'margin-right': '10px'}),
        dcc.Input(id='input-year', type='number', value=2010, min=2005, max=2020, step=1,
                  style={'fontSize': 20, 'width': '150px'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'margin-bottom': '20px'}),

    dcc.Graph(id='line-plot')
])

# Callback
@app.callback(
    Output('line-plot', 'figure'),
    Input('input-year', 'value')
)
def update_line_chart(entered_year):
    # Filter data for the entered year
    df_year = airline_data[airline_data['Year'] == int(entered_year)]

    # Group by month and compute average arrival delay
    monthly_delay = df_year.groupby('Month')['ArrDelay'].mean().reset_index()

    # Create line chart
    fig = go.Figure(
        data=go.Scatter(
            x=monthly_delay['Month'],
            y=monthly_delay['ArrDelay'],
            mode='lines+markers',
            marker=dict(color='green')
        )
    )
    fig.update_layout(
        title=f"Average Monthly Flight Delay in {entered_year}",
        xaxis_title="Month",
        yaxis_title="Average Arrival Delay (minutes)",
        template='plotly_white'
    )
    return fig

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
