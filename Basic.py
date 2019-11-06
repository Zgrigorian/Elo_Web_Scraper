# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 21:46:29 2019
Webscraper for automatic Elo Calculator
@author: GrigorianPC
"""
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import re
import Scraping_Functions as SC
from selenium import webdriver
import json
from openpyxl import load_workbook
#record=SC.Pull_Teams()
if 1 == 0:
    Links_List=SC.Pull_Links()
    Master_List=[]
    counter = 1 
    for url in Links_List:
        print(url)
        print("Pulling team number ", counter, " of ", len(Links_List))
        SC.Scrape_Games(Master_List,url)
        counter=counter+1
    Master_List.sort()

#==============================================================================
Master_List.sort(reverse=True)
Date_List,Time_List,Team1_List,Team2_List,Team1_Score,Team2_Score=SC.Split_Master_List(Master_List)
Team1_List=SC.Apply_Aliases(Team1_List)
Team2_List=SC.Apply_Aliases(Team2_List)
Master_Teams_List=SC.Generate_Master_Teams_List(Team1_List,Team2_List)
Broken_Seasons=SC.Break_Seasons(Date_List,Master_List)
Over_Times=SC.Record_Overtime(Time_List)
List_of_Games=SC.Generate_Data_Frame_List(Broken_Seasons)
path=r"C:\Quidditch_Elo_Project\Team_List.xlsx"
with pd.ExcelWriter("C:\Quidditch_Elo_Project\Team_List.xlsx") as writer:  # doctest: +SKIP
    for Df in List_of_Games:
        String= Df.iat[-1,0][0:4]
        Year=int(String)
        Name=str(Year)+"-"+str(Year+1)
        Df.to_excel(writer,sheet_name=Name)
print("Exported to Excel")

Team='George Mason University'
Season_Data=List_of_Games[0]
Team1_List=[]
Team2_List=[]
for i in range(0,len(Season_Data)):
    Team1_List.append(Season_Data.iat[i,2])
    Team2_List.append(Season_Data.iat[i,3])
Season_Master_Teams_List=SC.Generate_Master_Teams_List(Team1_List,Team2_List)
Range=[]
for i in range(0,len(Season_Master_Teams_List)):
    Range.append(i)
Team_2_Num=dict(zip(Season_Master_Teams_List,Range))
Num_2_Team=dict(zip(Range,Season_Master_Teams_List))
Team_Game_Indices=[]
for i in range(0,len(Season_Master_Teams_List)):
    Team_Game_Indices.append([])
for i in range(0,len(Team1_List)):
    Team1_Index=Team_2_Num[Team1_List[i]]
    Team2_Index=Team_2_Num[Team2_List[i]]
    Team_Game_Indices[Team1_Index].append(i)
    Team_Game_Indices[Team2_Index].append(i)
Team_Opponents_List=[]
#for i in range(0,len(Team_Game_Indices)):
for i in range(0,1):
    Team_Opponents_List.append([])
    Team_Name=Num_2_Team[i]
    List_Of_Indices=Team_Game_Indices[i]
    for j in range(0,len(List_Of_Indices)):
        index=Team_Game_Indices[i][j]
        if Team1_List[j] == Team_Name:
            Team_Opponents_List[i].append(Team2_List[j])
        else:
            Team_Opponents_List[i].append(Team1_List[j])