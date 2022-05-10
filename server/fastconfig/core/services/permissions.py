from fastapi import Depends
from sqlalchemy.orm.session import Session
from ..dependencies import get_db
from ..schemas.permissions import Permission
from ..database import models


class PermissionService:
    def __init__(self, db: Session  = Depends(get_db)) -> None:
        self._db = db
    
    async def validate_async(self, perm_to_check: Permission):
        matched_names = self._db.query(models.App).filter(models.App.name.in_(perm_to_check.names)).all()
        print([m.__dict__ for m in matched_names])
    