from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.bin import Bin

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)

@router.get("/bins")
async def bins(
    request: Request,
    db: Session = Depends(get_db)
):

    bins_data = db.query(Bin).all()

    return templates.TemplateResponse(
        request=request,
        name="bins.html",
        context={
            "bins": bins_data
        }
    )