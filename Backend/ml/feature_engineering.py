import pandas as pd
import numpy as np


TARGET_COLUMNS = [
    "fill_percentage",
    "wet_waste_pct",
    "dry_waste_pct"
]


# =========================================================
# 1. DATE FEATURES
# =========================================================

def create_date_features(df):

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month
    df["day_of_year"] = df["date"].dt.dayofyear

    df["week_of_year"] = (
        df["date"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    df["weekday"] = df["date"].dt.strftime("%A")

    df["is_weekend"] = (
        df["date"]
        .dt.dayofweek >= 5
    ).astype(int)

    # -------------------------
    # Cyclic features
    # -------------------------

    df["day_sin"] = np.sin(
        2 * np.pi * df["day_of_year"] / 365
    )

    df["day_cos"] = np.cos(
        2 * np.pi * df["day_of_year"] / 365
    )

    df["month_sin"] = np.sin(
        2 * np.pi * df["month"] / 12
    )

    df["month_cos"] = np.cos(
        2 * np.pi * df["month"] / 12
    )

    return df


# =========================================================
# 2. LAG FEATURES
# =========================================================

def create_lag_features(df):

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    # VERY IMPORTANT
    # Each bin must have its own history

    df = df.sort_values(
        ["bin_id", "date"]
    )

    lag_values = [1, 2, 3, 7, 14, 30]

    for lag in lag_values:

        df[f"fill_lag_{lag}"] = (
            df.groupby("bin_id")["fill_percentage"]
            .shift(lag)
        )

        df[f"wet_lag_{lag}"] = (
            df.groupby("bin_id")["wet_waste_pct"]
            .shift(lag)
        )

        df[f"dry_lag_{lag}"] = (
            df.groupby("bin_id")["dry_waste_pct"]
            .shift(lag)
        )

    return df


# =========================================================
# 3. ROLLING FEATURES
# =========================================================

def create_rolling_features(df):

    df = df.copy()

    df = df.sort_values(
        ["bin_id", "date"]
    )

    windows = [3, 7, 14]

    for window in windows:

        # shift(1) is VERY IMPORTANT.
        #
        # It prevents today's value from entering
        # today's rolling feature.

        df[f"fill_rolling_{window}"] = (
            df.groupby("bin_id")["fill_percentage"]
            .transform(
                lambda x:
                x.shift(1)
                 .rolling(window)
                 .mean()
            )
        )

        df[f"wet_rolling_{window}"] = (
            df.groupby("bin_id")["wet_waste_pct"]
            .transform(
                lambda x:
                x.shift(1)
                 .rolling(window)
                 .mean()
            )
        )

        df[f"dry_rolling_{window}"] = (
            df.groupby("bin_id")["dry_waste_pct"]
            .transform(
                lambda x:
                x.shift(1)
                 .rolling(window)
                 .mean()
            )
        )

    return df


# =========================================================
# 4. COMPLETE FEATURE ENGINEERING
# =========================================================

def create_features(df):

    df = create_date_features(df)

    df = create_lag_features(df)

    df = create_rolling_features(df)

    return df