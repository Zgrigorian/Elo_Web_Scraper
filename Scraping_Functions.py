# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 11:11:06 2019

@author: GrigorianPC
"""
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
from selenium.webdriver.support.select import Select
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
            elif count % 2 == 1:
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
        String=Reverse_Date(Date_List[i])+'|'+Time_List[i]+'|'+Team1_List[i]+'|'+Team2_List[i]+'|'+Team1_Score[i]+'|'+Team2_Score[i]
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

def Scrape_Games(Master_List,url):
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
        Team1 = Aliases(Team1_List[i])
        Team2 = Aliases(Team2_List[i])
        if not Team1 in Master_Teams_List and Team1 != '':
            Master_Teams_List.append(Team1)
        if not Team2 in Master_Teams_List and Team2 != '':
            Master_Teams_List.append(Team2)
    Master_Teams_List.sort()
    return Master_Teams_List
            
#==============================================================================
def Pull_Links():
    wait=1.25
    url = "http://usquidditch.org/standings"
    page=urllib.request.urlopen(url)
    soup= BeautifulSoup(page,'lxml')
    Season_List=soup.find("select",{"id":"season"})
    Options_List=Season_List.find_all('option')
    browser=webdriver.Chrome()
    browser.get(url)
    Links_List=[]
    Max_Page= browser.find_element_by_id('sp_1_pager')
    for i in range(1,len(Options_List)):
        count=1
        All_Links=browser.find_elements_by_xpath('.//a')
        while count <= int(Max_Page.text):
            All_Links=browser.find_elements_by_xpath('.//a')
            for a in All_Links:
                Link=a.get_attribute('href')
                if Link != None:
                    if Link[len(Link)-11:]=='/pastGames/' and not Find_Slug(Link) == '':
                        if not Link in Links_List:
                            Links_List.append(Link)
                            print(Link)
            next_button = browser.find_element_by_id('next_pager')
            next_button.click()
            #Need to wait for the webpage to actually load before scraping
            time.sleep(wait)
            count=count+1
        select_fr = Select(browser.find_element_by_id("season"))
        select_fr.select_by_index(i)
        #Need to wait for the webpage to actually load before scraping
        time.sleep(wait)
    return Links_List


def Find_Slug(string):
    beginning = string.find('team/')+5
    ending = string.find('/pastGames')
    return string[beginning:ending]
def Example():
    url = "http://kanview.ks.gov/PayRates/PayRates_Agency.aspx"

    # create a new Firefox session
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.get(url)
    
    python_button = driver.find_element_by_id('MainContent_uxLevel1_Agencies_uxAgencyBtn_33') #FHSU
    print(python_button.text)
    python_button.click() #click fhsu link
    return None

def Reverse_Date(string):
    return string[6:10]+'/'+string[0:2]+'/'+string[3:5]

def Initialize_Elo(n):
    return np.ones((n,1),dtype=float)*1000

def Index_Dictionary(Master_Teams_List):
    n = len(Master_Teams_List)
    List=[]
    for i in range(0,n):
        List.append(i)
    return dict(zip(Master_Teams_List, List))

def Apply_Aliases(List):
    n = len(List)
    for i in range(0,n):
        List[i]=Aliases(List[i])
    return List;

def Did_Team_1_Win(Team1_Score,Team2_Score):
    output = -1
    if Team1_Score > Team2_Score:
        output = 1
    return output

def Update_Elo(Team1_Elo,Team2_Elo,Team1_Score,Team2_Score):
    Team1_Win=Did_Team_1_Win(Team1_Score,Team2_Score)
    K=30
    QA=10**(Team1_Elo/400)
    QB=10**(Team2_Elo/400)
    EA=QA/(QA+QB)
    EB=QB/(QA+QB)
    RA_prime=Team1_Elo+K*(Team1_Win-EA)
    RB_prime=Team2_Elo+K*(-Team1_Win+EB)
    return RA_prime,RB_prime

def Reset_Elo(Elo_List):
    n=len(Elo_List)
    for i in range(0,n):
        Elo_List[i]=Elo_List[i]/4+1500*3/4
    return Elo_List

def Calculate_Elo_Scores(Team1_List,Team2_List,Team1_Scores_List,Team2_Scores_List,Elo_List,Index_Dictionary,Date_List):
    n=len(Team1_Scores_List)
    Team1=Team1_List[0]
    Team2=Team2_List[0]
    Team1_Elo=Elo_List[Index_Dictionary[Team1]]
    Team2_Elo=Elo_List[Index_Dictionary[Team2]]
    Team1_Score=Team1_Scores_List[0]
    Team2_Score=Team2_Scores_List[0]
    Elo_List[Index_Dictionary[Team1]],Elo_List[Index_Dictionary[Team2]]=Update_Elo(Team1_Elo,Team2_Elo,Team1_Score,Team2_Score)
    for i in range(1,n):
        if New_Season(Date_List[i],Date_List[i-1]):
            Elo_List=Reset_Elo(Elo_List)
        Team1=Team1_List[i]
        Team2=Team2_List[i]
        Team1_Elo=Elo_List[Index_Dictionary[Team1]]
        Team2_Elo=Elo_List[Index_Dictionary[Team2]]
        Team1_Score=Team1_Scores_List[i]
        Team2_Score=Team2_Scores_List[i]
        Elo_List[Index_Dictionary[Team1]],Elo_List[Index_Dictionary[Team2]]=Update_Elo(Team1_Elo,Team2_Elo,Team1_Score,Team2_Score)
    return Elo_List
      
def New_Season(Date,Date_Previous):
    output=False
    Current_Year=int(Date[0:4])
    Previous_Year=int(Date_Previous[0:4])
    Current_Month=int(Date[5:7])
    Previous_Month = int(Date_Previous[5:7])
    if Current_Month-Previous_Month>3 or Current_Year-Previous_Year > 1:
        output=True
    return output
  
def Fix_Scores(Scores_List):
    n=len(Scores_List)
    Output=[]
    Pulled_Regulation=[]
    Pulled_Overtime=[]
    for i in range(0,n):
        string = Scores_List[i]
        Reg_Pull=False
        Over_Pull=False
        while string[-1]=='*' or string[-1]=='^':
            if string[-1] == '*':
                Reg_Pull=True
            elif string[-1] == '^':
                Over_Pull=True
            string=string[:len(string)-1]
        Pulled_Regulation.append(Reg_Pull)
        Pulled_Overtime.append(Over_Pull)
        Output.append(int(string))
    return Output,Pulled_Regulation,Pulled_Overtime

def Quaffle_Points(Team_Raw_Scores,Team_Pulled_Regular,Team_Pulled_Overtime):
    n=len(Team_Raw_Scores)
    import copy
    Quaffle_Points=copy.deepcopy(Team_Raw_Scores)
    for i in range(0,n):
        if Team_Pulled_Regular[i]==True:
            Quaffle_Points[i]=Quaffle_Points[i]-30
        if Team_Pulled_Overtime[i]==True:
            Quaffle_Points[i]=Quaffle_Points[i]-30
    return Quaffle_Points
    

def Record_Overtime(Time_List):
    n=len(Time_List)
    Output=[]
    for i in range(0,n):
        string=Time_List[i]
        if string[-4:]=='(OT)':
            Output.append(True)
        else:
            Output.append(False)
    return Output

def Count_Seasons(Date_List):
    n=len(Date_List)
    Seasons=1
    for i in range(1,n):
        if New_Season(Date_List[i-1],Date_List[i]):
            Seasons=Seasons+1
    return Seasons

def Break_Seasons(Date_List,Master_List):
    n=len(Date_List)
    Season_Indexes=[-1]
    Broken_Seasons=[]
    for i in range(1,n):
        if New_Season(Date_List[i-1],Date_List[i]):
            Season_Indexes.append(i-1)
    Season_Indexes.append(n)
    for i in range(1,len(Season_Indexes)):
        Broken_Seasons.append(Master_List[Season_Indexes[i-1]+1:Season_Indexes[i]])
    return Broken_Seasons

def Generate_Data_Frame_List(Broken_Seasons):
    List_of_Games=[]
    for i in range(0,len(Broken_Seasons)):
        Date_List,Time_List,Team1_List,Team2_List,Team1_Score,Team2_Score=Split_Master_List(Broken_Seasons[i])
        Team1_List=Apply_Aliases(Team1_List)
        Team2_List=Apply_Aliases(Team2_List)
        Team1_Raw_Score,Team1_Pulled_Regular,Team1_Pulled_Overtime=Fix_Scores(Team1_Score)
        Team2_Raw_Score,Team2_Pulled_Regular,Team2_Pulled_Overtime=Fix_Scores(Team2_Score)
        Team1_Quaffle_Points = Quaffle_Points(Team1_Raw_Score,Team1_Pulled_Regular,Team1_Pulled_Overtime)
        Team2_Quaffle_Points = Quaffle_Points(Team2_Raw_Score,Team2_Pulled_Regular,Team2_Pulled_Overtime)
        Games_df=pd.DataFrame(Date_List,columns=['Date'])
        Games_df['Game Time']=Time_List
        Games_df['Team 1']=Team1_List
        Games_df['Team 2']=Team2_List
        Games_df['Team 1 Score']=Team1_Score
        Games_df['Team 2 Score']=Team2_Score
        Games_df['Team 1 Raw Score']=Team1_Raw_Score
        Games_df['Team 2 Raw Score']=Team2_Raw_Score
        Games_df['Team 1 Quaffle Points']=Team1_Quaffle_Points
        Games_df['Team 2 Quaffle Points']=Team2_Quaffle_Points
        List_of_Games.append(Games_df)
    return List_of_Games


def Aliases(string):
    if string == 'Appalachian State Quidditch':
        string = 'Appalachian Apparators Quidditch'
    elif string == 'Arizona State University - Sun Devil Quidditch':
        string = 'Arizona State University'
    elif string == 'Boise State Abraxans':
        string = 'Boise State Thestrals'
    elif string == 'Carolina Heat Quidditch Club':
        string = 'Terminus Quidditch Atlanta'
    elif string == 'Clark University RavenClarks':
        string == 'Clark University Quidditch'
    elif string == 'College of Charleston':
        string == 'College of Charleston Quidditch'
    elif string == 'NYDC Capitalists':
        string = 'District of Columbia Quidditch Club'
    elif string == 'DeathRow Quidditch Team':
        string = 'Death Row Quidditch'
    elif string == 'Easter Michigan Quidditch Club':
        string = 'Eastern Michigan Quidditch Club'
    elif string == 'George Mason Club Quidditch':
        string = 'George Mason University'
    elif string == 'Grand Valley Grindylows':
        string = 'Grand Valley Quidditch'
    elif string == 'Horn Tailed Horcruxes Quidditch Team':
        string = 'Horn Tailed Horcruxes'
    elif string == 'Illini Ridgebacks Quidditch Team':
        string = 'Illini Ridgebacks Quidditch'
    elif string == 'Indiana University Quidditch Club':
        string = 'Indiana University Quidditch'
    elif string == 'Iowa Quidditch Club':
        string = 'Iowa State Quidditch'
    elif string == 'Lake Effect Maelstrom':
        string = 'Lake Erie Elite'
    elif string == 'Lake Effect Tempest':
        string = 'Lake Erie Elite'
    elif string == 'Loyola University Chicago Quidditch':
        string = 'Loyola University Chicago'
    elif string == 'Loyola University New Orleans Quidditch ':
        string = 'Loyola University New Orleans'
    elif string == 'Michigan State University Spartan Quidditch':
        string = 'Michigan State Quidditch'
    elif string == 'Mizzou Club Quidditch ':
        string = 'Mizzou Quidditch'
    elif string == 'Nearly Headless Knights Quidditch':
        string = 'Nearly Headless Knights'
    elif string == 'Ohio Glory':
        string = 'Ohio Apollos'
    elif string == 'Oklahoma Quidditch':
        string = 'Oklahoma State University'
    elif string == 'Penn Quidditch':
        string = 'Penn State University Nittany Lions'
    elif string == 'Penn State Quidditch':
        string = 'Penn State University Nittany Lions'
    elif string == 'Philadelphia Freedom':
        string = 'Philadelphia Freedom Quidditch Club'
    elif string == 'Purdue Intercollegiate Quidditch Association':
        string = 'Purdue Intercollegiate Quidditch Club '
    elif string == 'Q.C. Pittsburgh':
        string = 'Quidditch Club of Pittsburgh'
    elif string == 'Ringling College of Art and Design Quidditch':
        string = 'Ringling College of Art and Design'
    elif string =='Rochester United':
        string = 'Rochester Hailstorm'
    elif string =='Rutgers University Quidditch 2015-16':
        string = 'Rutgers University Quidditch'
    elif string == 'Rutgers Nearly Headless Knights':
        string = 'Rutgers University Quidditch'
    elif string == 'Silicon Valley Skrewts':
        string = 'Silicon Valley Vipers'
    elif string =='Southern Illinois University Quidditch':
        string = 'Southern Illinois University '
    elif string =='Texas Tech Quidditch Club':
        string = 'Texas Tech Quidditch'
    elif string == 'The Fighting Farmers of America':
        string = 'The Fighting Farmers of Arizona'
    elif string == 'Toledo Firebolts Quidditch':
        string = 'Toledo Quidditch'
    elif string =='Tribe Quidditch':
        string = 'Tribe'
    elif string == 'Tulane University Club Quidditch':
        string = 'Tulane University'
    elif string == 'University of Arkansas Quidditch Club':
        string = 'University of Arkansas'
    elif string == 'University of Dayton Quidditch Club':
        string = 'University of Dayton Quidditch'
    elif string == 'University of Florida Quidditch Club':
        string = 'University of Florida Quidditch'
    elif string == 'University of Massachusetts Amherst Death Beaters':
        string = 'University of Massachusetts Amherst Crabs'
    elif string == 'University of Massachusetts Amherst Sillynannies':
        string = 'University of Massachusetts Amherst Crabs'
    elif string == 'University of Massachusetts Lowell Riverhawks':
        string = 'University of Massachusetts Amherst Crabs'
    elif string == 'University of North Texas Quidditch':
        string = 'University of North Texas'
    elif string == 'University of Texas at San Antonio Club Quidditch':
        string = 'University of Texas at San Antonio'
    elif string == 'University of Vermont Quidditch Club':
        string = 'University of Vermont Quidditch'
    elif string == 'Utah State Quidditch Club - Old':
        string = 'Utah State Quidditch Club'
    elif string == 'Virginia Tech Phoenixes':
        string = 'Quidditch Club at Virginia Tech'
    elif string == 'Virginia Tech':
        string = 'Quidditch Club at Virginia Tech'
    elif string == 'Wizengamot Quidditch of VCU':
        string = 'Wizengamot Quidditch at VCU'
    elif string == 'Quidditch at the University of Virginia':
        string = 'Virginia Quidditch Club'
    elif string =='Drexel Quidditch Club':
        string = 'Drexel University Quidditch Club'
    elif string == '':
        string = 'UNKNOWN TEAM'
    return string