import pandas as pd
from datetime import datetime
import re
from dash import dcc, Input, Output, html
from chessdotcom import get_player_stats

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

def update_output(input):
    children = []
    # Utilisez une regex pour extraire les informations de la chaîne de caractères
    categories = re.findall(r'Catégorie : (.?)\n', input)
    rankings = re.findall(r'Classement : (.?)\n', input)
    best_rankings = re.findall(r'Meilleur classement : (.?)\n', input)
    num_games_played = re.findall(r'Nombre de parties jouées : (.?)\n', input)
    activity_ratios = re.findall(r"ratio d'activité : (.?)\n", input)
    win_percentages = re.findall(r'Pourcentage de victoires : (.?)\n', input)

    for i in range(len(categories)):
        category = categories[i]
        ranking = rankings[i]
        best_ranking = best_rankings[i]
        num_games = num_games_played[i]
        activity_ratio = activity_ratios[i]
        win_percentage = win_percentages[i]
        # Créez un dictionnaire de styles pour chaque type d'élément
        h3_style = {'textAlign': 'center', 'color': '#7fa650 ', 'fontSize': '24px', 'fontWeight': 'bold', 'marginBottom': '20px'}
        p_style = {'textAlign': 'center','color': '#ffffff', 'fontSize': '20px', 'fontWeight': 'bold', 'marginBottom': '10px'}

        # Ajoutez les éléments à la liste children en utilisant les styles définis
        children.append(html.H3(f'Category: {category}', style=h3_style))
        children.append(html.P(f'Ranking: {ranking}', style=p_style))
        children.append(html.P(f'Best ranking: {best_ranking}', style=p_style))
        children.append(html.P(f'Number of games played: {num_games}', style=p_style))
        children.append(html.P(f'Activity ratio: {activity_ratio}', style=p_style))
        children.append(html.P(f'Win percentage: {win_percentage}', style=p_style))

    return children


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
            chn += 'Classement : ' + 'No ranking' + '\n'
            chn += 'Meilleur classement : ' + 'No ranking' + '\n'
            chn +='Nombre de parties jouées : ' + 'No ranking' + '\n'
            chn += "ratio d'activité : " + 'No ranking' + '\n'
            chn += "Pourcentage de victoires : " + 'No ranking' + '\n'    
    return chn