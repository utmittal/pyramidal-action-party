"""
Dash app homepage for Action Potential Party web app
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from app_components.table import generate_table


app = dash.Dash()
app.css.append_css({"external_url":
                    "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Data for CSS
background = '#111111'  # black
text = '#7FDBFF'        # a shade of blue

# Data for a table (of U.S. agriculture um....)
# US_agri = pd.read_csv(
#    'https://gist.githubusercontent.com/chriddyp/'
#    'c78bf172206ce24f77d6363a2d754b59/raw/'
#    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
#    'usa-agricultural-exports-2011.csv')

# my fake data
basket = pd.read_csv('data/test.csv')

# Demographic data: country, continent, population, life exp, GDP per capita
df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/' +
    'gdp-life-exp-2007.csv')

# Data for personnel graph
team_members = ['Liza', 'Nikunj', 'Noosh', 'Utkarsh']

# Text for a markdown section below
health_text = """
#
# Global Demographic information
### What we Care About
We care about people getting to live an equally long time

### Why we Care
According to the philosophical concept of the "veil of ignorance", WE could
have been born somewhere poor!
"""

# Main page layout
app.layout = html.Div(style={'backgroundColor': background}, children=[
    html.H1(
        children='Pyramidal Action Party',
        style={
            'textAlign': 'center',
            'color': text
        }),

    html.Div(children='A multi-API information retrieval and NLP platform.',
             style={
                'textAlign': 'center',
                'color': text,
                'fontSize': '24px'
             }),

    html.Div(style={'textAlign': 'center'}, children=[

        html.Label(children='Please enter your search query:', style={
            'color': text}),

        dcc.Input(value='cats', type='text')]
    ),

    dcc.Graph(
        id='personnel-graph',
        figure={
            'data': [
                {'x': team_members,
                 'y': [5, 2.5, 0.5, 1.5], 'type': 'bar', 'name': 'Hair'},
                {'x': team_members,
                 'y': [2, 5, 3, 2], 'type': 'bar', 'name': 'Zany-ness'},
                {'x': team_members,
                 'y': [0, 0, 5, 1.5], 'type': 'bar', 'name':
                     'Actually contributing to repo'}
            ],
            'layout': {
                'title': 'Personnel Overview',
                'plot_bgcolor': background,
                'paper_bgcolor': background,
                'font': {'color': text}
            }
        }
    ),

    html.H4('Basket Analysis', style={'color': text}),

    generate_table(basket),

    dcc.Markdown(health_text, containerProps={'style': {'color': text}}),

    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
