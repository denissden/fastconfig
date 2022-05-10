from fastapi import *
from ..core.dependencies import *
from ..core.schemas import Permission

router = APIRouter()


@router.post("/perm")
async def new_perm(perm: Permission, perm_service: PermissionService = Depends(PermissionService)):
    await perm_service.validate_async(perm)
    return perm