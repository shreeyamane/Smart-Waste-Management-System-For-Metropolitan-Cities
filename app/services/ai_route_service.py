from sqlalchemy.orm import Session

from app.models.bin import Bin
from app.models.sensor_data import SensorData

from app.ml.predictor import predict_time_to_full


def get_ai_priority_bins(db: Session):

    bins = db.query(Bin).all()

    results = []

    for b in bins:

        readings = (
            db.query(SensorData)
            .filter(
                SensorData.bin_id == b.id
            )
            .order_by(
                SensorData.timestamp.desc()
            )
            .limit(2)
            .all()
        )

        if len(readings) < 2:
            continue

        latest = readings[0]
        previous = readings[1]

        fill_rate = (
            latest.fill_level -
            previous.fill_level
        )

        fill_rate = max(fill_rate, 1)

        predicted_hours = predict_time_to_full(
            latest.fill_level,
            latest.temperature,
            latest.humidity,
            fill_rate
        )

        overflow_risk = min(
            100,
            round(
                latest.fill_level * 0.7 +
                fill_rate * 3,
                2
            )
        )

        battery_risk = (
            100 - b.battery
        )

        priority_score = round(

            latest.fill_level * 0.5 +

            overflow_risk * 0.3 +

            battery_risk * 0.2,

            2
        )

        urgency_score = max(
            0,
            100 - predicted_hours
        )

        route_score = round(

            priority_score * 0.4 +

            overflow_risk * 0.3 +

            latest.fill_level * 0.2 +

            urgency_score * 0.1,

            2
        )

        results.append({

            "bin": b,

            "fill_level": latest.fill_level,

            "overflow_risk": overflow_risk,

            "predicted_hours": predicted_hours,

            "priority_score": priority_score,

            "route_score": route_score

        })

    results.sort(
        key=lambda x: x["route_score"],
        reverse=True
    )

    return results