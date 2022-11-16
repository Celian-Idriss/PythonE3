import pandas as pd
import csv

'''Fonction qui prends un dataFrame en parametre et retourne le csv correspondant'''
def dataFrame_to_csv(file):
    file.to_csv("new.csv", sep=';', index = False)

#Le main
if __name__ == '__main__':
    file = pd.read_xml("standard_rating_list.xml")
    csv_file = dataFrame_to_csv(file)
    