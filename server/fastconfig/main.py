from fastapi import *
from . import routers
from .core.database import models, engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.config.router, prefix='/config')
app.include_router(routers.folder.router, prefix='/folder')
app.include_router(routers.permissions.router, prefix='/perm')
app.include_router(routers.token.router, prefix='/token')

