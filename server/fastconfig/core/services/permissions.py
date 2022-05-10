from typing import List, Dict
from fastapi import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy import select
from ..dependencies import get_db
from ..schemas.permissions import PermissionDTO, GroupInternal, PermissionInternal, PermissionKind
from ..database import models


class PermissionService:
    static_group = GroupInternal()

    def __init__(self, db: Session  = Depends(get_db)) -> None:
        self._db = db
    
    async def validate_async(self, perm_to_check: PermissionDTO):
        command = select(models.App).where(models.App.name.in_(perm_to_check.names))
        matched_names = await self._db.execute(command)
        print([m.__dict__ for m in matched_names.scalars()])
    
    @staticmethod
    def _dto_to_internal(dto: PermissionDTO) -> Dict[PermissionKind, PermissionInternal]:
        internals = dict()

        def name_to_int(name: str):
            return sum(ord(c) for c in name)

        for kind in dto.kinds:
            def get_names():
                return {name_to_int(n) for n in dto.names}

            internal = PermissionInternal(
                create= get_names() if 'c' in dto.access else None, 
                read= get_names() if 'r' in dto.access else None, 
                update= get_names() if 'u' in dto.access else None, 
                delete= get_names() if 'd' in dto.access else None 
            )
            internals[kind] = internal

        return internals

    def update(self, dto: PermissionDTO):
        perms_to_add = self._dto_to_internal(dto)
        for k, v in perms_to_add.items():
            self.static_group.add(k, v)
    
    def delete(self, dto: PermissionDTO):
        perms_to_remove = self._dto_to_internal(dto)
        for k, v in perms_to_remove.items():
            self.static_group.remove(k, v)