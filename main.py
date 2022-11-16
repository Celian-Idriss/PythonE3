import pandas as pd
import plotly.express as px
import numpy as np

#Fonction qui prends un dataFrame en parametre et retourne le csv correspondant
def dataFrame_to_csv(file):
    file.to_csv("new.csv", sep=';', index = False)

if __name__ == '__main__':
    file = pd.read_xml("standard_rating_list.xml")
    #créé un histogramme avec plotly express
    fig = px.histogram(file, x="rating", nbins=18)
    fig.show()