"""
Generic reusable components for the web app
"""

import dash_html_components as html
# import pandas as pd


def generate_table(dataframe, text_color, max_rows=10):
    """A generic table element

    Args:
        dataframe (pandas dataframe)
    Returns:
        A dash table element
    """

    return html.Table(
        # Header
        [html.Tr([html.Th(col, style={'color': text_color}) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col], style={'color': text_color}) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )
