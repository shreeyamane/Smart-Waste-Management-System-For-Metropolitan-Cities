from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.bin import Bin
from app.models.alert import Alert


def get_dashboard_stats(db: Session):

    total_bins = db.query(Bin).count()

    full_bins = (
        db.query(Bin)
        .filter(Bin.fill_level >= 80)
        .count()
    )

    active_alerts = (
        db.query(Alert)
        .filter(Alert.status == "ACTIVE")
        .count()
    )

    total_waste = (
        db.query(
            func.sum(Bin.weight)
        ).scalar()
        or 0
    )

    return {
        "total_bins": total_bins,
        "full_bins": full_bins,
        "alerts": active_alerts,
        "collected": round(total_waste, 2)
    }