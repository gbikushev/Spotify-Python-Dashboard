
import numpy as np
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import datetime
import dash_bootstrap_components as dbc

from app import app

# Incorporate data
df = pd.read_csv('US.csv', parse_dates=['snapshot_date'])

# find the last date
new_date = df['snapshot_date'].max()
old_date = df['snapshot_date'].min()
days = (new_date - old_date).days

df_latest_date = df[df['snapshot_date'] == new_date]

top_artists = df.groupby('artists')[['popularity']].sum().sort_values(by='popularity', ascending=False)
top20_artists = top_artists.head(20)


# Initialize the Dash app (usually in a main block)
# app = dash.Dash(__name__)

# Define the layout of the app
layout = html.Div([
    
    dbc.Container([
        dbc.Row(
        [
            dbc.Col(html.Img(src="/assets/ie.png", height="50px"), width="auto"),
            dbc.Col(html.H5([
                "KPI: The most popular song for current date is ",
                html.Span(df_latest_date.loc[0, 'name'], style={'font-weight': 'bold'}),
                " by ",
                html.Span(df_latest_date.loc[0, 'artists'], style={'font-weight': 'bold'}),
                " for country Ireland"
            ]
            ))
        ], align="center"
        )
    ]),
    
    html.Hr(style={'border-top': '3px solid #000000'}),

    html.H4(f"Information for the current date ({new_date.strftime('%d-%m-%Y')})",
        style={
            'textAlign': 'left',
            # 'width':'70%'
            'padding': '20px'
            # 'color': colors['text']
        }
    ),

    html.Div([
        html.Label('The songs contain explicit content'), 
        dcc.RadioItems(
            id='ie_explicit-selector',
            options=[
                {'label': 'True', 'value': True},
                {'label': 'False', 'value': False}
            ],
            value=False,  # Default value
            style={'width':'70%'},
            labelStyle={'display': 'inline-block'}
        )
    ],  style={'padding': '20px'}),
        
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='ie_popular_songs'
            )
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '20px'}),
        html.Div([
            dcc.Graph(
                id='ie_popular_artists'
            )            
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block', 'padding': '20px'}),
    ]),

    html.Hr(style={'border-top': '3px solid #000000'}),

    html.H4(f"Information for overall time (from {old_date.strftime('%d-%m-%Y')} till {new_date.strftime('%d-%m-%Y')})",
        style={
            'textAlign': 'left',
            # 'width':'70%'
            'padding': '20px'
            # 'color': colors['text']
        }
    ),

    html.Div([
        html.Div([
            html.Label('Choose the timeline'),
            dcc.RangeSlider(id='ie_range_slider', min=0, max=days,
                            marks={i: {'label': (old_date + datetime.timedelta(days=i)).strftime("%m/%d/%Y")} for i in range(0, days, 40)},
                            value=[0, days],
                            className='custom-slider'
            )
        ],style={'width': '49%', 'display': 'inline-block', 'padding': '20px'}),
        html.Div([
            html.Label('Choose an artist from the top 20 most popular'),
            dcc.Dropdown(id='ie_artists_dropdown',
                        options=[{'label': i, 'value': i}
                                for i in top20_artists.index],
                        value=top20_artists.index[0],
                        multi=False
            )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block', 'padding': '20px'}),
    ]),


    html.Div([
        html.Div([
            dcc.Graph(
                id='ie_popularity_changing',
            )
        ], style={'width': '95%', 'display': 'inline-block', 'padding': '20px'}),
    ])

])



# Define callback to update graph
@app.callback(
    [Output('ie_popular_songs', 'figure'),
     Output('ie_popular_artists', 'figure')] ,
    Input('ie_explicit-selector', 'value')
)
def update_graph(is_explicit):
    filtered_data = df_latest_date[df_latest_date['is_explicit'] == is_explicit]
    top_songs = filtered_data.sort_values(by='daily_rank').head(5)

    # top_songs['Top Label'] = top_songs['daily_rank'].apply(lambda x: f"Top-{x}")
    top_songs['Top Label'] = ['Top-1', 'Top-2', 'Top-3', 'Top-4', 'Top-5']
    # top_songs['inverse_rank'] = 11 - top_songs['daily_rank']
    top_songs['inverse_rank'] = [5, 4, 3, 2, 1]

    songs_fig = px.bar(
        top_songs, 
        x='inverse_rank',
        y='Top Label', 
        text='name',
        color='daily_rank',  # Use 'daily_rank' for the color
        color_continuous_scale='Greens_r',
        range_color=[1, 10],  # Assuming the 'daily_rank' goes from 1 to 10
        orientation='h',
        hover_data={'name': True, 'artists': True, 'daily_rank': True, 'Top Label': True, 'inverse_rank':False},
        labels={'Top Label': 'Top Label', 'name': 'Song name', 'artists': 'Artist', 'daily_rank': 'Daily rank'}                           
    )


    # Update the layout
    songs_fig.update_layout(
        title='Top 5 Popular Songs Based on Daily Rank (Filtered by Explicit Content)',
        xaxis=dict(title='Song Popularity', showgrid=False, visible=False),  # Hide the x-axis details
        yaxis=dict(title='Popularity Rank', autorange="reversed", categoryorder='total ascending'),
        showlegend=False,
        # plot_bgcolor='white'
    )

    songs_fig.update_layout(
        coloraxis_colorbar=dict(
            title='Daily Rank',
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            ticktext=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        )   
    )

    top_artists = pd.DataFrame(filtered_data.groupby('artists')['popularity'].sum().sort_values(ascending=False)).head(5)
    top_artists.reset_index(inplace=True)
    top_artists.columns = ['name', 'popularity']
    top_artists['Top Label'] = ['Top-1', 'Top-2', 'Top-3', 'Top-4', 'Top-5']
    top_artists['inverse_rank'] = [5, 4, 3, 2, 1]

    top_artists['log_popularity'] = round(np.log(top_artists['popularity']), 2)
    # top_artists['log_popularity'] = round(top_artists['log_popularity'], 2)

    # print(filtered_data)
    artists_fig = px.bar(
        top_artists, 
        x='inverse_rank', 
        y='Top Label', 
        text='name',
        color='log_popularity',  # Use 'daily_rank' for the color
        color_continuous_scale='Greens',
        # range_color=[1, 10],  # Assuming the 'daily_rank' goes from 1 to 10
        orientation='h',
        hover_data={'popularity': True, 'name': True, 'Top Label': True, 'log_popularity':True, 'inverse_rank':False},
        labels={'Top Label': 'Top Label', 'name': 'Artist', 'popularity': 'Popularity', 'log_popularity': 'Log(Popularity)'}  )
    
    # Update the layout
    artists_fig.update_layout(
        title='Top 5 Popular Artists Based on Popularity (Filtered by Explicit Content)',
        xaxis=dict(title='Song Popularity', showgrid=False, visible=False),  # Hide the x-axis details
        yaxis=dict(title='Popularity Rank', autorange="reversed", categoryorder='total ascending'),
        showlegend=False,
        # plot_bgcolor='white'
    )

    artists_fig.update_layout(
        coloraxis_colorbar=dict(
            title='Log(Popularity)'
            # tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            # ticktext=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        )   
    )


    return [songs_fig, artists_fig]



# Define callback to update graph
@app.callback(
    Output('ie_popularity_changing', 'figure'),
    [Input('ie_range_slider', 'value'),
     Input('ie_artists_dropdown', 'value')]    
)
def graph2(date, artist):
    date_start = old_date + datetime.timedelta(days=date[0])
    date_end = old_date + datetime.timedelta(days=date[1])
    filtered_data = df[(df['snapshot_date'] >= date_start) & (df['snapshot_date'] <= date_end) & (df['artists'] == artist)]
    
    artist_popularity = filtered_data.groupby(['artists', 'snapshot_date'])['popularity'].sum().reset_index()

    # Create the line graph
    fig = px.line(artist_popularity, 
                x='snapshot_date', 
                y='popularity', 
                color='artists',
                # color_continuous_scale='Greens_r',
                labels={'popularity': 'Total Popularity', 'snapshot_date': 'Date'},
                title='Artists Popularity Over Time')
    fig.update_traces(line=dict(color='#1ed760'))     
    return fig    


# Run the app
# if __name__ == '__main__':
#     app.run_server(port=8091, debug=True)

