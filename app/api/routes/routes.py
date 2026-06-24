from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from app.core.database import get_db

from app.services.ai_route_service import (
    get_ai_priority_bins
)

from app.services.route_optimizer import (
    nearest_neighbor_route
)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/routes")
async def collection_routes(
    request: Request,
    db: Session = Depends(get_db)
):

    ai_bins = get_ai_priority_bins(db)

    selected_bins = [

        item["bin"]

        for item in ai_bins[:15]

    ]

    route_bins, total_distance = (
        nearest_neighbor_route(
            selected_bins
        )
    )

    coordinates = []

    for b in route_bins:

        coordinates.append({

            "bin_code": b.bin_code,

            "lat": b.latitude,

            "lng": b.longitude,

            "fill_level": b.fill_level

        })

    return templates.TemplateResponse(
        request=request,
        name="routes.html",
        context={

            "route_bins": ai_bins[:15],

            "coordinates": coordinates,

            "total_distance": total_distance

        }
    )