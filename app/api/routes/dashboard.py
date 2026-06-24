from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from app.core.database import get_db
from app.models.bin import Bin

from app.services.dashboard_service import (
    get_dashboard_stats
)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/")
async def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    stats = get_dashboard_stats(db)

    bins = db.query(Bin).all()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            **stats,
            "bins": bins
        }
    )