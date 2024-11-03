#!/usr/bin/python3
import pandas as pd

# import json
from . import save_df


def populate_season_player_stats_table(players_stats_table_csv):
    # Get each player's stats over the entire season
    df = pd.read_csv(players_stats_table_csv)
    df["player_team"] = df["player_team"].str.lower()
    df["player_name"] = (
        df["player_name"].str.replace(".", "").str.replace(",", "").str.replace(" ", "")
    )

    # Replace inf values with NaN
    df.replace([float("inf"), -float("inf")], pd.NA, inplace=True)

    season_player_stats = []

    for player_name in df["player_name"].unique():
        player_df = df[df["player_name"] == player_name]

        if player_name[-1].isupper():
            player_name = f"{player_name[:-1]}.{player_name[-1]}"

        season_player_stats.append(
            {
                "season": "2024-2025",
                "player_name": player_name,
                "player_team": player_df["player_team"].iloc[0],
                "total_games_played": player_df["game_id"].count(),
                "total_free_throws_attempts": player_df["free_throw_attempt"].sum(),
                "total_free_throws_made": player_df["free_throw_made"].sum(),
                "total_two_points_attempt": player_df["two_points_attempt"].sum(),
                "total_two_points_made": player_df["two_points_made"].sum(),
                "total_three_points_attempt": player_df["three_points_attempt"].sum(),
                "total_three_points_made": player_df["three_points_made"].sum(),
                "total_assists": player_df["assists"].sum(),
                "total_steals": player_df["steals"].sum(),
                "total_blocks": player_df["blocks"].sum(),
                "total_offensive_rebounds": player_df["offensive_rebounds"].sum(),
                "total_defensive_rebounds": player_df["defensive_rebounds"].sum(),
                "total_turnovers": player_df["turnovers"].sum(),
                "total_points_scored": player_df["total_points_scored"].sum(),
                "average_eFG": player_df["eFG"].mean(),
                "average_TS": player_df["TS"].mean(),
                "average_PPS": player_df["PPS"].mean(),
                "average_offensive_contribution": player_df[
                    "offensive_contribution"
                ].mean(),
                "average_defensive_contribution": player_df[
                    "defensive_contribution"
                ].mean(),
                "average_rebound_percentage": player_df["rebound_percentage"].mean(),
                "average_playmaking_contribution": player_df["playmaking"].mean(),
                "average_player_valuation_score": player_df[
                    "player_valuation_score"
                ].mean(),
            }
        )

    # Convert teams_stats_table list of DataFrames to one DataFrame
    season_player_stats_df = pd.DataFrame(season_player_stats)

    # round to 4 decimal places
    season_player_stats_df[
        [
            "average_eFG",
            "average_TS",
            "average_PPS",
            "average_offensive_contribution",
            "average_defensive_contribution",
            "average_rebound_percentage",
            "average_playmaking_contribution",
            "average_player_valuation_score",
        ]
    ] = season_player_stats_df[
        [
            "average_eFG",
            "average_TS",
            "average_PPS",
            "average_offensive_contribution",
            "average_defensive_contribution",
            "average_rebound_percentage",
            "average_playmaking_contribution",
            "average_player_valuation_score",
        ]
    ].round(4)

    print(season_player_stats_df.info())

    # Save the DataFrame to a CSV file
    save_df.to_csv(season_player_stats_df, "./files/season_player_stats_table.csv")
