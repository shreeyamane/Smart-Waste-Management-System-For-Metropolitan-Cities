# app/services/analytics_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd

from app.models.bin import Bin
from app.models.alert import Alert
from app.models.bin_reading import BinReading


def get_analytics_data(db: Session):

    bins = db.query(Bin).all()

    total_bins = len(bins)

    avg_fill = 0
    avg_battery = 0
    overflow_bins = 0

    if total_bins > 0:

        avg_fill = round(
            sum(b.fill_level for b in bins) / total_bins,
            2
        )

        avg_battery = round(
            sum(b.battery for b in bins) / total_bins,
            2
        )

        overflow_bins = len(
            [b for b in bins if b.fill_level >= 90]
        )

    total_alerts = db.query(Alert).count()

    readings = db.query(BinReading).all()

    if not readings:

        return {
            "kpis": {
                "avg_fill": avg_fill,
                "avg_battery": avg_battery,
                "overflow_bins": overflow_bins,
                "total_alerts": total_alerts,
                "waste_today": 0
            },
            "daily": {"labels": [], "values": []},
            "weekly": {"labels": [], "values": []},
            "monthly": {"labels": [], "values": []},
            "area": {"labels": [], "values": []},
            "fill_distribution": {"labels": [], "values": []},
            "battery_distribution": {"labels": [], "values": []},
            "alerts": {"labels": [], "values": []},
            "top_bins": {"labels": [], "values": []},
            "trend": "No Data",
            "anomaly": "No Data"
        }

    df = pd.DataFrame([
        {
            "bin_id": r.bin_id,
            "fill_level": r.fill_level,
            "weight": r.weight,
            "battery": r.battery,
            "created_at": r.created_at
        }
        for r in readings
    ])

    df["created_at"] = pd.to_datetime(df["created_at"])

    # -------------------
    # Daily Waste Trend
    # -------------------

    daily_df = (
        df.groupby(
            df["created_at"].dt.date
        )["weight"]
        .sum()
        .reset_index()
    )

    daily_labels = [
        str(x)
        for x in daily_df["created_at"]
    ]

    daily_values = [
        round(x, 2)
        for x in daily_df["weight"]
    ]

    # -------------------
    # Weekly Waste Trend
    # -------------------

    weekly_df = (
        df.groupby(
            df["created_at"].dt.strftime("%Y-W%U")
        )["weight"]
        .sum()
        .reset_index()
    )

    weekly_labels = weekly_df["created_at"].tolist()
    weekly_values = weekly_df["weight"].round(2).tolist()

    # -------------------
    # Monthly Waste Trend
    # -------------------

    monthly_df = (
        df.groupby(
            df["created_at"].dt.strftime("%Y-%m")
        )["weight"]
        .sum()
        .reset_index()
    )

    monthly_labels = monthly_df["created_at"].tolist()
    monthly_values = monthly_df["weight"].round(2).tolist()

    # -------------------
    # Area Wise Waste
    # -------------------

    area_labels = []
    area_values = []

    for b in bins:

        area_labels.append(b.location)
        area_values.append(round(b.weight, 2))

    # -------------------
    # Fill Distribution
    # -------------------

    fill_ranges = [
        0, 20, 40, 60, 80, 100
    ]

    fill_counts = pd.cut(
        df["fill_level"],
        bins=fill_ranges,
        include_lowest=True
    ).value_counts().sort_index()

    fill_labels = [
        str(x)
        for x in fill_counts.index
    ]

    fill_values = fill_counts.tolist()

    # -------------------
    # Battery Distribution
    # -------------------

    battery_counts = pd.cut(
        df["battery"],
        bins=fill_ranges,
        include_lowest=True
    ).value_counts().sort_index()

    battery_labels = [
        str(x)
        for x in battery_counts.index
    ]

    battery_values = battery_counts.tolist()

    # -------------------
    # Alert Distribution
    # -------------------

    alert_rows = (
        db.query(
            Alert.alert_type,
            func.count(Alert.id)
        )
        .group_by(Alert.alert_type)
        .all()
    )

    alert_labels = [
        x[0]
        for x in alert_rows
    ]

    alert_values = [
        x[1]
        for x in alert_rows
    ]

    # -------------------
    # Top 10 Full Bins
    # -------------------

    top_bins = sorted(
        bins,
        key=lambda x: x.fill_level,
        reverse=True
    )[:10]

    top_labels = [
        b.bin_code
        for b in top_bins
    ]

    top_values = [
        b.fill_level
        for b in top_bins
    ]

    # -------------------
    # Trend Detection
    # -------------------

    if len(daily_values) >= 2:

        if daily_values[-1] > daily_values[0]:
            trend = "Increasing"

        elif daily_values[-1] < daily_values[0]:
            trend = "Decreasing"

        else:
            trend = "Stable"

    else:
        trend = "Insufficient Data"

    # -------------------
    # Anomaly Detection
    # -------------------

    mean_weight = df["weight"].mean()
    std_weight = df["weight"].std()

    threshold = mean_weight + (2 * std_weight)

    anomalies = df[df["weight"] > threshold]

    anomaly_status = (
        f"{len(anomalies)} anomalies detected"
    )

    today = pd.Timestamp.now().date()

    waste_today = round(
        df[
            df["created_at"].dt.date == today
        ]["weight"].sum(),
        2
    )

    return {

        "kpis": {
            "avg_fill": avg_fill,
            "avg_battery": avg_battery,
            "overflow_bins": overflow_bins,
            "total_alerts": total_alerts,
            "waste_today": waste_today
        },

        "daily": {
            "labels": daily_labels,
            "values": daily_values
        },

        "weekly": {
            "labels": weekly_labels,
            "values": weekly_values
        },

        "monthly": {
            "labels": monthly_labels,
            "values": monthly_values
        },

        "area": {
            "labels": area_labels,
            "values": area_values
        },

        "fill_distribution": {
            "labels": fill_labels,
            "values": fill_values
        },

        "battery_distribution": {
            "labels": battery_labels,
            "values": battery_values
        },

        "alerts": {
            "labels": alert_labels,
            "values": alert_values
        },

        "top_bins": {
            "labels": top_labels,
            "values": top_values
        },

        "trend": trend,

        "anomaly": anomaly_status
    }