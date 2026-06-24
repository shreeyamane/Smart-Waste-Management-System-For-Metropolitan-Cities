from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes.bins import router as bins_router

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.routes import router as routes_router
from app.api.routes.prediction import router as prediction_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.dashboard_api import router as dashboard_api_router



app = FastAPI(
    title="Smart Waste Management"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)
app.include_router(bins_router)
app.include_router(dashboard_router)
app.include_router(analytics_router)
app.include_router(routes_router)
app.include_router(prediction_router)
app.include_router(alerts_router)
app.include_router(dashboard_api_router)