import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor

from sqlalchemy import create_engine

from app.core.config import DATABASE_URL
from app.ml.feature_builder import create_features


engine = create_engine(DATABASE_URL)

query = """
SELECT
    bin_id,
    fill_level,
    temperature,
    humidity,
    timestamp
FROM sensor_data
"""

df = pd.read_sql(query, engine)

df = create_features(df)

df = df.dropna()

df["hours_to_full"] = (
    (100 - df["fill_level"])
    /
    df["fill_rate"].clip(lower=1)
)

features = [
    "fill_level",
    "temperature",
    "humidity",
    "fill_rate",
    "hour",
    "day"
]

X = df[features]

y = df["hours_to_full"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(
    model,
    "app/ml/waste_model.pkl"
)

print("Model trained successfully")