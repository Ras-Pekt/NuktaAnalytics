#!/usr/bin/python3


def calculate_offensive_contribution(df):
    # Effective Field Goal Percentage (eFG%)
    df["eFG"] = (
        (
            (
                (df["two_points_made"] + df["three_points_made"])
                + 0.5 * df["three_points_made"]
            )
            / (df["two_points_attempt"] + df["three_points_attempt"])
        )
        * 100
    ).round(4)

    # True Shooting Percentage (TS%)
    df["TS"] = (
        (
            df["total_points_scored"]
            / (
                2
                * (
                    (df["two_points_attempt"] + df["three_points_attempt"])
                    + (0.44 * df["free_throw_attempt"])
                )
            )
        )
        * 100
    ).round(4)

    # Points Per Shot (PPS)
    df["PPS"] = (
        df["total_points_scored"]
        / (df["two_points_attempt"] + df["three_points_attempt"])
    ).round(4)

    # Offensive Contribution
    df["offensive_contribution"] = (
        (0.4 * df["eFG"]) + (0.4 * df["TS"]) + (0.2 * df["PPS"])
    ).round(4)

    return df


def calculate_defensive_contribution(df):
    # Group by game_id (this will give all players who played in a particular game)
    # Within each game, group by team (player_team column in this case)
    # Aggregate team-level stats like total points and possessions for each team in each game

    # Define the team-level stats to aggregate
    team_stats = (
        df.groupby(["game_id", "player_team"])
        .agg(
            total_points=("total_points_scored", "sum"),
            total_two_points_attempt=("two_points_attempt", "sum"),
            total_three_points_attempt=("three_points_attempt", "sum"),
            total_FTA=("free_throw_attempt", "sum"),
            total_OR=("offensive_rebounds", "sum"),
            total_TO=("turnovers", "sum"),
        )
        .reset_index()
    )

    # Calculate the total field goal attemtotal_points_scored (FGA) by adding the 2PT and 3PT attemtotal_points_scored
    team_stats["total_FGA"] = (
        team_stats["total_two_points_attempt"]
        + team_stats["total_three_points_attempt"]
    )

    # Calculate possessions for each team in each game using the possession formula
    team_stats["possessions"] = (
        team_stats["total_FGA"]
        + 0.44 * team_stats["total_FTA"]
        - team_stats["total_OR"]
        + team_stats["total_TO"]
    )

    # Calculate opponent points and possessions
    # First calculate opponent points using the shifted values
    team_stats["opponent_points"] = team_stats.groupby("game_id")["total_points"].shift(
        1
    )
    team_stats["opponent_points"] = team_stats["opponent_points"].fillna(
        team_stats.groupby("game_id")["total_points"].shift(-1)
    )

    # Calculate opponent possessions
    team_stats["opponent_possessions"] = team_stats.groupby("game_id")[
        "possessions"
    ].shift(1)
    team_stats["opponent_possessions"] = team_stats["opponent_possessions"].fillna(
        team_stats.groupby("game_id")["possessions"].shift(-1)
    )

    # Merge the team-level stats back with the original player data
    df = df.merge(
        team_stats[
            ["game_id", "player_team", "opponent_points", "opponent_possessions"]
        ],
        on=["game_id", "player_team"],
        how="left",
    )

    # Calculate Defensive Rating (DRtg)
    df["defensive_contribution"] = (
        100 * (df["opponent_points"] / df["opponent_possessions"])
    ).round(4)

    return df


def calculate_playmaking_contribution(df):
    # Calculate assist-to-Turnover Ratio (AS/TO)
    # df['AS/TO'] = df['AS'] / df['TO']
    df["playmaking"] = df["assists"] / df["turnovers"]
    return df


def calculate_rebounding_contribution(df):
    # # Calculate Total Rebounds (TOT) for each player
    # # Total Rebounds = Offensive Rebounds + Defensive Rebounds
    # df["TOT"] = (df["offensive_contribution"] + df["defensive_contribution"]).round(4)

    # # Calculate Total Rebounds in each Game
    # # Aggregate the rebounds for each game
    # total_rebounds_per_game = (
    #     df.groupby("game_id").agg(total_rebounds=("TOT", "sum")).reset_index()
    # )

    # # Step 3: Merge Total Rebounds in Game back to the original DataFrame
    # df = df.merge(total_rebounds_per_game, on="game_id", how="left")

    # # Calculate Rebound Percentage (Reb%)
    # df["rebound_percentage"] = (df["TOT"] / df["total_rebounds"]).round(4)

    df["player_total_rebounds"] = df["offensive_rebounds"] + df["defensive_rebounds"]
    df["game_total_rebounds"] = df.groupby("game_id")[
        "player_total_rebounds"
    ].transform("sum")

    return df


def calculate_player_valuation_score(df):
    # Calculate Player Valuation Score for each player
    df["player_valuation_score"] = (
        0.35 * df["offensive_contribution"]
        + 0.25 * df["defensive_contribution"]
        + 0.20 * df["rebound_percentage"]
        + 0.10 * df["playmaking"]
    ).round(4)

    return df
