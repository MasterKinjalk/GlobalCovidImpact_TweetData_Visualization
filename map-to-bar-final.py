import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import json
from dash import callback_context

app = dash.Dash(__name__)


fname = 'Covid-19 Twitter Dataset (Apr-Jun 2020) clean.csv'


with open("world-countries.json", 'r') as file:
    worldCountries = json.load(file)

file_options = [
    {'label': 'Dataset 1 - April-June 2020', 'value': 'Covid-19 Twitter Dataset (Apr-Jun 2020) clean.csv'},
    {'label': 'Dataset 2 - August-September 2020', 'value': 'Covid-19 Twitter Dataset (Aug-Sep 2020) clean.csv'},
    {'label': 'Dataset 3 - April-June 2021', 'value': 'Covid-19 Twitter Dataset (Apr-Jun 2021) clean.csv'}
]

app.layout = html.Div([
   html.Div([
        html.H1('Visualizing Covid-19 Through Tweets', id='page-title', style={'color': '#89a2cc', 'font-size': '50px'})
    ],
    style={'display': 'flex', 'justify-content': 'center'}),
    html.Div([html.Hr(style={'border-top': '1px solid #ccc', 'margin': '20px 0px', 'background-color': '#1d3a69', 'height': '40px', 'width': '100%'}),
            #   html.Hr(style={'height':'20px'}),
              ]
    
    ),
    html.Div([
         
        html.Button('Show Sentiment Map', id='choropleth-button', n_clicks=0, style={'background-color': '#d8e1f0', 'color': 'black', 'font-size': '20px'}),
        html.Button('Show Word Search Map', id='word-search-button', n_clicks=0, style={'background-color': '#d8e1f0', 'color': 'black', 'font-size': '20px'})
    ],
    style={'display': 'flex', 'justify-content': 'center'}
    ),
    dcc.RadioItems(
        id='file-selector',
        options=file_options,
        value='Covid-19 Twitter Dataset (Apr-Jun 2020) clean.csv',  
        labelStyle={'display': 'block', 'margin-right': '20px', 'font-size': '20px'},
        inputStyle={"margin-right": "10px", "cursor": "pointer"} 
    ),
    
    html.Div(id='output-container', children=[
        html.Div(id='choropleth-container', style={'display': 'none'}, children=[
            html.Div([dcc.Input(id='country-input1', type='text', placeholder='Enter desired country...', style={'font-size': '20px'}),
            html.Button('Search country', id='country-button1', n_clicks=0, style={'background-color': '#445570', 'color': 'white','font-size': '15px'})
            ], style={'display': 'flex', 'justify-content': 'center'}),
            html.H2('Average Sentiment by Country', id='sentiment-title', style={'color': '#2d4875', 'font-size': '30px','display': 'flex', 'justify-content': 'center'}),
            dcc.Graph(id='country-map', config={'staticPlot': False}),
            html.Hr(style={'border': 'none', 'margin': '20px 0px', 'height': '40px'}),
            dcc.Graph(id='sentiment-bar', style={'width': '1200px', 'height': '500px','margin': 'auto', 'border': '3px solid #ccc'},config={'staticPlot': False})
        ]),
        html.Div(id='word-search-container', style={'display': 'none'}, children=[
            html.Div([dcc.Input(id='search-input', type='text', placeholder='Enter search query...',  style={'font-size': '20px'}),
            html.Button('Search tweet text', id='search-button', n_clicks=0, style={'background-color': '#445570', 'color': 'white','font-size': '15px'}),
            dcc.Input(id='country-input', type='text', placeholder='Enter desired country...', style={'font-size': '20px'}),
            html.Button('Search country', id='country-button', n_clicks=0, style={'background-color': '#445570', 'color': 'white','font-size': '15px'})]
            ,style={'display': 'flex', 'justify-content': 'center'}),
            html.H2('Average Word Density', id='word-density-title', style={'color': '#2d4875', 'font-size': '30px', 'display': 'flex', 'justify-content': 'center'}),
            dcc.Graph(id='word-search-map',  style={'width': '1200px', 'height': '500px', 'margin': 'auto'}, config={'staticPlot': False})  # Changed ID here
        ])
    ])

    
])

@app.callback(
    Output('choropleth-container', 'style'),
    Output('word-search-container', 'style'),
    Input('choropleth-button', 'n_clicks'),
    Input('word-search-button', 'n_clicks')
)
def toggle_graphs(choropleth_clicks, word_search_clicks):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'choropleth-button':
        return {'display': 'block'}, {'display': 'none'}
    elif button_id == 'word-search-button':
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}

# @app.callback(
#     Output('country-map', 'figure'),
#     [Input('file-selector', 'value')]
# )
# # def update_map(selected_file):

# #     df = pd.read_csv(selected_file)
# #     return generate_choropleth(df)
 
# def update_map(selected_file, choropleth_clicks):
#     if choropleth_clicks:
#         df = pd.read_csv(selected_file)
#         return generate_choropleth(df)
#     else:
#         raise dash.exceptions.PreventUpdate




def generate_choropleth(df):
    df_2020 = df
    avg_sentiment_by_country = df_2020.groupby("place_clean")["compound"].mean()

    trace = go.Choropleth(
        locations=avg_sentiment_by_country.index,  # Country names
        z=avg_sentiment_by_country.values,  # Sentiment scores
        locationmode='country names',
        showscale=True,
        geojson=worldCountries,
        featureidkey="properties.name",
        marker_line_color='white',
        marker_line_width=2,
        colorscale="RdYlGn",
        reversescale=False,
        text=avg_sentiment_by_country.index,  # Add country names to hover text
        hoverinfo="location+z+text",  
        colorbar=dict(len=0.75),
    )

    fig = go.Figure(trace)
    fig.update_geos(projection_type="natural earth")
    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            showframe=False, 
            showcoastlines=True, 
            showocean=True,  # Add this line to show oceans
            oceancolor="LightBlue"  # You can choose any color you like
        ),
        coloraxis_colorbar=dict(
            title='Average\nSentiment',  # Add a title to the color scale
            thicknessmode="pixels", thickness=15,
            lenmode="fraction", len=0.75,
            bgcolor='rgba(255,255,255,0.6)',
            tickvals=[-1, 0, 1],
            ticktext=["Negative", "Neutral", "Positive"],
            outlinewidth=1,
            outlinecolor='black',
            yanchor='middle',
            y=0.5
        )
    )

    return fig

@app.callback(
    Output('country-map', 'figure'),
    [Input('file-selector', 'value'), Input('country-button1', 'n_clicks')],
    [State('country-input1', 'value')]
)
def update_choropleth_map(selected_file, n_clicks, country_query):
    # Check if the callback was triggered by a country search
    if n_clicks > 0 and country_query:
        df = pd.read_csv(selected_file)
        fig = generate_choropleth(df)
        fig = zoom_country(fig, country_query, 'countries.csv')
        return fig
    # Fallback to updating the map based on file selection alone
    elif n_clicks == 0 or not country_query:
        df = pd.read_csv(selected_file)
        return generate_choropleth(df)
    else:
        raise dash.exceptions.PreventUpdate
# @app.callback(
#     Output('country-map', 'figure'),
#     [Input('country-button1', 'n_clicks')],
#     [State('country-input1', 'value'),
#      State('file-selector', 'value')],
#     prevent_initial_call=True
# )
# def update_map_country_button1(n_clicks, country_query, selected_file):
#     if n_clicks:
#         df = pd.read_csv(selected_file)
#         fig = generate_choropleth(df)
#         fig = zoom_country(fig, country_query, 'countries.csv') 
#         return fig
#     else:
#         raise dash.exceptions.PreventUpdate

@app.callback(
    Output('sentiment-bar', 'figure'),
    [Input('country-map', 'clickData'), Input('file-selector', 'value')],
    prevent_initial_call=True
)
def update_sentiment_bar(clickData, selected_file):
    if clickData is None:
        raise dash.exceptions.PreventUpdate
    
    df = pd.read_csv(selected_file)
    return display_country_sentiment(clickData, df)  
def display_country_sentiment(clickData,df):
    
    country_name = clickData['points'][0]['location']
    df_country = df[df['place_clean'] == country_name]
    
    # Calculate the total count for normalization
    total_count = df_country[['pos', 'neg', 'neu']].sum().sum()
    
    # Calculate the percentage for positive, negative and neutral sentiments
    pos_percentage = (df_country['pos'].sum() / total_count) * 100
    neg_percentage = (df_country['neg'].sum() / total_count) * 100
    neu_percentage = (df_country['neu'].sum() / total_count) * 100
    
    # Format the percentage text to display on the bars
    pos_text = f"{pos_percentage:.2f}%"
    neg_text = f"{neg_percentage:.2f}%"
    neu_text = f"{neu_percentage:.2f}%"
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Positive'], y=[df_country['pos'].sum()], name='Positive', marker_color='rgba(0,255,0,0.6)',
        text=pos_text, textposition='inside', hovertext='Positive Sentiment'
    ))
    fig.add_trace(go.Bar(
        x=['Negative'], y=[df_country['neg'].sum()], name='Negative', marker_color='rgba(255,0,0,0.6)',
        text=neg_text, textposition='inside', hovertext='Negative Sentiment'
    ))
    fig.add_trace(go.Bar(
        x=['Neutral'], y=[df_country['neu'].sum()], name='Neutral', marker_color='rgba(128,128,128,0.6)',
        text=neu_text, textposition='inside', hovertext='Neutral Sentiment'
    ))

    fig.update_layout(
        title=f"Positive vs Negative Sentiment Distribution for Tweets from {country_name}",
        xaxis_title="Sentiment",
        yaxis_title="Count",
        barmode='group',
        legend_title="Sentiment Type",
        xaxis={'categoryorder':'array', 'categoryarray':['Positive', 'Negative', 'Neutral']},
        plot_bgcolor='white', 
    )

    return fig

###############################################################################################################################

# Function to count occurrences of a word in a text
# Function to count occurrences of a word in a text
def count_word_occurrences(text, word):
  return 1 if (word.lower() in text.lower()) else 0

def plot_word_search(fname, search_word):
    df = pd.read_csv(fname)
    
    df['word_count'] = df['original_text'].apply(lambda x: count_word_occurrences(x, search_word))
    # Assuming df['word_count'] has been calculated and average_word_count is computed
    average_word_count = df.groupby('place_clean')['word_count'].mean()

    # Normalize the average_word_count series
    normalized_word_count =average_word_count #(average_word_count - average_word_count.min()) / (average_word_count.max() - average_word_count.min())

    df['normalized_word_count'] = df['place_clean'].map(normalized_word_count)
    # Create a choropleth trace

    trace = go.Choropleth(
        locations=normalized_word_count.index,  # Country names
        z=normalized_word_count.values,  # Sentiment scores
        locationmode="country names",
        showscale=True,  # Show color scale legend
        geojson=worldCountries,  # GeoJSON file for country boundaries
        featureidkey="properties.name",  # Key for country names in GeoJSON
        marker_line_color="white",  # Color of country boundaries
        marker_line_width=2,  # Width of country boundaries
        colorscale="RdYlGn",  # Red-Yellow-Green color scale
        reversescale=False,  # Reverse the color scale
        colorbar=dict(len=0.5),
    )
    # Create the figure
    fig = go.Figure(trace)

    # Customize the layout (optional)
    fig.update_geos(projection_type="natural earth")
    fig.update_layout(height=1000, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Show the plot
    fig.update_layout(title=dict(
            #text='Average Word Density',  # Add a title to your map
            x=0.5,  # Center the title
            xanchor='center',
            yanchor='top'
        ),
        geo=dict(
            showframe=False, 
            showcoastlines=True, 
            showocean=True,  # Add this line to show oceans
            oceancolor="LightBlue"  # You can choose any color you like
        ),)

    return fig



def zoom_country(fig, country, geo_path):
    geo_df = pd.read_csv(geo_path)
    coord_row = geo_df[(geo_df['COUNTRY'].str.lower() == country.lower()) | (geo_df['ISO'].str.lower() == country.lower())]
    if (coord_row.empty):
        return

    #TODO: Maybe make an animation when transitioning from country to country


    fig.update_geos(
        center={'lon': coord_row.iloc[0]['longitude'], 'lat': coord_row.iloc[0]['latitude']},
        projection_scale=4,
    )
    return fig

@app.callback(
    Output('word-search-map', 'figure'),
    [Input('search-button', 'n_clicks'), Input('country-button', 'n_clicks')],
    [State('search-input', 'value'), State('country-input', 'value'), State('file-selector', 'value')]
)
def update_word_search_map(search_clicks, country_clicks, search_query, country_query, selected_file):
    if search_clicks > 0 or country_clicks > 0:
        fig = plot_word_search(selected_file, search_query)
        if country_query:
            fig = zoom_country(fig, country_query, 'countries.csv')
        return fig
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
