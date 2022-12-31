import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import os
import dash
from dash import dcc, Input, Output, html
from date_fichier import *

global file

if __name__ == '__main__':

    #On regarde si le fichier de notre repertoir courant est le dernier ficheir disponible sur le site
    regarde_date()

    # Récupère la liste des fichiers du répertoire courant
    files = os.listdir(".")

    # Filtre la liste des fichiers pour ne garder que ceux qui ont l'extension .csv
    csv_file = [f for f in files if f.endswith(".csv")]

    
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
            newFile = newFile[newFile['country'] == country]
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
        #on filtre le fichier pour ne garder que les lignes qui ont un rating non null et différent de 0
        hist = newFile[newFile['rating'].notna() & (newFile['rating'] != 0)]
        fig = px.histogram(hist, x="rating", nbins=20, title='Rating repartition', color_discrete_sequence=['#f0d9b5'])
        fig.update_layout(paper_bgcolor='#312e2b', font_color='#FFFFFF', plot_bgcolor='#b58863', title_font_color='#7fa650', title_x=0.5)

        #CAMEMBERT SEX
        fig3 = px.pie(newFile, values='sum', title='Gender distribution', names='sex')
        fig3.update_layout(paper_bgcolor='#f0d9b5', font_color='#FFFFFF', title_x=0.5)

        #CAMEMBERT TITLE
        newFileForTitle = newFile[newFile['title'].notna()]
        fig4 = px.pie(newFileForTitle, values='sum', title='Title Repartiton', names='title')
        fig4.update_layout(paper_bgcolor='#b58863', font_color='#FFFFFF', title_x=0.5)

        #PLAN
        new_file = newFile.groupby(['country']).sum(numeric_only=True).reset_index()
        plan = px.choropleth(
            new_file,
            locations='country',
            color='sum',
            labels={'sum':'number of players'},
            projection="natural earth",
            title="Players Repartition by Country",
        )
        plan.update_layout(paper_bgcolor='#312e2b', font_color='#FFFFFF', plot_bgcolor='#f0d9b5', title_font_color='#7fa650', title_x=0.5)

        #TABLEAU
        #trie les données par rating
        tableau = newFile.sort_values(by=['rating'], ascending=False)[0:10]
        #garde seulement les colonnes qui nous intéressent (name, country, rating, rapid_rating, blitz_rating, sum, sex, title, birthday)
        tableau = tableau[['name', 'country','title', 'rating', 'rapid_rating', 'blitz_rating', 'sex', 'birthday']]

        tableau = tableau.applymap(convert_to_int)

        fig2 = ff.create_table(tableau)

        return fig, fig2, fig3, fig4, plan

    #callback pour le bouton de chess.com
    @app.callback( 
        Input('Player 1', 'value'),
        Input('Player 2', 'value'),
        output=[Output('output_1', 'children'), Output('output_2', 'children')],
    )
    def update_chesscom(input_1, input_2):
        output1_children = update_output(get_player_ranking(input_1))
       
        output2_children = update_output(get_player_ranking(input_2))
        print(output1_children + 'balbalbla')
        print(output2_children + 'jkqldfjqkdf   ')
        return output1_children, output2_children

    output1_children = []
    output2_children = []

    #on lit le fichier csv
    file = pd.read_csv(csv_file[0], sep=';')

    #créé un nouvelle collone sum avec pour valeur 1 (permet de créé un compteur)
    file['sum'] = 1

    #supprime les valeurs null de la collone title
    fileForTitle = file[file['title'].notna()]

    #supprime les valeurs null de la collone birthday et trie par ordre décroissant de birthday (pour le dropdown) les date doivent être supérieur à 1920
    fileBirtday = file[file['birthday'].notna() & (file['birthday'] > 1920)].sort_values(by=['birthday'], ascending=False)

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
        style={'backgroundColor': '#312e2b'},
        children=[        
            html.H1(
                children='Chess Dashboard',
                style={'textAlign': 'center', 'color': '#7fa650', 'font-size': '64px', 'font-weight': 'bold', 'margin-bottom': '30px', 'margin-top': '0px'}
            ),
            html.P(
                style={'textAlign': 'center', 'font-size': '20px', 'margin-bottom': '30px', 'color': '#ffffff', 'margin': '0px 25% 0px 25%'}, 
                children=[
                    "Welcome to our dashboard! Here are some information about chess :", html.Br(),html.Br(),
                    "Chess is a strategy game played by two players on a board of 64 squares, made up of 32 white squares and 32 black squares. Each player has 16 pieces, including a king, queen, two rooks, two bishops, two knights, and eight pawns. The white pieces are played by one player and the black pieces by the other. Players take turns moving one of their pieces. The goal of the game is to put the opponent's king in a position of checkmate, where the king is in danger and there is no way to protect it. Chess is considered a sport in many countries, including France.",
                    html.Br(), html.Br(), "The goal of this dashboard is to allow you to visualize the data from the International Chess Federation (FIDE) through various charts and graphs."
                ]    
            ),
            html.P(
                style={'textAlign': 'center', 'font-size': '20px', 'margin-bottom': '30px', 'size': '50%', 'color': '#ffffff'},
                children=[
                    'You can change the display options if you want : '
                ]    
            ),
            html.Div(
                style={'text-align': 'center', 'margin-bottom': '20px'}, 
                children=[
                    html.H3(
                        children='Name',
                        style={'textAlign': 'center', 'color': '#7fa650 ', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}
                    ),
                    dcc.Input(
                        id='inputName', 
                        value='',
                        type='text', 
                        style={'width': '40%', 'display': 'inline-block', 'font-size': '20px', 'background-color': '#f0d9b5', 'color': '#7fa650'} 
                    )    
                ]
            ),                
            html.Div(                    
                style={'width': '24%', 'display': 'inline-block', 'backgroundColor': '#312e2b', 'margin-left': '2%'},                   
                children=[                        
                    html.H3(                            
                        children='Country',     
                        style={'textAlign': 'center', 'color': '#7fa650 ', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}                        
                    ),                        
                    dcc.Dropdown(                            
                        id='countryDropdown',                             
                        options= optionCountry,                            
                        value='ALL',                            
                        style={'font-size': '20px', 'padding': '10px', 'background-color': '#b58863'}                               
                    )                    
                ]
            ),
            html.Div(
                style={'width': '24%', 'display': 'inline-block', 'backgroundColor': '#312e2b'},
                children=[                        
                    html.H3(                            
                        children='Sex',                            
                        style={'textAlign': 'center', 'color': '#7fa650 ', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}                        
                    ),                        
                    dcc.Dropdown(                                            
                        id='sexDropdown',                                            
                        options= optionSex,                                            
                        value='ALL',                                            
                        style={'font-size': '20px', 'padding': '10px', 'background-color': '#f0d9b5'}                                   
                    )                    
                ]
            ),       
            html.Div(                    
                style={'width': '24%', 'display': 'inline-block', 'backgroundColor': '#312e2b'},                    
                children=[                        
                    html.H3(                            
                        children='Title',                            
                        style={'textAlign': 'center', 'color': '#7fa650 ', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}                        
                    ),                       
                    dcc.Dropdown(                                            
                        id='titleDropdown',                                            
                        options= optionsTitle,                                            
                        value='ALL',                                            
                        style={'font-size': '20px', 'padding': '10px', 'background-color': '#b58863'}                                    
                        )                    
                    ]
            ),
            html.Div(
                style={'width': '24%', 'display': 'inline-block', 'backgroundColor': '#312e2b', 'margin-right': '2%'},
                children=[                        
                    html.H3(                            
                        children='Date',                            
                        style={'textAlign': 'center', 'color': '#7fa650 ', 'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '20px'}                        
                    ),                        
                    dcc.Dropdown(                            
                        id='DateDropdown',                                            
                        options= optionsAge,
                        value='ALL',
                        style={'font-size': '20px', 'padding': '10px', 'background-color': '#f0d9b5'}
                    )
                ]
            ),
            dcc.Graph(
                id='graph1',
                figure=fig,
                style={'height': '12%', 'width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '2%'}
            ),
            dcc.Graph(
                id='plan',
                figure=plan,
                style={'height': '12%', 'width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '2%'}
            ),
            html.P(
                style={'textAlign': 'center', 'font-size': '25px', 'margin-bottom': '30px', 'color': '#ffffff'},
                children=[
                    html.Br(), '10 best players by rating : '
                ]
            ),        
            dcc.Graph(
                id='graph2',
                figure=fig2,
                style={'height': '10%', 'width': '96%', 'display': 'inline-block', 'vertical-align': 'top', 'margin' : '0px 2% 20px 2%'}
            ),
            dcc.Graph(
                id='graph3',
                figure=fig3,
                style={'height': '10%', 'width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '2%'}
            ),
            dcc.Graph(
                id='graph4',
                figure=fig4,
                style={'height': '10%', 'width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '2%'}
            ),
            #tout ce qui a a voir avec le chess.com est dans une Div
            html.H3(
                children='Chess.com',
                style={'textAlign': 'center', 'color': '#7fa650 ', 'font-size': '50px', 'font-weight': 'bold', 'margin-bottom': '20px'}
            ),
            html.P(
                style={'textAlign': 'center', 'font-size': '25px', 'margin-bottom': '30px', 'color': '#ffffff'}, 
                children=[
                html.Br(), 'Enter the name of two players to compare their statistics on chess.com : '
                ]    
            ),
            html.Div(
                style={'text-align': 'center', 'margin-bottom': '20px'},
                children=[
                    dcc.Input(
                        id='Player 1', 
                        value='idrissb77',
                        type='text', 
                        style={'width': '20%', 'display': 'inline-block', 'font-size': '20px', 'margin-right': '2%'}  
                    ),
                    dcc.Input(
                        id='Player 2', 
                        value='valtozz',
                        type='text', 
                        style={'width': '20%', 'display': 'inline-block', 'font-size': '20px'}
                    )
                ]
            ), 
            html.Div(
                id='output_1',
                style={'height': '10%', 'width': '49%', 'vertical-align': 'top', 'margin-left': '1%', 'display': 'inline-block'},
                children=output1_children
            ),
            html.Div(
                id='output_2',
                style={'height': '10%', 'width': '49%', 'vertical-align': 'top', 'margin-left': '1%', 'display': 'inline-block'},
                children=output2_children
            )
    ]
)
app.run_server(debug=True)