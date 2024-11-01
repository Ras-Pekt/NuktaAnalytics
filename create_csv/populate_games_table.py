#!/usr/bin/python3
import json
import os

import pandas as pd

from . import games, save_df


def populate_games_table(all_games_json, allgames_csv):
    if not os.path.exists(all_games_json):
        games.get_games()

    with open(all_games_json, "r") as infile:
        data = json.load(infile)

    game_list_from_site = [
        {
            "game_id": game.get("game_id"),
            "home": game.get("home").lower(),
            "away": game.get("away").lower(),
            "timestamp": game.get("timestamp"),
        }
        for game in data
    ]

    df = pd.read_csv(allgames_csv)
    df["playerType"] = df["playerType"].str.lower()

    game_id_list_from_csv = [game_id for game_id in df["game_id"].unique()]

    game_table = []
    for game in game_list_from_site:
        if game["game_id"] in game_id_list_from_csv:
            game_df = df[df["game_id"] == game["game_id"]]

            home_df = game_df[game_df["playerType"] == game["home"]]
            home_points = home_df["PTS"].sum().sum()

            away_df = game_df[game_df["playerType"] == game["away"]]
            away_points = away_df["PTS"].sum().sum()

            if home_points > away_points:
                winner = game["home"]
                loser = game["away"]
            else:
                winner = game["away"]
                loser = game["home"]

            game_table.append(
                {
                    "game_id": game["game_id"],
                    "home": game["home"],
                    "away": game["away"],
                    "timestamp": game["timestamp"],
                    "winner": winner,
                    "loser": loser,
                }
            )
    df = pd.DataFrame(game_table)

    print(df.info())

    save_df.to_csv(df, "./files/games_table.csv")
