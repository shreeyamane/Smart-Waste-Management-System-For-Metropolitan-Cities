from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from app.core.database import get_db

from app.services.ml_service import (
    get_predictions
)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/prediction")
async def prediction(
    request: Request,
    db: Session = Depends(get_db)
):

    predictions = get_predictions(db)

    return templates.TemplateResponse(
        request=request,
        name="prediction.html",
        context={
            "predictions": predictions
        }
    )