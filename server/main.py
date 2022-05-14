from fastapi import FastAPI
from fastconfig import routers

app = FastAPI()

app.include_router(routers.folder)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("serve:app", port=5000, reload=True)