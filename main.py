import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

def dataFrame_to_csv(file):
    file.to_csv("new.csv", sep=';', index = False)

if __name__ == '__main__':

    app = dash.Dash(__name__)

    file = pd.read_xml("standard_rating_list.xml")
    #créé un histogramme avec plotly express
    fig = px.histogram(file, x="rating", nbins=20)

    app.title = 'Chess Dashboard'
    app.layout = html.Div(
    children=[
        html.H1(children=f'Chess Dashboard',
            style={'textAlign': 'center', 'color': '#7FDBFF'}),
        dcc.Graph(
            id='graph1',
            figure=fig
        ),
    ]
    )

    app.run_server(debug=True) # (8)