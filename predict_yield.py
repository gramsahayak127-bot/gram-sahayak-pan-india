import os
import joblib
import pandas as pd

from step23_environmental_inputs import get_environmental_inputs


# ============================================================
# PATH SETUP
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Deployment-sized model created from cleaned_crop_dataset.csv.
# The original models/yield_model.pkl is intentionally left untouched.
MODEL_PATH = os.path.join(
    SCRIPT_DIR,
    "models",
    "yield_model_deployment.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading deployment yield model...")

model = joblib.load(MODEL_PATH)

print("Deployment yield model loaded successfully.")


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_yield(
    state,
    crop_type,
    crop,
    area_in_hectares
):
    """
    Predict crop yield and total production.

    Inputs:
        state              : State name
        crop_type          : kharif / rabi / summer / whole year
        crop               : Crop name
        area_in_hectares   : Farm area in hectares

    Returns:
        Dictionary containing environmental inputs,
        predicted yield and predicted production.
    """

    # --------------------------------------------------------
    # Validate area
    # --------------------------------------------------------

    area_in_hectares = float(area_in_hectares)

    if area_in_hectares <= 0:
        raise ValueError("Area must be greater than 0 hectares.")

    # --------------------------------------------------------
    # Get automatic rainfall + temperature
    # --------------------------------------------------------

    environmental = get_environmental_inputs(
        state,
        crop_type
    )

    rainfall = float(environmental["rainfall"])
    temperature = float(environmental["temperature"])

    # --------------------------------------------------------
    # Create model input
    #
    # The deployment model is a complete sklearn Pipeline.
    # It performs its own OneHotEncoder preprocessing.
    # Its training features are exactly:
    # State_Name, Crop_Type, Crop, rainfall,
    # temperature, Area_in_hectares
    # --------------------------------------------------------

    input_data = pd.DataFrame({
        "State_Name": [state],
        "Crop_Type": [crop_type],
        "Crop": [crop],
        "rainfall": [rainfall],
        "temperature": [temperature],
        "Area_in_hectares": [area_in_hectares],
    })

    # --------------------------------------------------------
    # Predict yield directly.
    #
    # The new deployment model was trained on
    # Yield_ton_per_hec directly, so there is NO log1p/
    # expm1 conversion here.
    # --------------------------------------------------------

    predicted_yield = float(model.predict(input_data)[0])

    # Prevent negative prediction.
    predicted_yield = max(predicted_yield, 0.0)

    # --------------------------------------------------------
    # Calculate total production
    # --------------------------------------------------------

    predicted_production = (
        predicted_yield * area_in_hectares
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "state": environmental["state"],
        "crop_type": environmental["crop_type"],
        "crop": crop,
        "area_in_hectares": area_in_hectares,
        "rainfall": rainfall,
        "temperature": temperature,
        "predicted_yield_ton_per_hectare": predicted_yield,
        "predicted_production_tons": predicted_production
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 65)
    print("       GRAM SAHAYAK - YIELD PREDICTION TEST")
    print("=" * 65)

    result = predict_yield(
        state="andhra pradesh",
        crop_type="kharif",
        crop="Arhar/Tur",
        area_in_hectares=2
    )

    print("\nPrediction result:")
    print("-" * 65)

    for key, value in result.items():

        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")

    print("-" * 65)
    print("Prediction completed successfully.")
