import joblib
import pandas as pd

MODEL_PATH = "app/ml/waste_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_time_to_full(
    fill_level,
    temperature,
    humidity,
    fill_rate
):

    data = pd.DataFrame([{
        "fill_level": fill_level,
        "temperature": temperature,
        "humidity": humidity,
        "fill_rate": fill_rate,
        "hour": 12,
        "day": 1
    }])

    prediction = model.predict(data)

    return round(
        float(prediction[0]),
        2
    )