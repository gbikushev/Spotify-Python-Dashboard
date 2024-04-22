import dash
from dash import html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from app import app

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H1("Welcome to the Top Spotify Songs and Artists Dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='The dashboard was created to compare the top songs and artists in different countries to identify cultural music preferences. Each page of the dashboard represents one country.'
            ), className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children=[
                'The dashboard consists of 4 main pages:',
                html.Ul([
                    html.Li('Home: The home page of the dashboard with a brief description.'),
                    html.Li('US: Represents the most popular songs and artists in United States, according to Spotify data.'),
                    html.Li('IN: Represents the most popular songs and artists in India, according to Spotify data.'),
                    html.Li('IE: Represents the most popular songs and artists in Ireland, according to Spotify data.'),
                ]),
                'The main key performance indicator (KPI) for each page (each country) is the top-1 Spotify song of the current date.'
            ]), className="mb-5")
        ]),
        dbc.Row([
            # 2 columns of width 6 with a border
            dbc.Col(dbc.Card(children=[html.H3(children='Go to the Kaggle to get the original dataset',
                                               className="text-center",
                                               style={'color': '#1ed760','fontWeight': 'bold'}),
                                       dbc.Button("Kaggle",
                                                  href="https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated/data",
                                                  color="primary",
                                                  className="mt-3",),
                                       ],
                             body=True, color="#262626", outline=True)
                    , width=6, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                               className="text-center",
                                               style={'color': '#1ed760','fontWeight': 'bold'}),
                                       dbc.Button("GitHub",
                                                  href="https://github.com/gbikushev/Spotify-Python-Dashboard",
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color='#262626', outline=True)
                    , width=6, className="mb-4"),

        ], className="mb-5"),

    ])

])

# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8098,debug=True)