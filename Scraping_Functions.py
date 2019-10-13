# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 11:11:06 2019

@author: GrigorianPC
"""
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
def Generate_Team_List(string):
    beginning = string.find('var teams')
    ending = string.find(']',beginning)
    Raw_Teams = string[beginning:ending+1]
    Team_Count = Count_Teams(Raw_Teams)
    return Construct_Team_List(Team_Count,Raw_Teams)

def Count_Teams(string):
    return string.count('},{')+1

def Next_String_Info(string,start):
    beginning = string.find('{',start)
    ending = string.find('}}',start)+2
    return string[beginning:ending],ending

def Retrieve_Name(Team_Info):
    beginning = Team_Info.find("\"name\"")+8
    ending = Team_Info.find(',',beginning)-1
    return Team_Info[beginning:ending]

def Retrieve_Type(Team_Info):
    beginning = Team_Info.find("\"team_type\"")+len("\"team_type\":\"")
    ending = Team_Info.find(',',beginning)-1
    return Team_Info[beginning:ending]

def Retrieve_Slug(Team_Info):
    beginning = Team_Info.find("\"slug\"")+len("\"slug\":\"")
    ending = Team_Info.find(',',beginning)-1
    return Team_Info[beginning:ending]

def Retrieve_Region(Team_Info):
    beginning = Team_Info.find("\"region_id\"")+len("\"region_id\":\"")
    ending = Team_Info.find(',',beginning)-1
    result = Team_Info[beginning:ending]
    if result == '1':
        result = 'Northeast'
    elif result == '2':
        result = 'Mid-Atlantic'
    elif result == '3':
        result = 'Midwest'
    elif result =='4':
        result = 'West'
    elif result =='5':
        result = 'South'
    elif result == '6':
        result = 'Southwest'
    elif result == '12':
        result = 'Northwest'
    elif result == '13':
        result = 'Great Lakes'
    return result

def Construct_Team_List(Team_Count,Raw_Teams):
    Names_List=[]
    Type_List=[]
    Region_List=[]
    Slug_List=[]
    Counter=0
    tracker=0
    while Counter < Team_Count:
        Team_Info,tracker = Next_String_Info(Raw_Teams,tracker)
        Names_List.append(Retrieve_Name(Team_Info))
        Type_List.append(Retrieve_Type(Team_Info))
        Region_List.append(Retrieve_Region(Team_Info))
        Slug_List.append(Retrieve_Slug(Team_Info))
        Counter=Counter+1
    return Names_List,Type_List,Region_List,Slug_List
#==============================================================================
#Methods to retrieve data from the team previous scores page output data
def Retrieve_Record_Information(Table_List):
    Date_List=[]
    Time_List=[]
    Team1_List=[]
    Team2_List=[]
    Team1_Score=[]
    Team2_Score=[]
    for table in Table_List:
        count = 0;
        for row in table.findAll("tr"):
            cells = row.findAll('td')
            if count % 2 == 0:
                string = cells[0].text
                game_time=Retrieve_Game_Time(string)
                Time_List.append(game_time)
                Date_List.append(string[0:10])
                Team1_List.append(cells[1].text)
                Team1_Score.append(cells[2].text)
            else:
                Team2_List.append(cells[0].text)
                Team2_Score.append(cells[1].text)
            count=count+1
    return Date_List,Time_List,Team1_List,Team2_List,Team1_Score,Team2_Score

def Retrieve_Game_Time(string):
    if string[len(string)-4:]=="(OT)":
        game_time = string[len(string)-10:]
    else:
        game_time = string[len(string)-6:]
    return game_time

def Record_Data_Table(Date_List,Time_List,Team1_List,Team2_List,Team1_Score,Team2_Score):
    df=pd.DataFrame(Date_List,columns =['Date'])
    df['Game Time']=Time_List
    df['Team 1']=Team1_List
    df['Team 2']=Team2_List
    df['Team 1 Score']=Team1_Score
    df['Team 2 Score']=Team2_Score
    return df

def Sort_Scores(Team1_List,Team2_List,Team1_Score,Team2_Score):
    for i in range(0,len(Team1_List)):
        if Team1_List[i] > Team2_List[i]:
            Temp = Team1_List[i]
            Team1_List[i]=Team2_List[i]
            Team2_List[i]=Temp
            Temp_Score=Team1_Score[i]
            Team1_Score[i]=Team2_Score[i]
            Team2_Score[i]=Temp_Score
    return None

def Update_Master_List(Master_List,Date_List,Time_List,Team1_List,Team2_List,Team1_Score,Team2_Score):
    for i in range(0,len(Date_List)):
        String=Date_List[i]+'|'+Time_List[i]+'|'+Team1_List[i]+'|'+Team2_List[i]+'|'+Team1_Score[i]+'|'+Team2_Score[i]
        if not( String in Master_List):
            Master_List.append(String)
    return None

def Pull_Games(Master_List,slug):
    url = "https://www.usquidditch.org/team/" + slug +"/pastGames/"
    page=urllib.request.urlopen(url)
    soup = BeautifulSoup(page,'lxml')
    Table_List=soup.find_all('table')
    Date_List,Time_List,Team1_List,Team2_List,Team1_Score,Team2_Score=Retrieve_Record_Information(Table_List)
    Sort_Scores(Team1_List,Team2_List,Team1_Score,Team2_Score)
    Update_Master_List(Master_List,Date_List,Time_List,Team1_List,Team2_List,Team1_Score,Team2_Score)
    return None

def Split_Master_List(Master_List):
    Date_List=[]
    Time_List=[]
    Team1_List=[]
    Team2_List=[]
    Team1_Score=[]
    Team2_Score=[]
    for i in range(0,len(Master_List)):
        Temp=Master_List[i].split('|')
        Date_List.append(Temp[0])
        Time_List.append(Temp[1])
        Team1_List.append(Temp[2])
        Team2_List.append(Temp[3])
        Team1_Score.append(Temp[4])
        Team2_Score.append(Temp[5])
    return Date_List,Time_List,Team1_List,Team2_List,Team1_Score,Team2_Score

def Generate_Master_Teams_List(Team1_List,Team2_List):
    Master_Teams_List=[]
    for i in range(0,len(Team1_List)):
        if not Team1_List[i] in Master_Teams_List:
            Master_Teams_List.append(Team1_List[i])
        if not Team2_List[i] in Master_Teams_List:
            Master_Teams_List.append(Team2_List[i])
    Master_Teams_List.sort()
    return Master_Teams_List
            
        