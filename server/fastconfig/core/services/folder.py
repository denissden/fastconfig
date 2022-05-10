from fastapi import Depends
from ..database import SessionLocal
from ..dependencies import get_db


FOLDER_SEP = '/'
class FolderService:
    def __init__(self, db: SessionLocal = Depends(get_db)) -> None:
        self._db = db
    
    def create(self, path: str):
        print(self.parse_path(path))

    
    @staticmethod
    def parse_path(path):
        return list(filter(None, path.split(FOLDER_SEP)))
