#!/usr/bin/python3
import json

import requests


def get_games():
    url = "https://allstar.nukta.pro/getAllGames"
    all_games_json = "./files/all_games.json"
    response = requests.get(url)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()

        # Convert the list of dictionaries to a JSON string
        json_string = json.dumps(data, indent=4)  # Add indentation for readability

        # Save the JSON string to a file
        with open(all_games_json, "w") as outfile:
            outfile.write(json_string)

        print("Data successfully saved to all_games.json")
    else:
        print(f"Request failed with status code: {response.status_code}")


def read_game_id():
    # Load the JSON data from the file
    with open("all_games.json", "r") as infile:
        data = json.load(infile)

    for game in data:
        game_id = game.get("game_id")
        yield game_id
