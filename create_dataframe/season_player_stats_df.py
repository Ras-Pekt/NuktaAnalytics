#!/usr/bin/python3
from base.base_class import BaseClass


class SeasonPlayerStats(BaseClass):
    __season_player_stats = []

    def __init__(self, df_name):
        """
        Initialize the SeasonPlayerStats class.

        Args:
            df (pd.DataFrame): DataFrame.
        """

        # super().__init__()
        self.df_name = df_name

    def get_season_player_stats(self):
        """
        Create the season player stats DataFrame.

        Returns:
            pd.DataFrame: The season player stats DataFrame.
        """

        instance_df = self.read_csv_util(self.df_name)

        if instance_df is None:
            return

        self.__season_player_stats = []

        for player_name in instance_df["player_name"].unique():
            player_df = instance_df[instance_df["player_name"] == player_name]

            if player_name[-1].isupper():
                player_name = f"{player_name[:-1]}.{player_name[-1]}"

            self.__season_player_stats.append(
                {
                    "season": "2024-2025",
                    "player_name": player_name,
                    "player_team": player_df["player_team"].iloc[0],
                    "total_games_played": player_df["game_id"].count(),
                    "total_free_throws_attempts": player_df["free_throw_attempt"].sum(),
                    "total_free_throws_made": player_df["free_throw_made"].sum(),
                    "total_two_points_attempt": player_df["two_points_attempt"].sum(),
                    "total_two_points_made": player_df["two_points_made"].sum(),
                    "total_three_points_attempt": player_df[
                        "three_points_attempt"
                    ].sum(),
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
                    "average_rebound_percentage": player_df[
                        "rebound_percentage"
                    ].mean(),
                    "average_playmaking_contribution": player_df["playmaking"].mean(),
                    "average_player_valuation_score": player_df[
                        "player_valuation_score"
                    ].mean(),
                }
            )
        return self.to_df(self.__season_player_stats)

    def save_to_csv(self, filename=None):
        """
        Save the season player stats DataFrame to a CSV file.

        Args:
            path (str): The path to save the CSV file.
        """
        if self.__season_player_stats is None:
            return
        df = self.to_df(self.__season_player_stats)
        self.to_csv(df, filename)
