from fastapi import *
from . import routers
from .core.database import models, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.config.router)
app.include_router(routers.permissions.router)

