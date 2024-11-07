#!/usr/bin/python3
# def main():
#     all_games_json = "./files/all_games.json"
#     allgames_csv = "./files/allgames.csv"
#     games_table_csv = "./files/games_table.csv"
#     players_stats_table_csv = "./files/players_stats_table.csv"

#     # games_table.csv - populate_games_table.py
#     populate_games_table.populate_games_table(all_games_json, allgames_csv)

#     # teams_table.csv - populate_teams_table.py
#     populate_teams_table.populate_teams_table(allgames_csv, games_table_csv)

#     # players_stats_table.csv - populate_player_stats_table.py
#     populate_player_stats_table.populate_player_stats_table(
#         all_games_json, allgames_csv
#     )

#     # teams_stats_table.csv - populate_team_stats_table.py
#     populate_team_stats_table.populate_team_stats_table(all_games_json, allgames_csv)

#     # season_player_stats_table.csv - populate_season_player_stats_table.py
#     populate_season_player_stats_table.populate_season_player_stats_table(
#         players_stats_table_csv
#     )


if __name__ == "__main__":
    # from create_csv import (
    #     populate_games_table,
    #     populate_player_stats_table,
    #     populate_season_player_stats_table,
    #     populate_team_stats_table,
    #     populate_teams_table,
    # )

    # main()
    from create_dataframe.season_player_stats_df import SeasonPlayerStats

    # TODO: read df instead of csv
    df_obj = SeasonPlayerStats("./files/players_stats_table.csv")
    df = df_obj.get_season_player_stats()

    print(df.info())
    print()
    print(df.head(25))

    df_obj.save_to_csv("./files/season_player_stats.csv")
