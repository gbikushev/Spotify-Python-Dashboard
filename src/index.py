# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
# import all pages in the app
from apps import US, IN, IE, home


# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("USA", href="/US"),
        dbc.DropdownMenuItem("India", href="/IN"),
        dbc.DropdownMenuItem("Ireland", href="/IE"),
        # dbc.DropdownMenuItem("Global", href="/task123"),
        # dbc.DropdownMenuItem("Europe", href="/Europe"),
    ],
    nav = True,
    in_navbar = True,
    label = "Choose country",
)
# format_datetime.strftime("%b %d %Y %H:%M:%S")
date_text = dbc.Row(
    [dbc.Col(html.Div(f"The data is relevant until {US.new_date.strftime('%B %d, %Y')}", style={'color': 'white'}))
    ],
    # Use class 'ml-auto' to float the text to the right
    className="ml-auto",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/spotify.png", height="50px"), width="auto"),
                        dbc.Col(dbc.NavbarBrand("Top Spotify Songs and Artists in different countries Dashboard", className="ml-2", style={'color': '#1ed760', 'fontWeight': 'bold'}), width=True),
                    ],
                    align="center",
                ),
                href="/home",
                className="flex-nowrap",
                style={'width': '100%'},
                # className="g-0"
                # no_gutters=True,
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # Assume 'dropdown' and 'date_text' are defined elsewhere as shown in previous examples
                    [dropdown, date_text], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="black",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/US':
        return US.layout
    elif pathname == '/IN':
        return IN.layout
    elif pathname == '/IE':
        return IE.layout
    else:
        return home.layout    
    # elif pathname == '/Europe':
    #     return Europe.layout
    # else:
    #     return home.layout

if __name__ == '__main__':
    app.run_server(port=8091,debug=True)