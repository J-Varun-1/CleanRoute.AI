import os
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "indian_waste_data_v2.csv"
)


# =========================================================
# LOAD HISTORICAL DATA
# =========================================================

def load_historical_data():

    if not os.path.exists(DATA_PATH):

        raise FileNotFoundError(
            f"Historical dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(
        DATA_PATH
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    return df


# =========================================================
# GET DATA BEFORE TARGET DATE
# =========================================================

def get_history_for_bin(
    bin_id: str,
    target_date: str
):

    df = load_historical_data()

    target_date = pd.to_datetime(
        target_date
    )

    history = df[
        (df["bin_id"] == bin_id)
        &
        (df["date"] < target_date)
    ].copy()

    history = history.sort_values(
        "date"
    )

    return history