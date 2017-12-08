"""
Dash app homepage for Action Potential Party web app
"""

import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash()
app.css.append_css({"external_url":
                    "https://codepen.io/chriddyp/pen/bWLwgP.css"})

team_members = ['Liza', 'Nikunj', 'Noosh', 'Utkarsh']

app.layout = html.Div(children=[
    html.H1(children='Pyramidal Action Party'),

    html.Div(children='''
        A multi-API information retrieval and NLP platform.
    '''),

    dcc.Graph(
        id='example-graph2',
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
                'title': 'Personnel Overview'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
