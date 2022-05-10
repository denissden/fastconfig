import imp
from multiprocessing.spawn import import_main_path
from fastconfig.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("serve:app", port=5000, reload=True)