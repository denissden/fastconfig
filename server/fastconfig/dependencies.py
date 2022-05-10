from fastapi import Request, HTTPException

def get_token_header(request: Request):
    token = request.headers.get("token")
    if token is None:
        raise HTTPException(400, "no token header")
    return token