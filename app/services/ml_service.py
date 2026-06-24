from sqlalchemy.orm import Session

from app.models.bin import Bin
from app.models.sensor_data import SensorData

from app.ml.predictor import predict_time_to_full


def calculate_overflow_risk(
    fill_level,
    fill_rate
):

    risk = (
        fill_level * 0.7
        +
        fill_rate * 3
    )

    return round(
        min(100, max(0, risk)),
        2
    )


def calculate_priority(
    fill_level,
    overflow_risk,
    battery
):

    battery_risk = 100 - battery

    score = (

        fill_level * 0.5

        +

        overflow_risk * 0.3

        +

        battery_risk * 0.2

    )

    return round(score, 2)


def get_predictions(db: Session):

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

            latest.fill_level
            -
            previous.fill_level

        )

        fill_rate = max(
            fill_rate,
            1
        )

        hours = predict_time_to_full(
            latest.fill_level,
            latest.temperature,
            latest.humidity,
            fill_rate
        )

        overflow_risk = (
            calculate_overflow_risk(
                latest.fill_level,
                fill_rate
            )
        )

        priority_score = (
            calculate_priority(
                latest.fill_level,
                overflow_risk,
                b.battery
            )
        )

        results.append({

            "bin": b.bin_code,

            "fill_level": latest.fill_level,

            "hours": hours,

            "overflow_risk": overflow_risk,

            "priority_score": priority_score

        })

    results.sort(
        key=lambda x: x["priority_score"],
        reverse=True
    )

    return results