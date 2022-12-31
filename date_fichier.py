import urllib.request
import zipfile
from bs4 import BeautifulSoup
from datetime import datetime
import os
from fuction import *

def regarde_date():
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