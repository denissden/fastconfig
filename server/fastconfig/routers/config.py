from fastapi import *
from ..core.dependencies import *

router = APIRouter()


@router.get("/folder/{full_path:path}")
def get_folder(full_path: str, folders: FolderService = Depends(FolderService)):
    folders.create(full_path)