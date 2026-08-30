import os
import joblib


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

preprocessor_path = os.path.join(
    BASE_DIR,
    "ml",
    "random_forest_preprocessor.pkl"
)

preprocessor = joblib.load(
    preprocessor_path
)


print("\n==============================")
print("PREPROCESSOR INPUT FEATURES")
print("==============================\n")


print(
    "Number of features:",
    len(preprocessor.feature_names_in_)
)


for i, feature in enumerate(
    preprocessor.feature_names_in_,
    start=1
):

    print(
        f"{i}. {feature}"
    )


print("\n==============================")