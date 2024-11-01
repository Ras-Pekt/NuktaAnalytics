#!/usr/bin/python3
import json
import os

import pandas as pd

from . import games, save_df


def populate_team_stats_table(all_games_json, allgames_csv):
    # Call the get_games function to save the data to a file
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

    teams_stats_table = []

    # Create a player stats table with all relevant fields
    for game in game_list_from_site:
        if game["game_id"] in game_id_list_from_csv:
            # Filter the DataFrame for the current game
            game_df = df[df["game_id"] == game["game_id"]]

            # Group by playerType (team) and calculate the total stats for each team
            team_ft_totals = game_df.groupby("playerType")[
                [
                    "1FT_A",
                    "1FT_M",
                    "2PT_A",
                    "2PT_M",
                    "3PT_M",
                    "3PT_A",
                    "AS",
                    "OR",
                    "DR",
                    "TO",
                    "PTS",
                ]
            ].sum()

            # Rename the columns as needed
            team_ft_totals = team_ft_totals.rename(
                columns={
                    "1FT_A": "total_free_throw_attempts",
                    "1FT_M": "total_free_throw_made",
                    "2PT_A": "total_two_point_attempts",
                    "2PT_M": "total_two_point_made",
                    "3PT_A": "total_three_point_attempts",
                    "3PT_M": "total_three_point_made",
                    "AS": "total_assists",
                    "OR": "total_offensive_rebounds",
                    "DR": "total_defensive_rebounds",
                    "TO": "total_turnovers",
                    "PTS": "total_points",
                }
            )

            # Add the game_id and timestamp to the DataFrame
            team_ft_totals["game_id"] = game["game_id"]
            team_ft_totals["timestamp"] = game["timestamp"]

            # Reset the index to make 'playerType' a column
            team_ft_totals = team_ft_totals.reset_index().rename(
                columns={"playerType": "team"}
            )

            teams_stats_table.append(team_ft_totals)

    # Convert teams_stats_table list of DataFrames to one DataFrame
    df = pd.concat(teams_stats_table, ignore_index=True)
    print(df.info())

    # Save the DataFrame to a CSV file
    save_df.to_csv(df, "./files/teams_stats_table.csv")
