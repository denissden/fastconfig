from fastapi import *
from ..core.dependencies import *

router = APIRouter()

@router.post("/new/{entity_type}{full_path:path}")
def new_command(
    entity_type: str, 
    full_path: str, 
    name: str | None = None,
    token: str = Depends(get_token_header)):

    print(full_path, name, token)

@router.post("/{full_path:path}")
def post_command(full_path: str, name: str):
    print(full_path, name)


@router.put("/{full_path:path}")
def new_command(full_path: str, name: str):
    print(full_path, name)

@router.get("/{full_path:path}")
def new_command(full_path: str, name: str):
    print(full_path, name)

@router.delete("/{full_path:path}")
def new_command(full_path: str, name: str):
    print(full_path, name)