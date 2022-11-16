import pandas as pd
import csv

#Le main
if __name__ == '__main__':
    file = pd.read_xml("standard_rating_list.xml")
    file.to_csv("new.csv")