from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import func

from app.core.database import get_db

from app.models.bin import Bin
from app.models.alert import Alert

router = APIRouter(prefix="/api")


@router.get("/stats")
def stats(db: Session = Depends(get_db)):

    total_bins = db.query(Bin).count()

    full_bins = (
        db.query(Bin)
        .filter(Bin.fill_level >= 80)
        .count()
    )

    alerts = (
        db.query(Alert)
        .filter(Alert.status == "ACTIVE")
        .count()
    )

    total_weight = (
        db.query(func.sum(Bin.weight))
        .scalar()
        or 0
    )

    return {
        "total_bins": total_bins,
        "full_bins": full_bins,
        "alerts": alerts,
        "collected": round(total_weight, 2)
    }