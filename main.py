import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

import dash
from dash import dcc, Input, Output, html
from dash import html

def dataFrame_to_csv(file):
    file.to_csv("test.csv", sep=';', index = False)

if __name__ == '__main__':

    app = dash.Dash(__name__)

    file = pd.read_csv("test.csv", sep=';')
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
    #supprime les ligne dont la valeur de la colonne flag n'est pas null
    file_sample = file[file['flag'].isnull()]
    #supprime les colones inutile

    file_sample = file_sample.drop(['sum','fideid','w_title','o_title','foa_title','games','k','flag'], axis=1)
    #tri les valeurs par rating de manière décroissante
    file_sample = file_sample.sort_values(by=['rating'], ascending=False)
    file_sample = file_sample[0:10]
    fig2 = ff.create_table(file_sample)

    #créé un camembert avec la somme des sexes
    fig3 = px.pie(file, values='sum', title='', names='sex')

    #supprime les valeurs null de la collone title
    fileForTitle = file[file['title'].notna()]
    #créé un camembert avec la somme des titres mais exclu les valeurs null
    fig4 = px.pie(fileForTitle, values='sum', title='', names='title')

    fileBirtday = file[file['birthday'].notna()].sort_values(by=['birthday'], ascending=False)

    #créé les options pour les différents dopdown
    optionCountry = [{'label': i, 'value': i} for i in file['country'].unique()]
    optionSex = [{'label': i, 'value': i} for i in file['sex'].unique()]
    optionsTitle = [{'label': i, 'value': i} for i in fileForTitle['title'].unique()]
    optionsAge = [{'label': i, 'value': i} for i in fileBirtday['birthday'].unique()]

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
        #permet de rentrer un nom
        dcc.Input(id='inputName', type='text'),
        dcc.Dropdown(
            id='countryDropdown',
            options= optionCountry,
            value=''
        ),
        dcc.Dropdown(
            id='sexDropdown',
            options= optionSex,
            value=''
        ),
        dcc.Dropdown(
            id='titleDropdown',
            options= optionsTitle,
            value=''
        ),
        dcc.Dropdown(
            id='DateDropdown',
            options= optionsAge,
            value=''
        ),
        html.Button('Enter', id='button'),
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
    #écrit idriss dans inputname quand on clique sur le bouton enter
    @app.callback(
        Output('inputName', 'value'),
        Input('button', 'n_clicks')
    )
    def update_output(n_clicks):
        return 'idriss' + str(n_clicks)

    app.run_server(debug=True) # (8)