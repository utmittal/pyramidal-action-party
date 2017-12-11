"""
Random data files that could be used for visualisation purposes
"""
import pandas as pd

# Data for personnel graph
team_members = ['Liza', 'Nikunj', 'Noosh', 'Utkarsh']

# Fake data to have a table
basket = pd.read_csv('data/test.csv')

# Demographic data: country, continent, population, life exp, GDP per capita
demographics = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/' +
    'gdp-life-exp-2007.csv')

# Text for a markdown section below
health_text = """
#
## Global Demographic information
#### What we Care About
We care about people getting to live an equally long time

#### Why we Care
According to the philosophical concept of the "veil of ignorance", WE could
have been born somewhere poor!
"""

# A CSV table of U.S. agriculture data
US_agri = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')
