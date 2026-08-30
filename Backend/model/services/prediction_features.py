import pandas as pd
import numpy as np

from ml.feature_engineering import create_features
from service.historical_service import get_history_for_bin
from service.bin_metadata import BIN_METADATA
from data.festival import get_festival_info


# =========================================================
# BUILD FEATURES FOR ONE PREDICTION
# =========================================================

def build_prediction_features(
    bin_id: str,
    target_date: str
):

    # =====================================================
    # 1. CHECK BIN
    # =====================================================

    if bin_id not in BIN_METADATA:
        raise ValueError(
            f"Unknown bin: {bin_id}"
        )

    metadata = BIN_METADATA[bin_id]


    # =====================================================
    # 2. GET HISTORICAL DATA
    # =====================================================

    history = get_history_for_bin(
        bin_id,
        target_date
    )

    if history.empty:
        raise ValueError(
            f"No historical data found for {bin_id}"
        )

    history = history.copy()

    history["date"] = pd.to_datetime(
        history["date"]
    )

    history = history.sort_values(
        "date"
    ).reset_index(drop=True)


    # =====================================================
    # 3. DATE + FESTIVAL
    # =====================================================

    target_date_obj = pd.to_datetime(
        target_date
    )

    festival = get_festival_info(
        target_date
    )

    print("\n==============================")
    print("FESTIVAL DEBUG")
    print("==============================")
    print("Target date:", target_date)
    print("Festival:", festival)
    print("Festival name:", festival.get("name"))
    print("Major:", festival.get("major"))
    print("==============================\n")

    festival_name = festival["name"]
    is_major_festival = int(
        festival["major"]
    )

    is_factory_closed = 0

    if (
        metadata["area_type"]
        == "Industrial/Manufacturing"
        and is_major_festival == 1
    ):
        is_factory_closed = 1


    # =====================================================
    # 4. CREATE TARGET ROW
    # =====================================================

    target_row = pd.DataFrame([{

        "date": target_date_obj,

        "bin_id": bin_id,

        "area_type":
            metadata["area_type"],

        "population_density":
            metadata["population_density"],

        "fill_percentage": np.nan,

        "wet_waste_pct": np.nan,

        "dry_waste_pct": np.nan
    }])


    # =====================================================
    # 5. COMBINE HISTORY + TARGET
    # =====================================================

    data = pd.concat(
        [
            history,
            target_row
        ],
        ignore_index=True
    )

    data = data.sort_values(
        "date"
    ).reset_index(drop=True)


    # =====================================================
    # 6. FEATURE ENGINEERING
    # =====================================================

    data = create_features(
        data
    )


    # =====================================================
    # 7. GET TARGET ROW
    # =====================================================

    target_rows = data[
        data["date"] == target_date_obj
    ]

    if target_rows.empty:
        raise ValueError(
            f"Target date {target_date} not found"
        )

    prediction_row = (
        target_rows.iloc[-1].copy()
    )


    # =====================================================
    # 8. USE LATEST KNOWN WET/DRY VALUES
    # =====================================================

    latest = (
        history
        .sort_values("date")
        .iloc[-1]
    )

    prediction_row["wet_waste_pct"] = float(
        latest["wet_waste_pct"]
    )

    prediction_row["dry_waste_pct"] = float(
        latest["dry_waste_pct"]
    )


    # =====================================================
    # 9. ADD FESTIVAL FEATURES EXPLICITLY
    # =====================================================

    prediction_row["festival_name"] = (
        festival_name
    )

    prediction_row["is_major_festival"] = (
        is_major_festival
    )

    prediction_row["is_factory_closed"] = (
        is_factory_closed
    )


    # =====================================================
    # 10. REQUIRED MODEL FEATURES
    # =====================================================

    required_features = [

        "bin_id",
        "area_type",
        "population_density",

        "day",
        "month",
        "day_of_year",
        "week_of_year",

        "weekday",
        "is_weekend",

        "day_sin",
        "day_cos",

        "month_sin",
        "month_cos",

        "festival_name",
        "is_major_festival",
        "is_factory_closed",

        "wet_waste_pct",
        "dry_waste_pct",

        "fill_lag_1",
        "fill_lag_2",
        "fill_lag_3",
        "fill_lag_7",
        "fill_lag_14",
        "fill_lag_30",

        "fill_rolling_3",
        "fill_rolling_7",
        "fill_rolling_14",

        "wet_lag_1",
        "wet_lag_2",
        "wet_lag_3",
        "wet_lag_7",
        "wet_lag_14",
        "wet_lag_30",

        "wet_rolling_3",
        "wet_rolling_7",
        "wet_rolling_14",

        "dry_lag_1",
        "dry_lag_2",
        "dry_lag_3",
        "dry_lag_7",
        "dry_lag_14",
        "dry_lag_30",

        "dry_rolling_3",
        "dry_rolling_7",
        "dry_rolling_14"
    ]


    # =====================================================
    # 11. CHECK COLUMNS BEFORE SELECTING
    # =====================================================

    missing_columns = [
        col
        for col in required_features
        if col not in prediction_row.index
    ]

    if missing_columns:

        raise ValueError(
            "Missing model columns: "
            + str(missing_columns)
        )


    # =====================================================
    # 12. BUILD FINAL DATAFRAME
    # =====================================================

    X = pd.DataFrame(
        [prediction_row]
    )

    X = X[
        required_features
    ].copy()


    # =====================================================
    # 13. CHECK NaN
    # =====================================================

    missing_values = (
        X.columns[
            X.isna().any()
        ].tolist()
    )

    if missing_values:

        raise ValueError(
            "Missing model feature values: "
            + str(missing_values)
        )


    # =====================================================
    # 14. RETURN
    # =====================================================

    return X