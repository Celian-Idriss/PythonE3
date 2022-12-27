import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import urllib.request
import zipfile
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import dash
from dash import dcc, Input, Output, html
from dash import html

global file

def dataFrame_to_csv(file, date_nouvelle):
    df = pd.read_xml(file)
    name = date_nouvelle.strftime("%d-%m-%Y") + ".csv"
    df.to_csv(name, sep=';', index = False)

#télécharge le fichier sur internet et le sauvegarde dans un fichier csv
def download_file(url, file_name):
    import requests
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

def conversion_date(chn):
    #dico des correspondance entre les moiset les chiffres
    dico = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    mois = int(dico[chn[4:7]])
    jour = int(chn[1:3])
    annee = int(chn[8:12])
    return datetime(annee, mois, jour)


if __name__ == '__main__':
    # Récupère la liste des fichiers du répertoire courant
    files = os.listdir(".")

    # Filtre la liste des fichiers pour ne garder que ceux qui ont l'extension .xml
    xml_files = [f for f in files if f.endswith(".xml")]

    # Filtre la liste des fichiers pour ne garder que ceux qui ont l'extension .csv
    csv_files = [f for f in files if f.endswith(".csv")]

    #date du fichier dans le répertoire courant
    if xml_files != []:
        chn = xml_files[0][0:10]
        date_courent = datetime.strptime(chn, "%d-%m-%Y")
    else:
        #On met une date très ancienne pour que le fichier soit téléchargé obligatoirement
        date_courent = datetime(1900, 1, 1)

    # Récupération de la page web
    url = "https://ratings.fide.com/download.phtml"
    response = urllib.request.urlopen(url)
    data = response.read()

    # Parse le contenu de la page Web
    soup = BeautifulSoup(data, "html.parser")

    # Recherche la balise qui suit "http://ratings.fide.com/download/players_list_xml.zip"
    link = soup.find(string="Download full list of players")

    # Affiche le contenu de la balise small suivante
    if link:
        small = link.findNext("small")
        if small:
            small = small.findNext("small")

    date_nouvelle = conversion_date(small.text)

    #si la date du fichier sur le site est plus récente que celle du fichier dans le répertoire courant
    if date_nouvelle > date_courent:

        #on supprime le fichier csv et xml
        if xml_files != []:
            os.remove(xml_files[0])
            os.remove(csv_files[0])

        # Téléchargement du fichier
        download_file("http://ratings.fide.com/download/players_list_xml.zip", "myfile.zip")

        # Décompression du fichier .zip
        with zipfile.ZipFile("myfile.zip", 'r') as zipObj:
            zipObj.extractall()

        # Récupère la liste des fichiers du répertoire courant
        files = os.listdir(".")

        # Filtre la liste des fichiers pour ne garder que ceux qui ont l'extension .xml
        xml_files = [f for f in files if f.endswith(".xml")]

        #on renomme le fichier xml
        new_name = date_nouvelle.strftime("%d-%m-%Y") + ".xml"

        os.rename(xml_files[0], new_name)

        #on convertit le fichier xml en csv
        dataFrame_to_csv(new_name, date_nouvelle)
    
    # Récupère la liste des fichiers du répertoire courant
    files = os.listdir(".")

    # Filtre la liste des fichiers pour ne garder que ceux qui ont l'extension .csv
    csv_file = [f for f in files if f.endswith(".csv")]
    

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

    #on lit le fichier csv
    file = pd.read_csv(csv_file[0], sep=';')

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
    