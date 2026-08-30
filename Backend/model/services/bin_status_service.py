from data.virtual_city import VIRTUAL_BINS
from service.prediction_features import build_prediction_features
from ml.predictor import predict


def get_bin_status(bin_data, date):

    features = build_prediction_features(
        bin_id=bin_data["bin_id"],
        target_date=date
    )

    prediction = predict(features)

    fill = prediction["fill_percentage"]

    if fill >= 80:
        status = "critical"

    elif fill >= 60:
        status = "high"

    elif fill >= 40:
        status = "medium"

    else:
        status = "low"

    return {
        "bin_id": bin_data["bin_id"],
        "area": bin_data["area"],
        "latitude": bin_data["latitude"],
        "longitude": bin_data["longitude"],

        "fill_percentage": fill,
        "wet_waste_pct": prediction["wet_waste_pct"],
        "dry_waste_pct": prediction["dry_waste_pct"],

        "status": status
    }


def get_all_bin_status(date):

    result = []

    for bin_data in VIRTUAL_BINS:

        result.append(
            get_bin_status(
                bin_data,
                date
            )
        )

    return result