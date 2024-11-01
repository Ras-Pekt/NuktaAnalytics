#!/usr/bin/python3
import pandas as pd

from . import save_df


def populate_teams_table(allgames_csv, games_table_csv):
    games_table_df = pd.read_csv(games_table_csv)
    allgames_df = pd.read_csv(allgames_csv)

    teams_table = []
    for team in allgames_df["playerType"].unique():
        teams_table.append(
            {
                "team": team,
                "wins": games_table_df[games_table_df["winner"] == team].shape[0],
                "losses": games_table_df[games_table_df["loser"] == team].shape[0],
            }
        )
    df = pd.DataFrame(teams_table)

    print(df.info())

    save_df.to_csv(df, "./files/teams_table.csv")