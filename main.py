import requests

# create the url for the api-football site
api_url = "https://v3.football.api-sports.io/leagues"

# create the headers for the request
api_headers = {
   "x-rapidapi-host":"v3.football.api-sports.io",
	"x-rapidapi-key": "ddf604eadb1b6eff2bdbeebee1edca8d"
}

# create a list of querry parameters
api_query_parameters = {
    "id": 39,
   "team": 42,
   "season": 2022
}

# create an api get request
response = requests.get(url=api_url, headers=api_headers,params=api_query_parameters ,verify=False)

print(response.text)
