from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.alert import Alert

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/alerts")
async def alerts(
    request: Request,
    db: Session = Depends(get_db)
):

    alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="alerts.html",
        context={
            "alerts": alerts
        }
    )