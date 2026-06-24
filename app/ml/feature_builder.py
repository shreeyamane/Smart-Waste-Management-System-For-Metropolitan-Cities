import pandas as pd


def create_features(df):

    df = df.sort_values(
        ["bin_id", "timestamp"]
    )

    df["previous_fill"] = (
        df.groupby("bin_id")["fill_level"]
        .shift(1)
    )

    df["fill_rate"] = (
        df["fill_level"] -
        df["previous_fill"]
    )

    df["hour"] = (
        pd.to_datetime(df["timestamp"])
        .dt.hour
    )

    df["day"] = (
        pd.to_datetime(df["timestamp"])
        .dt.dayofweek
    )

    return df