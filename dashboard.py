import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# 添加自定义CSS样式
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Macroeconomic Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Helvetica Neue', Arial, sans-serif;
                background-color: #121212;
                color: #e0e0e0;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #1e1e1e;
                box-shadow: 0 0 10px rgba(255,255,255,0.1);
            }
            h1, h3 {
                color: #bb86fc;
            }
            .parameter-input {
                margin-bottom: 10px;
            }
            .parameter-input label {
                display: inline-block;
                width: 200px;
                color: #03dac6;
            }
            .parameter-input input {
                width: 100px;
                background-color: #2c2c2c;
                border: 1px solid #03dac6;
                color: #e0e0e0;
                padding: 5px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

initial_params = {
    'GDP': {'A': 10, 'g': 0.03},
    'Inflation': {'π_target': 2, 'α': 0.5},
    'Unemployment': {'u_natural': 4, 'β': -0.5}
}

def calculate_gdp(years, A, g):
    return A * (1 + g) ** years

def calculate_inflation(years, π_target, α):
    return π_target + α * np.sin(years / 2)

def calculate_unemployment(years, u_natural, β):
    return u_natural + β * np.cos(years / 3)

app.layout = html.Div([
    html.Div([
        html.H1('Macroeconomic Theory Dashboard', style={'textAlign': 'center'}),
        
        html.Div([
            html.Div([
                html.H3('GDP Parameters'),
                html.Div([
                    html.P('GDP = A * (1 + g)^t', style={'fontWeight': 'bold', 'color': '#03dac6'}),
                    html.Div([
                        html.Label('A (Initial GDP)'),
                        dcc.Input(id='gdp-A', type='number', value=initial_params['GDP']['A'], step=0.1)
                    ], className='parameter-input'),
                    html.Div([
                        html.Label('g (Growth rate)'),
                        dcc.Input(id='gdp-g', type='number', value=initial_params['GDP']['g'], step=0.01)
                    ], className='parameter-input')
                ])
            ], style={'width': '33%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            html.Div([
                html.H3('Inflation Parameters'),
                html.Div([
                    html.P('π = π_target + α * sin(t/2)', style={'fontWeight': 'bold', 'color': '#03dac6'}),
                    html.Div([
                        html.Label('π_target (Target inflation rate)'),
                        dcc.Input(id='inf-target', type='number', value=initial_params['Inflation']['π_target'], step=0.1)
                    ], className='parameter-input'),
                    html.Div([
                        html.Label('α (Cyclical factor)'),
                        dcc.Input(id='inf-alpha', type='number', value=initial_params['Inflation']['α'], step=0.1)
                    ], className='parameter-input')
                ])
            ], style={'width': '33%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            html.Div([
                html.H3('Unemployment Parameters'),
                html.Div([
                    html.P('u = u_natural + β * cos(t/3)', style={'fontWeight': 'bold', 'color': '#03dac6'}),
                    html.Div([
                        html.Label('u_natural (Natural unemployment rate)'),
                        dcc.Input(id='unemp-natural', type='number', value=initial_params['Unemployment']['u_natural'], step=0.1)
                    ], className='parameter-input'),
                    html.Div([
                        html.Label('β (Cyclical factor)'),
                        dcc.Input(id='unemp-beta', type='number', value=initial_params['Unemployment']['β'], step=0.1)
                    ], className='parameter-input')
                ])
            ], style={'width': '33%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),
        
        dcc.Graph(id='macro-trends-graph'),
        
        html.Div([
            html.H3('Macroeconomic Theory Explanations'),
            html.P('GDP (Gross Domestic Product) measures the total economic output. '
                   'It is modeled as exponential growth where A is the initial GDP and g is the growth rate.'),
            html.P('Inflation represents the rate of price level increase. '
                   'This model assumes inflation fluctuates around a target rate with some cyclical behavior.'),
            html.P('Unemployment rate is the percentage of the labor force that is jobless. '
                   'This model represents unemployment as fluctuating around a natural rate.')
        ], style={'marginTop': '20px'})
    ], className='container')
])

@app.callback(
    Output('macro-trends-graph', 'figure'),
    [Input('gdp-A', 'value'),
     Input('gdp-g', 'value'),
     Input('inf-target', 'value'),
     Input('inf-alpha', 'value'),
     Input('unemp-natural', 'value'),
     Input('unemp-beta', 'value')]
)
def update_graph(gdp_A, gdp_g, inf_target, inf_alpha, unemp_natural, unemp_beta):
    years = np.arange(0, 11)
    
    gdp = calculate_gdp(years, gdp_A, gdp_g)
    inflation = calculate_inflation(years, inf_target, inf_alpha)
    unemployment = calculate_unemployment(years, unemp_natural, unemp_beta)
    
    fig = make_subplots(rows=1, cols=3, shared_yaxes=False, horizontal_spacing=0.05,
                        subplot_titles=('GDP', 'Inflation', 'Unemployment'))
    
    fig.add_trace(go.Scatter(x=years+2010, y=gdp, mode='lines+markers', name='GDP', line=dict(color='#bb86fc')), row=1, col=1)
    fig.add_trace(go.Scatter(x=years+2010, y=inflation, mode='lines+markers', name='Inflation', line=dict(color='#03dac6')), row=1, col=2)
    fig.add_trace(go.Scatter(x=years+2010, y=unemployment, mode='lines+markers', name='Unemployment', line=dict(color='#cf6679')), row=1, col=3)
    
    fig.update_layout(
        height=500,
        title_text='Macroeconomic Trends',
        paper_bgcolor='#1e1e1e',
        plot_bgcolor='#1e1e1e',
        font=dict(color='#e0e0e0'),
        showlegend=False
    )
    
    fig.update_xaxes(title_text='Year', gridcolor='#5e5e5e', zerolinecolor='#5e5e5e')
    fig.update_yaxes(gridcolor='#5e5e5e', zerolinecolor='#5e5e5e')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)