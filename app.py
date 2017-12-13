"""
Dash app homepage for Action Potential Party web app
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from html import unescape
from dash.dependencies import Input, Output, State, Event

# Reusable elements
from app_components.table import generate_table
# Data sources
from data.data_sources import team_members, basket, health_text, demographics

# Search functionality
from twitter_search import search_tweets
import json
import bz2


# Initialise the app
app = dash.Dash()

# Default CSS settings so that text doesn't look awful
app.css.append_css({"external_url":
                    "https://codepen.io/chriddyp/pen/bWLwgP.css"})
# Background and text CSS (feel free to change)
background = '#ffffff'  # light green
text = '#2B521A'        # dark text


# Main page layout
app.layout = html.Div(style={'backgroundColor': background}, children=[
    # Title and heading
    html.H1(
        children='Pyramidal Action Party!',
        style={
            'textAlign': 'center',
            'color': text
        }),

    html.Div(children='A multi-API information retrieval and NLP platform.'
             '\nBrewed with love.',
             style={
                 'textAlign': 'center',
                 'color': text,
                 'fontSize': '24px'
             }),

    # Input for search query and APIs to include
    html.Div(style={'textAlign': 'center'}, children=[

        html.Label(children='Please enter your search query:', style={
            'color': text}),

        dcc.Input(
            value='',
            id='query-input',
            type='text',
            placeholder='E.g. cats'),

        html.Button(
            'Do it!',
            id='submit-button',
            type='submit',
            style={'color': text}),

        html.Label('APIs to include:', style={'color': text}),
        dcc.Checklist(
            options=[
                {'label': 'Twitter', 'value': 'twitter'},
                {'label': 'LinkedIn', 'value': 'linkedin'},
                {'label': 'Google', 'value': 'google'}
            ],
            values=['twitter'],
            labelStyle={'display': 'inline-block'},
            style={'color': text}
        )
    ]),

    html.H3(
        'Results:',
        id='results-header',
        style={'color': text, 'fontSize': '24px', 'textAlign': 'center'}),

    html.Div(
        id='results-div'),

    # Graph of personnel traits
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

    # Demo of a table
    html.H4('Basket Analysis', style={'color': text}),
    generate_table(basket, '#2B521A'),

    # Demo of how Markdown can be used
    dcc.Markdown(health_text, containerProps={'style': {'color': text}}),

    # Demo of a fancy scatter plot
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=demographics[demographics['continent'] == i]['gdp per capita'],
                    y=demographics[demographics['continent'] == i]['life expectancy'],
                    text=demographics[demographics['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in demographics.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                plot_bgcolor=background,
                paper_bgcolor=background
            )
        }
    )
])


### Callbacks ###

@app.callback(
    Output('results-header', 'children'),
    [],
    [State('query-input', 'value')],
    [Event('submit-button', 'click')]
)
def update_header(state):
    """Update heading"""
    return 'Results for \'{}\':'.format(state)


@app.callback(
    Output('results-div', 'children'),
    [],
    [State('query-input', 'value')],
    [Event('submit-button', 'click')]
)
def query_APIs(state):
    """Submit query to APIs"""
    print('Current state: {}'.format(state))
    if state:
        results = []
        search_tweets(state, **{'file': 'temp', 'lang': 'en'})
        tweet_file = bz2.BZ2File('./tweets/temp.txt.bz2', mode='r')
        for i in range(1, 7):
            tweet = json.loads(tweet_file.readline(), encoding='utf-8')
            # html.escape() turns e.g. &amp; => &
            results.append(str(i) + '. ' + unescape(tweet['text']))
            results.append(html.Br())
        tweet_file.close()
        return results

    return 'Try entering a search query :-)'


# Start the app
if __name__ == '__main__':
    app.run_server(debug=True)
