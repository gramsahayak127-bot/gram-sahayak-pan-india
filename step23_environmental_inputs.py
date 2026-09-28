import os
import pandas as pd


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

LOOKUP_PATH = os.path.join(
    SCRIPT_DIR,
    "outputs",
    "environmental_lookup.csv"
)


# ---------------------------------------------------------
# LOAD MODEL-COMPATIBLE ENVIRONMENTAL LOOKUP
# ---------------------------------------------------------

print("Loading model-compatible environmental lookup...")

environmental_df = pd.read_csv(LOOKUP_PATH)

environmental_df["State_Name"] = (
    environmental_df["State_Name"]
    .astype(str)
    .str.strip()
    .str.lower()
)

environmental_df["Crop_Type"] = (
    environmental_df["Crop_Type"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# ---------------------------------------------------------
# ENVIRONMENTAL INPUT FUNCTION
# ---------------------------------------------------------

def get_environmental_inputs(state, crop_type):

    state = str(state).strip().lower()
    crop_type = str(crop_type).strip().lower()

    result = environmental_df[
        (environmental_df["State_Name"] == state) &
        (environmental_df["Crop_Type"] == crop_type)
    ]

    if result.empty:
        raise ValueError(
            f"No environmental data found for "
            f"state='{state}', crop_type='{crop_type}'"
        )

    row = result.iloc[0]

    return {
        "state": state,
        "crop_type": crop_type,
        "rainfall": float(row["rainfall"]),
        "temperature": float(row["temperature"])
    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("\nTesting environmental input system...\n")

    test_cases = [
        ("karnataka", "kharif"),
        ("karnataka", "rabi"),
        ("karnataka", "summer"),
        ("andhra pradesh", "kharif"),
    ]

    for state, crop_type in test_cases:

        try:
            result = get_environmental_inputs(
                state,
                crop_type
            )

            print(result)

        except ValueError as e:
            print("ERROR:", e)