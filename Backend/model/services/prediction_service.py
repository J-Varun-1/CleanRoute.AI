from ml.predictor import predict

from service.prediction_features import (
    build_prediction_features
)


def generate_prediction(
    bin_id: str,
    target_date: str
):

    # ==========================================
    # BUILD EXACT 45 FEATURES
    # ==========================================

    features = build_prediction_features(
        bin_id,
        target_date
    )

    # ==========================================
    # ML PREDICTION
    # ==========================================

    result = predict(features)

    return result


def predict_bin(
    bin_id: str,
    target_date: str
):

    result = generate_prediction(
        bin_id,
        target_date
    )

    # Your actual ML output:
    # {
    #     "fill_percentage": 55.24,
    #     "wet_waste_pct": 64.56,
    #     "dry_waste_pct": 35.41
    # }

    return {
        "bin_id": bin_id,
        "date": target_date,

        "fill": float(
            result["fill_percentage"]
        ),

        "wet": float(
            result["wet_waste_pct"]
        ),

        "dry": float(
            result["dry_waste_pct"]
        )
    }