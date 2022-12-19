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


class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
    def handle_starttag(self, tag, attrs):
        print("<< Trouvé balise ouvrante :", tag)
    def handle_endtag(self, tag):
        print(">> Trouvé balise fermante :", tag)
    def handle_data(self, data):
        if data.strip(): print("Trouvé contenu  :", data)

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

    file = pd.read_csv("test.csv", sep=';')
    #créé un nouvelle collone sum avec pour valeur 1 (permet de créé un compteur)
    file['sum'] = 1

    #créé un histogramme avec plotly express
    fig = px.histogram(file, x="rating", nbins=20)
    country_data = px.data.gapminder()

    #Création d'un dataframe avec deux colonnes (contry et nbr) qui pour chaque pays compte le nombre de joueurs qu'il y a
    new_file = file.groupby(['country']).sum().reset_index() 


    plan = px.choropleth(
        new_file, 
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
            value='USA'
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
    #met à jour le graph1 en fonction des valeurs des dropdown
    @app.callback(
        [Output('graph1', 'figure'), Output('graph2', 'figure'), Output('graph3', 'figure'), Output('graph4', 'figure'), Output('plan', 'figure')],
        [Input('countryDropdown', 'value'), Input('sexDropdown', 'value'), Input('titleDropdown', 'value'), Input('DateDropdown', 'value')]
    )
    def update(country, sex, title, date):
        global file
        newFile = file[file['country'] == country]
        newFile = newFile[newFile['sex'] ==  sex]
        newFile = newFile[newFile['title'] ==  title]
        newFile = newFile[newFile['birthday'] ==  date]
        newFile = newFile[newFile['flag'].isnull()]

        #HISTOGRAMME
        fig = px.histogram(newFile, x="rating", nbins=20)

        #TABLEAU
        #supprime les ligne dont la valeur de la colonne flag n'est pas null
        tableau = newFile[0:10]
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

    app.run_server(debug=True)

