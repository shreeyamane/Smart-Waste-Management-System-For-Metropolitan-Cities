from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from app.core.database import get_db

from app.services.analytics_service import (
    get_analytics_data
)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/analytics")
async def analytics(
    request: Request,
    db: Session = Depends(get_db)
):

    analytics_data = get_analytics_data(db)

    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "request": request,

            "kpis": analytics_data["kpis"],

            "daily": analytics_data["daily"],
            "weekly": analytics_data["weekly"],
            "monthly": analytics_data["monthly"],

            "area": analytics_data["area"],

            "fill_distribution": analytics_data["fill_distribution"],

            "battery_distribution": analytics_data["battery_distribution"],

            "alerts": analytics_data["alerts"],

            "top_bins": analytics_data["top_bins"],

            "trend": analytics_data["trend"],

            "anomaly": analytics_data["anomaly"]
        }
    )