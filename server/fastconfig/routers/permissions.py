from fastapi import *
from ..core.dependencies import *
from ..core.schemas import PermissionDTO

router = APIRouter()


@router.post("/")
async def new_perm(perm: PermissionDTO, perm_service: PermissionService = Depends(PermissionService)):
    await perm_service.validate_async(perm)
    return perm

@router.post("/group")
def new_perm(perm: PermissionDTO, perm_service: PermissionService = Depends(PermissionService)):
    perm_service.update(perm)
    return perm_service.static_group

@router.delete("/group")
def new_perm(perm: PermissionDTO, perm_service: PermissionService = Depends(PermissionService)):
    perm_service.delete(perm)
    return perm_service.static_group