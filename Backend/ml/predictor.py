import os
import joblib
import pandas as pd


# =========================================================
# PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# =========================================================
# LOAD TRAINED MODELS
# =========================================================

fill_model = joblib.load(
    os.path.join(
        BASE_DIR,
        "random_forest_fill.pkl"
    )
)

wet_model = joblib.load(
    os.path.join(
        BASE_DIR,
        "random_forest_wet.pkl"
    )
)

dry_model = joblib.load(
    os.path.join(
        BASE_DIR,
        "random_forest_dry.pkl"
    )
)

preprocessor = joblib.load(
    os.path.join(
        BASE_DIR,
        "random_forest_preprocessor.pkl"
    )
)


# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict(features):

    # -----------------------------------------------------
    # build_prediction_features()
    # already returns a DataFrame
    # -----------------------------------------------------

    if isinstance(features, pd.DataFrame):

        X = features.copy()

    else:

        X = pd.DataFrame(
            [features]
        )


    # -----------------------------------------------------
    # GET FEATURES USED DURING TRAINING
    # -----------------------------------------------------

    expected_columns = list(
        preprocessor.feature_names_in_
    )


    # -----------------------------------------------------
    # CHECK MISSING FEATURES
    # -----------------------------------------------------

    missing_columns = [
        column
        for column in expected_columns
        if column not in X.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing features: {missing_columns}"
        )


    # -----------------------------------------------------
    # KEEP EXACT SAME COLUMN ORDER
    # AS TRAINING
    # -----------------------------------------------------

    X = X[
        expected_columns
    ]


    # -----------------------------------------------------
    # PREPROCESS FEATURES
    # -----------------------------------------------------

    X_processed = preprocessor.transform(
        X
    )


    # -----------------------------------------------------
    # PREDICTIONS
    # -----------------------------------------------------

    fill_prediction = fill_model.predict(
        X_processed
    )[0]

    wet_prediction = wet_model.predict(
        X_processed
    )[0]

    dry_prediction = dry_model.predict(
        X_processed
    )[0]


    # -----------------------------------------------------
    # KEEP PERCENTAGES BETWEEN 0 AND 100
    # -----------------------------------------------------

    fill_prediction = max(
        0,
        min(
            100,
            float(fill_prediction)
        )
    )

    wet_prediction = max(
        0,
        min(
            100,
            float(wet_prediction)
        )
    )

    dry_prediction = max(
        0,
        min(
            100,
            float(dry_prediction)
        )
    )


    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return {

        "fill_percentage":
            round(
                fill_prediction,
                2
            ),

        "wet_waste_pct":
            round(
                wet_prediction,
                2
            ),

        "dry_waste_pct":
            round(
                dry_prediction,
                2
            )
    }