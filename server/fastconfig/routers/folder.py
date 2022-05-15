from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, Response
from ..dependencies import retrieve_token
from ..utils import Util

folder = APIRouter(dependencies=[Depends(retrieve_token)])

@folder.get("/{full_path:path}")
async def get_folder(request: Request, full_path: str, util: Util = Depends()):
    body = await request.body()
    if not body:
        request_json = ""
    else:
        request_json = await request.json()
    path = util.parse_path(full_path)
    res = await util.get_dict(path)
    return res


@folder.put("/{full_path:path}")
async def update_folder(request: Request, full_path: str, util: Util = Depends()):
    request_json = await request.json()
    location = util.parse_path(full_path)
    util.parse_dict(request_json, location)
    await util.put_dict(request_json, location)
    return

@folder.delete("/{full_path:path}")
async def update_folder(request: Request, full_path: str, util: Util = Depends()):
    location = util.parse_path(full_path)
    await util.delete(location)
    return