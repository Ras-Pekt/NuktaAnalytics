#!/usr/bin/python3
import os

import pandas as pd


class BaseClass:
    # def __init__(self):
    #     pass

    def read_csv_util(self, file_path, df_class=None):
        """
        Read a CSV file and return a DataFrame.

        Args:
            file_path (str): The path to the CSV file.
            df_class (class): The class to load dependant DataFrame if not present
        Returns:
            pd.DataFrame: The DataFrame.
        """

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            # TODO: call respective class to create the dataframe
            # pass it as args (PlayerGameStats, etc class)

            print(f"Error: File '{file_path}' not found.")
            return None

        df["player_team"] = df["player_team"].str.lower()
        df["player_name"] = (
            df["player_name"]
            .str.replace(".", "")
            .str.replace(",", "")
            .str.replace(" ", "")
        )

        # Replace inf values with NaN
        df.replace([float("inf"), -float("inf")], pd.NA, inplace=True)

        # Replace NaN and NA values with 0 and infer types explicitly
        with pd.option_context("future.no_silent_downcasting", True):
            df = df.fillna(0)

        return df

    def to_df(self, obj):
        """
        Convert an object to a DataFrame.

        Args:
            obj (object): The object to convert.
        Returns:
            pd.DataFrame: The DataFrame.
        """

        if isinstance(obj, pd.DataFrame):
            return obj
        elif isinstance(obj, list):
            return pd.DataFrame(obj)
        else:
            return None

    def to_csv(self, df, filename):
        """
        Save a DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): The DataFrame.
            filename (str): The filename.
        """
        if filename is None:
            filename = "output.csv"
        df.to_csv(filename, index=False)
