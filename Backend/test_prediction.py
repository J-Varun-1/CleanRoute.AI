from service.prediction_features import (
    build_prediction_features
)

from ml.predictor import predict


BIN_ID = "BIN_001"

TARGET_DATE = "2025-10-20"


print("\n==============================")
print("BUILDING FEATURES")
print("==============================")

X = build_prediction_features(
    BIN_ID,
    TARGET_DATE
)


print(
    "Shape:",
    X.shape
)


print(
    "\nColumns:"
)

for i, col in enumerate(
    X.columns,
    1
):

    print(
        i,
        col
    )


print("\n==============================")
print("PREDICTING")
print("==============================")


result = predict(
    X
)


print(
    "\nRESULT:"
)

print(
    result
)