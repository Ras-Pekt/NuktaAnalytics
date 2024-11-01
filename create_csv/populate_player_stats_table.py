#!/usr/bin/python3
import json
import os

import pandas as pd

from . import games, player_stats, save_df


def populate_player_stats_table(all_games_json, allgames_csv):
    players_stats_table = []

    if not os.path.exists(all_games_json):
        games.get_games()

    with open(all_games_json, "r") as infile:
        data = json.load(infile)

    game_list_from_site = [
        {
            "game_id": game.get("game_id"),
            "timestamp": game.get("timestamp"),
        }
        for game in data
    ]

    df = pd.read_csv(allgames_csv)
    df["playerType"] = df["playerType"].str.lower()

    game_id_list_from_csv = [game_id for game_id in df["game_id"].unique()]

    for game in game_list_from_site:
        if game["game_id"] in game_id_list_from_csv:
            game_df = df[df["game_id"] == game["game_id"]]

            for _, row in game_df.iterrows():
                players_stats_table.append(
                    {
                        "game_id": game["game_id"],
                        "timestamp": game["timestamp"],
                        "player_name": row["playerName"],
                        "player_team": row["playerType"],
                        "free_throw_attempt": row["1FT_A"],
                        "free_throw_made": row["1FT_M"],
                        "two_points_attempt": row["2PT_A"],
                        "two_points_made": row["2PT_M"],
                        "three_points_attempt": row["3PT_A"],
                        "three_points_made": row["3PT_M"],
                        "assists": row["AS"],
                        "steals": row["ST"],
                        "blocks": row["BS"],
                        "offensive_rebounds": row["OR"],
                        "defensive_rebounds": row["DR"],
                        "turnovers": row["TO"],
                        "total_points_scored": row["PTS"],
                    }
                )

    df = pd.DataFrame(players_stats_table)

    df = player_stats.calculate_offensive_contribution(df)

    df = player_stats.calculate_defensive_contribution(df)

    df = player_stats.calculate_rebounding_contribution(df)

    df = player_stats.calculate_playmaking_contribution(df)

    df = player_stats.calculate_player_valuation_score(df)

    print(df.info())

    save_df.to_csv(df, "./files/players_stats_table.csv")
