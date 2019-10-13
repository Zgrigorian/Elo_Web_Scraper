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
#url = "https://www.usquidditch.org/teams"
#page=urllib.request.urlopen(url)
#soup = BeautifulSoup(page,'lxml')
#test = soup.prettify()
#Names_List,Type_List,Region_List,Slug_List=SC.Generate_Team_List(test)
#df=pd.DataFrame(Names_List,columns =['Team Name'])
#df['Team Type']=Type_List
#df['Region']=Region_List
#df['Slug']=Slug_List
#writer = ExcelWriter('C:\Quidditch_Elo_Project\Team_List.xlsx')
#df.to_excel("C:\Quidditch_Elo_Project\Team_List.xlsx")
#print("Exported to Excel")

#Create Master List for this stuff
#Master_List=[]
#
#Name2Slug = dict(zip(Names_List,Slug_List))
#Slug2Name = dict(zip(Slug_List,Names_List))

#This should be its own method for each one
#counter= 1
#for slug in Slug_List:
#    print("Pulling team ", counter)
#    SC.Pull_Games(Master_List,slug)
#    counter=counter+1
#==============================================================================
#Uncomment all of the methods above this line
Date_List,Time_List,Team1_List,Team2_List,Team1_Score,Team2_Score=SC.Split_Master_List(Master_List)
Master_Teams_List=SC.Generate_Master_Teams_List(Team1_List,Team2_List)

#all_links=soup.find_all("a")
#for link in all_links:
#    print(link.get("href"))
#right_table=soup.find_all('var')
#holder = test.find('var teams')
#variable = test[holder:]

#print(right_table)
#A=[]
#B=[]
#C=[]
#D=[]
#E=[]
#F=[]
#G=[]
#for row in right_table.findAll("tr"):
#    print(row)
#    cells = row.findAll('td')
#    states = row.findAll('th')
#    if len(cells) ==6:
#        A.append(cells[0].find(text=True))
#        B.append(cells[0].find(text=True))
#        C.append(cells[1].find(text=True))
#        D.append(cells[2].find(text=True))
#        E.append(cells[3].find(text=True))
#        F.append(cells[4].find(text=True))
#        G.append(cells[5].find(text=True))
#df=pd.DataFrame(A,columns=['Number'])
#df['State/UT']=B
#df['Admin_Capital']=C
#df['Legislative_Captial']=D
#df['Judiciary_Capital']=E
#df['Year_Capital']=F
#df['Former_Capital']=G

