import streamlit as st
import pandas as pd
import numpy as np
import requests
from pyarrow import json
import pyarrow.parquet as pq
import json

# create the url for the api-football site
BASE_URL = "https://v3.football.api-sports.io"
API_KEY =  "ddf604eadb1b6eff2bdbeebee1edca8d"
PASSWORD = "Alexis#21"
USERNAME = "maishasambopape@gmail.com"

# create the headers for the request
API_HEADERS = {
   "x-rapidapi-host":"v3.football.api-sports.io",
	"x-rapidapi-key": API_KEY 
}

def get_fixtures(league_id, season):
   '''Description:: 
            Function gets all season fixtures from the Api-Football api.   
      Parameters:: 
            str: League ID - refer to the API for the applicable IDs
            int: Season - refer to the API for available seasons
      Outputs:: 
            Function returns the api response with list of all fixtures in the specified season and league. 
      Error Handling:: 
            1. If api response=200 (Ok), return the api response data in a json formatt
            2. If api response=204 (No Content), returns the status code
            3. If api response=499 (Time Out), returns the status code
            4. If api response=500 (Internal Server Error), returns the ststus code
   '''
   # create an api endpoint using the base url, league_id, 
   fixture_url = f"{BASE_URL}/fixtures?league={league_id}&season={season}"
   response = requests.get(url=fixture_url,headers=API_HEADERS, verify=False) # send a get request to the api

   # api response status check
   if response.status_code == 200:
      data = response.json()
      return  data["response"]
   elif response.status_code == 204:
      return f"No content found: Error code {response.status_code}."
   elif response.status_code == 499:
      return f"Time out: Error code {response.status_code}."
   else:
      return f"Internal server error: Error code {response.status_code}."

def convert_fixtures_to_dataframe(all_fixtures): 
   '''Description::
            Function converts fixtures data into a pandas  dataframe
      Parameters::
            Dict: all_fixtures - A json dictionary 
      Outputs::
            DataFrame with fixture data
   '''
   # create an empty list 
   fixture_data = []
   # loop through all_fixtures and extract the relevant data points
   for fixture in all_fixtures:
      # append the relevant data points into defined empty list
      fixture_data.append({
         "Fixture ID": fixture['fixture']['id'], 
         "Date": fixture['fixture']['date'], 
         "Home Team": fixture['teams']['home']['name'], 
         "Away Team": fixture['teams']['away']['name'],
         "Home HT Goals": fixture["score"]["halftime"]["home"],
         "Away HT Goals": fixture["score"]["halftime"]["away"],
         "Home FT Goals": fixture["score"]["fulltime"]["home"],
         "Away FT Goals": fixture["score"]["fulltime"]["away"],
         "Match Oficial": fixture["fixture"]["referee"],
         }
      )
   return pd.DataFrame(fixture_data)

def get_list_of_teams(season_id, league_id):
   teams_url = f"{BASE_URL}/teams?league={league_id}&season={season_id}"
   response = requests.get(url=teams_url,headers=API_HEADERS, verify=False)
   teams_data = response.json()["response"]
   teams_venue_info = []
   # extact team name and id
   for i in range(0,len(teams_data)):

      teams_venue_info.append({
      "League ID": 39,
      "Team ID": teams_data[i]["team"]["id"],
      "Team Name": teams_data[i]["team"]["name"],
      "Stadium ID": teams_data[i]["venue"]["id"],
      "Stadium Name": teams_data[i]["venue"]["name"],
      "Stadium Capacity": teams_data[i]["venue"]["capacity"]
         }
      )   
   return pd.DataFrame(teams_venue_info) 

# def get_team_statistics(season_id, team_id, league_id):
#    stats_url = f"{BASE_URL}/teams/statistics?season={season_id}&team={team_id}&league={league_id}"
#    response = requests.get(url=stats_url, headers=API_HEADERS, verify=False)
#    # check if the api request has succeeded
#    if response:
#       data = response.json()
#       return data["response"]
#    else:
#       print("Error fetching the stats.")
# -----------------START HERE WITH FIXING THE CONNECTION TO GETTING TEAM STATS-------------------------    
# # extract the stats into a dataframe
# def get_stats_for_all_teams(list_of_teams,season_id):
#    '''
#       Description::
#             Function gets stats for all the teams in the specified league and season
#       Parameters::
#             List:  list_of_teams 
#       Outputs::
#             List: stats_data_for_teams, a list of dictinaries
#    '''

#    # defined an empty list
#    stats_data_for_teams = []
#    teamID = list_of_teams["Team ID"]
#    # loop through the list_of_teams 
#    for id in teamID:
#       leagueID = list_of_teams["League ID"]
#       # loop through the dictionary and extract the relevant data points
      
#       # declare the following variables as parameters to the "get_team_statistics" function
#       stats_url = f"{BASE_URL}/teams/statistics?season={season_id}&team={id}&league={leagueID}"
#       response = requests.get(url=stats_url, headers=API_HEADERS, verify=False)
#       data = response.json()
      
#       # check if the api request has succeeded
#       if response.status_code == 200:
#          data = response.json()
#          stats_data_for_teams.append(
#             data["response"]
            
#          )  
#          return stats_data_for_teams 
#       else:
#          return f"Error fetching the stats."
      
# convert stats into a daframe
def convert_stats_into_dataframe(all_teams_stats):
   '''Description::
            Function converts stats data into a pandas  dataframe
      Parameters::
            Dict: all_teams_stats, a json dictionary 
      Outputs::
            DataFrame with stats data
   '''
   # define an empty list
   final_stats = []
   # loop through all_teams_stats and extract the relevant data points
   # for i in range(0, len(all_teams_stats)):
   for one_team_stats in all_teams_stats:
      # append the relevant data points into the defined empty list
      final_stats.append({
         "Team ID": one_team_stats["team"]["id"],
         "Team Name": one_team_stats["team"]["name"],
         "Team Form": one_team_stats["form"],
         "Played Home": one_team_stats["fixtures"]["played"]["home"],
         "Played Away": one_team_stats["fixtures"]["played"]["away"],
         "Wins Home": one_team_stats["fixtures"]["wins"]["home"],
         "Wins Away": one_team_stats["fixtures"]["wins"]["away"],
         "Draw Home": one_team_stats["fixtures"]["draws"]["home"],
         "Draw Away": one_team_stats["fixtures"]["draws"]["away"],
         "Loses Home": one_team_stats["fixtures"]["loses"]["home"],
         "Loses Away": one_team_stats["fixtures"]["loses"]["away"],
         "GF Home": one_team_stats["goals"]["for"]["total"]["home"],
         "GF Away": one_team_stats["goals"]["for"]["total"]["away"],
         "GF minute (0-15)":one_team_stats["goals"]["for"]["minute"]["0-15"]["percentage"],
         "GF minute (16-30)":one_team_stats["goals"]["for"]["minute"]["16-30"]["percentage"],
         "GF minute (31-45)":one_team_stats["goals"]["for"]["minute"]["31-45"]["percentage"],
         "GF minute (46-60)":one_team_stats["goals"]["for"]["minute"]["46-60"]["percentage"],
         "GF minute (61-75)":one_team_stats["goals"]["for"]["minute"]["61-75"]["percentage"],
         "GF minute (76-90)":one_team_stats["goals"]["for"]["minute"]["76-90"]["percentage"],
         "GF minute (91-105)":one_team_stats["goals"]["for"]["minute"]["91-105"]["percentage"],
         "GA minute (0-15)":one_team_stats["goals"]["against"]["minute"]["0-15"]["percentage"],
         "GA minute (16-30)":one_team_stats["goals"]["against"]["minute"]["16-30"]["percentage"],
         "GA minute (31-45)":one_team_stats["goals"]["against"]["minute"]["31-45"]["percentage"],
         "GA minute (46-60)":one_team_stats["goals"]["against"]["minute"]["46-60"]["percentage"],
         "GA minute (61-75)":one_team_stats["goals"]["against"]["minute"]["61-75"]["percentage"],
         "GA minute (76-90)":one_team_stats["goals"]["against"]["minute"]["76-90"]["percentage"],
         "GA minute (91-105)":one_team_stats["goals"]["against"]["minute"]["91-105"]["percentage"],
         "Biggest Win Streak":one_team_stats["biggest"]["streak"]["wins"],
         "Biggest Draw Streak":one_team_stats["biggest"]["streak"]["draws"],
         "Biggest Loses Streak":one_team_stats["biggest"]["streak"]["loses"],
         "Biggest Wins Home":one_team_stats["biggest"]["wins"]["home"],
         "Biggest Wins Away":one_team_stats["biggest"]["wins"]["away"],
         "Biggest Loss Home":one_team_stats["biggest"]["loses"]["home"],
         "Biggest Loss Away":one_team_stats["biggest"]["loses"]["away"],
         "Clean Sheet Home":one_team_stats["clean_sheet"]["home"],
         "Clean Sheet Away":one_team_stats["clean_sheet"]["away"],
         "Failed to Score Home":one_team_stats["failed_to_score"]["home"],
         "Failed to Score Away":one_team_stats["failed_to_score"]["away"],
         "Yellow Cards (0-15)":one_team_stats["cards"]["yellow"]["0-15"]["percentage"],
         "Yellow Cards (16-30)":one_team_stats["cards"]["yellow"]["16-30"]["percentage"],
         "Yellow Cards (31-45)":one_team_stats["cards"]["yellow"]["31-45"]["percentage"],
         "Yellow Cards (46-60)":one_team_stats["cards"]["yellow"]["46-60"]["percentage"],
         "Yellow Cards (61-75)":one_team_stats["cards"]["yellow"]["61-75"]["percentage"],
         "Yellow Cards (76-90)":one_team_stats["cards"]["yellow"]["76-90"]["percentage"],
         "Yellow Cards (91-105)":one_team_stats["cards"]["yellow"]["91-105"]["percentage"],
         "Red Cards (0-15)":one_team_stats["cards"]["red"]["0-15"]["percentage"],
         "Red Cards (16-30)":one_team_stats["cards"]["red"]["16-30"]["percentage"],
         "Red Cards (31-45)":one_team_stats["cards"]["red"]["31-45"]["percentage"],
         "Red Cards (46-60)":one_team_stats["cards"]["red"]["46-60"]["percentage"],
         "Red Cards (61-75)":one_team_stats["cards"]["red"]["61-75"]["percentage"],
         "Red Cards (76-90)":one_team_stats["cards"]["red"]["76-90"]["percentage"],
         "Red Cards (91-105)":one_team_stats["cards"]["red"]["91-105"]["percentage"],
      })
   return pd.DataFrame(final_stats)
         
 
# main script execution
if __name__ == "__main__":
   league_id = 39
   team_id = 42
   season = 2020
   stats_output_file = "premier_league_team_stats.csv"

   # fetch list of teams in a season and convering them toa parquet file
   
   # team_list_df = get_list_of_teams(season_id=season, league_id=league_id)
   team_list_df = pd.read_parquet("team_list.parquet")
   # team_list_df.to_parquet("team_list.parquet", engine="fastparquet")
   


   # # fetch all fixtures dataframe and coonvert to a parquet
   # fixtures = get_fixtures(league_id, season)
   # all_fixtures_df = convert_fixtures_to_dataframe(fixtures)
   # all_fixtures_df.to_parquet("fixtures.parquet", engine="fastparquet")

   # fetch all teams stats
   #all_teams_stats_df = get_stats_for_all_teams(team_list_df, season)
   #print(all_teams_stats_df)
   
   # convert all teams stats to dataframe
   
   # with open('stats.json') as f:
   #  data = json.load(f)
   # print(data)
   #print(convert_stats_into_dataframe(data))
   data = pd.read_json('stats.json').to_dict('records')
   #print(convert_stats_into_dataframe(data_df).head())
   stats_df = convert_stats_into_dataframe(data)
   stats_df["GF minute (91-105)"] = stats_df["GF minute (91-105)"].astype('str')
   stats_df["GA minute (91-105)"] = stats_df["GA minute (91-105)"].astype('str')
   stats_df["Biggest Loss Away"] = stats_df["Biggest Loss Away"].astype('str')
   stats_df["Yellow Cards (91-105)"] = stats_df["Yellow Cards (91-105)"].astype('str')
   stats_df["Red Cards (0-15)"] = stats_df["Red Cards (0-15)"].astype('str')
   stats_df["Red Cards (16-30)"] = stats_df["Red Cards (16-30)"].astype('str')
   stats_df["Red Cards (31-45)"] = stats_df["Red Cards (31-45)"].astype('str')
   stats_df["Red Cards (46-60)"] = stats_df["Red Cards (46-60)"].astype('str')
   stats_df["Red Cards (61-75)"] = stats_df["Red Cards (61-75)"].astype('str')
   stats_df["Red Cards (76-90)"] = stats_df["Red Cards (76-90)"].astype('str')
   
   stats_df.to_parquet("final_stats.parquet", engine="fastparquet")
         
  
# -----------------RESERVED IDEAS---------------------------------------------  

# # fetch predictions for remaining fixtures
# def get_remaining_predictions(fixtures, processed_fixture_ids, max_calls=5):
#    predictions_data = []
#    calls_made = 0
#    for fixture in fixtures:
#       if calls_made >= max_calls:
#          break
#       fixture_id = fixture["fixture"]['id']
#       if fixture_id in processed_fixture_ids:
#          continue # skip the already processed fixtures
#       prediction = get_prediction(fixture_id)
#       if prediction:
#          prediction_data = prediction[0]
#          predictions_data.append({ 
#                     "Fixture ID": fixture_id, 
#                     "Date": fixture['fixture']['date'], 
#                     "Home Team": fixture['teams']['home']['name'], 
#                     "Away Team": fixture['teams']['away']['name'], 
#                     "Home Win Probability": prediction_data.get('predictions', {}).get('win_or_draw', {}), 
#                     "Draw Probability": prediction_data.get('predictions', {}).get('win_or_draw', {})}
#                     )
#       else:
#           print(f"No prediction available for fixture ID {fixture_id}") 
#       calls_made += 1
#       time.sleep(1)
   
# def prediction_data_to_dataframe(data):
#       df = pd.DataFrame(data)
#       return df 
       
   
 # fetch all fixtures 
   # fixtures = get_fixtures(league_id, season)
   # print(convert_fixtures_to_dataframe(fixtures))
   #print(f"Fixtures: {fixtures}")

   # fetch team stats
   # stats = get_team_statistics(season, team_id, league_id)
   # print(stats)
   # # Append new predictions to csv
# def save_stats_dataframe_to_csv(stats_dict, output_file):
#    df = pd.DataFrame(stats_dict)
#    if os.path.exists(stats_output_file):
#       df.to_csv(stats_output_file, mode="a", index=False, header=False) # append without header
#    else:
#       df.to_csv(stats_output_file, index=False) # create new file with header