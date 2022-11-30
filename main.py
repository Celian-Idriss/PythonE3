import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

import dash
from dash import dcc
from dash import html

def dataFrame_to_csv(file):
    file.to_csv("test.csv", sep=';', index = False)

if __name__ == '__main__':

    app = dash.Dash(__name__)

    file = pd.read_csv("test.csv", sep=';')
    dataFrame_to_csv(file)
    #créé un nouvelle collone sum avec pour valeur 1 (permet de créé un compteur)
    file['sum'] = 1

    #créé un histogramme avec plotly express
    fig = px.histogram(file, x="rating", nbins=20)
    country_data = px.data.gapminder()

    #Création d'un dataframe avec deux colonnes (contry et nbr) qui pour chaque pays compte le nombre de joueurs qu'il y a
    new_file = file.groupby(['country']).sum().reset_index() 


    plan = px.choropleth(new_file, 
                            locations='country', 
                            color='sum',
                           labels={'sum':'number of players'},
                           projection='orthographic',
                           title="Players Repartition",
                          )

    #créé un tableau
    #supprime les colones inutile
    file_sample = file.drop(['sum','fideid','w_title','o_title','foa_title','games','k','flag'], axis=1)

    #tri les valeurs par rating de manière décroissante
    file_sample = file_sample.sort_values(by=['rating'], ascending=False)
    file_sample = file_sample[0:25]
    fig2 =  ff.create_table(file_sample) 

    #créé un camembert avec la somme des sexes
    fig3 = px.pie(file, values='sum', title='', names='sex')

    #supprime les valeurs null de la collone title
    fileForTitle = file[file['title'].notna()]
    #créé un camembert avec la somme des titres mais exclu les valeurs null
    fig4 = px.pie(fileForTitle, values='sum', title='', names='title')

    app.title = 'Chess Dashboard'
    app.layout = html.Div(
    children=[
        html.H1(children=f'Chess Dashboard',
            style={'textAlign': 'center', 'color': '#7FDBFF'}),
        dcc.Graph(
            id='graph1',
            figure=fig
        ),
        dcc.Graph(
            id='plan',
            figure=plan
        ),
        dcc.Graph(
            id='graph2',
            figure=fig2
        ),
        dcc.Graph(
            id='graph3',
            figure=fig3
        ),
        dcc.Graph(
            id='graph4',
            figure=fig4
        )
    ]
)
    

    app.run_server(debug=True) # (8)