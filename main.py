import streamlit as st
import pandas as pd
import numpy as np
import requests

# create the url for the api-football site
BASE_URL = "https://v3.football.api-sports.io"
API_KEY =  "ddf604eadb1b6eff2bdbeebee1edca8d"

# create the headers for the request
API_HEADERS = {
   "x-rapidapi-host":"v3.football.api-sports.io",
	"x-rapidapi-key": API_KEY 
}

# create api parameters
API_PARAMETERS = {}

def get_leagues():
    leagues_url = f"{BASE_URL}/leagues"
    response = requests.get(url=leagues_url, headers=API_HEADERS, verify=False)
    # check for response status
    if response.status_code == 200:
        data = response.json()
        leagues = data["response"]
        return leagues
    else:
        print(f"Error: {response.status_code} --> {response.text}")
        return None
    
def get_fixtures(league_id, season):
    fixture_url = f"{BASE_URL}/fixtures?league={league_id}&season={season}"
    response = requests.get(url=fixture_url,headers=API_HEADERS, verify=False)
    # check for response status
    if response.status_code == 200:
        data = response.json()
        fixtures = data["response"]
        return  fixtures
    else:
        print(f"Error:{response.status_code} --> {response.text}")
        return None

# convert fictures to a pandas dataframe
def convert_fixtures_to_dataframe(fixtures):
    # extract relevant fields
      data = []
      for fixture in fixtures:
        data.append({
            "Fixture ID": fixture["fixture"]["id"],
            "Date": fixture["fixture"]["date"],
            "Stadium": fixture["fixture"]["venue"]["name"],
            "Home Team": fixture["teams"]["home"]["name"],
            "Away Team": fixture["teams"]["away"]["name"],
            "Home Goals": fixture["goals"]["home"],
            "Away Goals": fixture["goals"]["away"],
            "Status": fixture["fixture"]["status"]["short"]}
      )
      df_fixtures = pd.DataFrame(data)
      return df_fixtures

    
# main
if __name__ == "__main__":
   leagues = get_leagues()

   print(convert_fixtures_to_dataframe(fixtures=get_fixtures(39, 2020)))

   
