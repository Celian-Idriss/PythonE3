import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import urllib.request
from zipfile import ZipFile
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup

import dash
from dash import dcc, Input, Output, html
from dash import html

global file

def dataFrame_to_csv(file):
    df = pd.read_xml(file)
    #df.to_csv("Players.csv", sep=';', index = False)

#télécharge le fichier sur internet et le sauvegarde dans un fichier csv
def download_file(url, file_name):
    import requests
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

    

if __name__ == '__main__':
    # Récupération de la page web
    url = "https://ratings.fide.com/download.phtml"
    page = requests.get(url)

    # Analyse du code HTML avec Beautiful Soup
    soup = BeautifulSoup(page.content, 'html.parser')

    # Recherche de tous les liens vers des fichiers .zip
    zip = ''
    for link in soup.find_all('a', href=True):
        if link['href'] == 'http://ratings.fide.com/download/players_list_xml.zip':
            zip = link['href']
            break

    # Téléchargement du fichier .zip
    urllib.request.urlretrieve(zip, "myfile.zip")

    # Décompression du fichier .zip
    with ZipFile("myfile.zip", 'r') as zipObj:
        zipObj.extractall()

    app = dash.Dash(__name__)

    @app.callback(
        [Output('graph1', 'figure'), Output('graph2', 'figure'), Output('graph3', 'figure'), Output('graph4', 'figure'), Output('plan', 'figure')],
        [Input('countryDropdown', 'value'), Input('sexDropdown', 'value'), Input('titleDropdown', 'value'), Input('DateDropdown', 'value')]
    )
    def update(country, sex, title, date):
        global file
        newFile = file
        if country != 'ALL': newFile = file[file['country'] == country]
        if sex != 'ALL': newFile = newFile[newFile['sex'] ==  sex]
        if title != 'ALL': newFile = newFile[newFile['title'] ==  title]
        if date != 'ALL': newFile = newFile[newFile['birthday'] ==  date]
        newFile = newFile[newFile['flag'].isnull()]

        #HISTOGRAMME
        fig = px.histogram(newFile, x="rating", nbins=20)

        #TABLEAU
        #supprime les ligne dont la valeur de la colonne flag n'est pas null
        #trie les données par rating
        tableau = newFile.sort_values(by=['rating'], ascending=False)[0:10]
        #supprime les colones inutile
        tableau = tableau.drop(['sum','fideid','w_title','o_title','foa_title','games','k','flag'], axis=1)
        fig2 = ff.create_table(tableau)

        #CAMEMBERT SEX
        fig3 = px.pie(newFile, values='sum', title='', names='sex')

        #CAMEMBERT TITLE
        newFileForTitle = newFile[newFile['title'].notna()]
        fig4 = px.pie(newFileForTitle, values='sum', title='', names='title')

        #PLAN
        new_file = newFile.groupby(['country']).sum().reset_index()
        plan = px.choropleth(
            new_file,
            locations='country',
            color='sum',
            labels={'sum':'number of players'},
            projection='eckert4',
            title="Players Repartition",
        )

        return fig, fig2, fig3, fig4, plan

    file = pd.read_csv("test.csv", sep=';')
    #créé un nouvelle collone sum avec pour valeur 1 (permet de créé un compteur)
    file['sum'] = 1

    #supprime les valeurs null de la collone title
    fileForTitle = file[file['title'].notna()]

    fileBirtday = file[file['birthday'].notna()].sort_values(by=['birthday'], ascending=False)

    #initialise les graphes à zéro
    fig, fig2, fig3, fig4, plan = update('USA', 'M', 'GM', '1995')

    #créé les options pour les différents dropdown
    optionCountry = [{'label': i, 'value': i} for i in file['country'].unique()]
    optionSex = [{'label': i, 'value': i} for i in file['sex'].unique()]
    optionsTitle = [{'label': i, 'value': i} for i in fileForTitle['title'].unique()]
    optionsAge = [{'label': i, 'value': i} for i in fileBirtday['birthday'].unique()]
    #ajoute une option vide
    optionCountry.insert(0, {'label': 'ALL', 'value': 'ALL'})
    optionSex.insert(0, {'label': 'ALL', 'value': 'ALL'})
    optionsTitle.insert(0, {'label': 'ALL', 'value': 'ALL'})
    optionsAge.insert(0, {'label': 'ALL', 'value': 'ALL'})

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
            value='ALL'
        ),
        dcc.Dropdown(
            id='sexDropdown',
            options= optionSex,
            value='ALL'
        ),
        dcc.Dropdown(
            id='titleDropdown',
            options= optionsTitle,
            value='ALL'
        ),
        dcc.Dropdown(
            id='DateDropdown',
            options= optionsAge,
            value='ALL'
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

    app.run_server(debug=True)