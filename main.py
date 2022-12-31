import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import urllib.request
import zipfile
from bs4 import BeautifulSoup
from datetime import datetime
import os
import dash
from dash import dcc, Input, Output, State, html
from chessdotcom import get_player_stats

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

def convert_to_int(x):
  if pd.isnull(x) or isinstance(x, str):
    return x
  return int(x)


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
    

    #On s'occupe de chess.com
    def get_player_ranking(username):
        try:
            player = get_player_stats(username).json
        except:
            return ""

        chn = ''

        categories = ["chess_blitz", "chess_bullet", "chess_rapid"]
        for cat in categories:
            if cat in player['stats']:
                chn += 'Catégorie : ' + cat + '\n'
                chn += 'Classement : ' + str(player['stats'][cat]['last']['rating']) + '\n'
                chn += 'Meilleur classement : ' + str(player['stats'][cat]['best']['rating']) + '\n'
                chn +='Nombre de parties jouées : ' + str(player['stats'][cat]['record']['win'] + player['stats'][cat]['record']['loss'] + player['stats'][cat]['record']['draw']) + '\n'
                chn += "ratio d'activité : " + str(player['stats'][cat]['record']['win']) + 'V / ' + str(player['stats'][cat]['record']['loss']) + 'D / ' + str(player['stats'][cat]['record']['draw']) + 'N' + '\n'
                chn += "Pourcentage de victoires : " + str(round(player['stats'][cat]['record']['win'] / (player['stats'][cat]['record']['win'] + player['stats'][cat]['record']['loss'] + player['stats'][cat]['record']['draw']) * 100, 2)) + "%" + '\n'
            else:
                chn += 'Catégorie : ' + cat + '\n'
                chn += 'Classement : ' + 'Pas de classement' + '\n'
                chn += 'Meilleur classement : ' + 'Pas de classement' + '\n'
                chn +='Nombre de parties jouées : ' + 'Pas de classement' + '\n'
                chn += "ratio d'activité : " + 'Pas de classement' + '\n'
                chn += "Pourcentage de victoires : " + 'Pas de classement' + '\n'    
        return chn
    
    app = dash.Dash(__name__)

    @app.callback(
        [Output('graph1', 'figure'), Output('graph2', 'figure'), Output('graph3', 'figure'), Output('graph4', 'figure'), Output('plan', 'figure')],
        [Input('countryDropdown', 'value'), Input('sexDropdown', 'value'), Input('titleDropdown', 'value'), Input('DateDropdown', 'value'), Input('inputName', 'value')], 
    )

    def update(country, sex, title, date, name):
        global file
        newFile = file
        newFile = newFile[newFile['flag'].str.contains('i', na=False) == False]
        if country != 'ALL': 
            newFile = new_file[new_file['country'] == country]
        if sex != 'ALL': 
            newFile = newFile[newFile['sex'] ==  sex]
        if title != 'ALL': 
            newFile = newFile[newFile['title'] ==  title]
        if date != 'ALL': 
            newFile = newFile[newFile['birthday'] ==  date]
        #si name n'est pas vide on filtre le fichier avec environ le nom sans tenir compte de la casse
        if name != '':
            newFile = newFile[newFile['name'].str.contains(name, case=False, na=False)]

        #HISTOGRAMME
        fig = px.histogram(newFile, x="rating", nbins=20)

        #CAMEMBERT SEX
        fig3 = px.pie(newFile, values='sum', title='', names='sex')

        #CAMEMBERT TITLE
        newFileForTitle = newFile[newFile['title'].notna()]
        fig4 = px.pie(newFileForTitle, values='sum', title='', names='title')

        #PLAN
        new_file = newFile.groupby(['country']).sum(numeric_only=True).reset_index()
        plan = px.choropleth(
            new_file,
            locations='country',
            color='sum',
            labels={'sum':'number of players'},
            projection='eckert4',
            title="Players Repartition",
        )

        #TABLEAU
        #trie les données par rating
        tableau = newFile.sort_values(by=['rating'], ascending=False)[0:10]
        #supprime les colones inutile
        tableau = tableau.drop(['fideid','w_title','o_title','foa_title','games','k','flag', 'sum'], axis=1)

        tableau = tableau.applymap(convert_to_int)

        fig2 = ff.create_table(tableau)


        return fig, fig2, fig3, fig4, plan

    #callback pour le bouton de chess.com
    @app.callback(
        Output('output_1', 'children'),
        Output('output_2', 'children'),   
        Input('bouton', 'n_clicks'),
        State('Player 1', 'value'),
        State('Player 2', 'value'))

    def update_output(n_clicks, input_1, input_2):
        return get_player_ranking(input_1), get_player_ranking(input_2)

    #on lit le fichier csv
    file = pd.read_csv(csv_file[0], sep=';')

    #créé un nouvelle collone sum avec pour valeur 1 (permet de créé un compteur)
    file['sum'] = 1

    #supprime les valeurs null de la collone title
    fileForTitle = file[file['title'].notna()]

    fileBirtday = file[file['birthday'].notna()].sort_values(by=['birthday'], ascending=False)

    #initialise les graphes à zéro
    fig, fig2, fig3, fig4, plan = update('ALL', 'ALL', 'ALL', 'ALL', '')

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
        html.H1(
            children='Chess Dashboard',
            style={'textAlign': 'center', 'color': '#7FDBFF', 'font-size': '64px', 'font-weight': 'bold', 'margin-bottom': '30px'}
        ),
        html.P(
            style={'textAlign': 'center', 'font-size': '25px', 'margin-bottom': '30px'}, 
            children=[
            "Welcome to our dashboard! Here are some information about chess :", html.Br(),
            "Chess is a strategy game played by two players on a board of 64 squares, made up of 32 white squares and 32 black squares. Each player has 16 pieces, including a king, queen, two rooks, two bishops, two knights, and eight pawns. The white pieces are played by one player and the black pieces by the other. Players take turns moving one of their pieces. The goal of the game is to put the opponent's king in a position of checkmate, where the king is in danger and there is no way to protect it. Chess is considered a sport in many countries, including France."
            ]    
        ),
        #ajoute une dive pour graph1 et graph2 pour qu'il s'adapte à la taille de l'écran    
        dcc.Graph(
            id='graph1',
            figure=fig,
            style={'height': '12%', 'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}
        ),
        dcc.Graph(
            id='plan',
            figure=plan,
            style={'height': '12%', 'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}
        ),           
        html.Div(
            style={'text-align': 'center', 'margin-bottom': '20px'}, 
            children=[
                html.H3(
                    children='Name',
                    style={'textAlign': 'center', 'color': '#7FDBFF', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}
                ),
                dcc.Input(
                    id='inputName', 
                    value='',
                    type='text', 
                    style={'width': '40%', 'display': 'inline-block', 'font-size': '20px'}),            
            ]
        ),                
        html.Div(                    
            style={'width': '25%', 'display': 'inline-block'},                    
            children=[                        
                html.H3(                            
                    children='Country',     
                    style={'textAlign': 'center', 'color': '#7FDBFF', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}                        
                ),                        
                dcc.Dropdown(                            
                    id='countryDropdown',                             
                    options= optionCountry,                            
                    value='ALL',                            
                    style={'font-size': '20px', 'padding': '10px'}                               
                )                    
            ]
        ),
        html.Div(
            style={'width': '25%', 'display': 'inline-block'},
            children=[                        
                html.H3(                            
                    children='Sex',                            
                    style={'textAlign': 'center', 'color': '#7FDBFF', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}                        
                ),                        
                dcc.Dropdown(                                            
                    id='sexDropdown',                                            
                    options= optionSex,                                            
                    value='ALL',                                            
                    style={'font-size': '20px', 'padding': '10px'}                                   
                )                    
            ]
        ),       
        html.Div(                    
            style={'width': '25%', 'display': 'inline-block'},                    
            children=[                        
                html.H3(                            
                    children='Title',                            
                    style={'textAlign': 'center', 'color': '#7FDBFF', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}                        
                ),                       
                dcc.Dropdown(                                            
                    id='titleDropdown',                                            
                    options= optionsTitle,                                            
                    value='ALL',                                            
                    style={'font-size': '20px', 'padding': '10px'}                                    
                    )                    
                ]
        ),
        html.Div(
            style={'width': '25%', 'display': 'inline-block'},
            children=[                        
                html.H3(                            
                    children='Date',                            
                    style={'textAlign': 'center', 'color': '#7FDBFF', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}                        
                ),                        
                dcc.Dropdown(                            
                    id='DateDropdown',                                            
                    options= optionsAge,
                    value='ALL',
                    style={'font-size': '20px', 'padding': '10px'}
                )
            ]
        ),
        dcc.Graph(
            id='graph2',
            figure=fig2,
            style={'height': '10%', 'width': '99%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '1%', 'margin-bottom': '20px'}
        ),
        dcc.Graph(
            id='graph3',
            figure=fig3,
            style={'height': '10%', 'width': '49%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '1%'}
        ),
        dcc.Graph(
            id='graph4',
            figure=fig4,
            style={'height': '10%', 'width': '49%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '1%'}
        ),
        #tout ce qui a a voir avec le chess.com est dans une Div
        html.Div(
            style={'text-align': 'center', 'margin-bottom': '20px'}, 
            children=[
                html.H3(
                    children='Chess.com',
                    style={'textAlign': 'center', 'color': '#7FDBFF', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}
                ),
                dcc.Input(
                    id='Player 1', 
                    value='',
                    type='text', 
                    style={'font-size': '20px', 'padding': '10px', 'margin-right': '1%'}
                ),
                dcc.Input(
                    id='Player 2', 
                    value='',
                    type='text', 
                    style={'font-size': '20px', 'padding': '10px', 'margin-left': '1%'}
                ),
                html.Button(
                    id='bouton',
                    children='Valider',
                    style={'margin-left': '1%'}
                ),
                html.Div(
                    id='output_1',
                    style={'margin-top': '20px', 'white-space': 'pre-line'}
                ),
                html.Div(
                    id='output_2',
                    style={'margin-top': '20px', 'white-space': 'pre-line', 'display': 'inline-block',}
                )
            ]
        ),   
    ]
    
)
app.run_server(debug=True)
