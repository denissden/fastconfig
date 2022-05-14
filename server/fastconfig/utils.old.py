from enum import Enum
import json
from typing import Any, List
from fastapi import Depends, HTTPException
from .database import models
from .dependencies import get_db
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.session import Session

class OutputType(Enum):
    dict = "dict"
    model = "model"

class Util:
    def __init__(self, output_type: OutputType = OutputType.dict, db: Session = Depends(get_db)) -> None:
        self.db = db
        self.output_type = output_type
        print(output_type)
    
    async def create_folder(self, folder_name):
        # TODO: check if exists
        folder = models.Folder()
        folder.name = folder_name
        self.db.add(folder)
        await self.db.commit()
    
    async def create_kv(self, folder_name, key_name, value):
        folder = await self._get_folder(folder_name)
        kv = models.KeyValue()
        kv.folder_id = folder.id
        kv.name = key_name
        kv.value = value
        self.db.add(kv)
        await self.db.commit()

    async def get_all_folders(self):
        command = select(models.Folder).options(selectinload(models.Folder.kvs))
        folders = await self.db.execute(command)
        for f in folders.scalars():
            print(f.name)
            for kv in f.kvs:
                print("\t" + kv.name)
        return folders.scalars()

    async def _get_folder(self, folder_name: str, include_kvs: bool = False) -> models.Folder:
        command = select(models.Folder).where(models.Folder.name == folder_name)
        if include_kvs:
            command = command.options(selectinload(models.Folder.kvs))
        folders = await self.db.execute(command)
        folder, = folders.scalars()
        return folder
    
    async def get_folder(self, folder_name: str, include_kvs: bool = False):
        folder = await self._get_folder(folder_name, include_kvs)
        
        if self.output_type == OutputType.model:
            return folder
        
        if not include_kvs: 
            return folder

        res_dict = dict()
        for kv in folder.kvs:
            json_val = None
            try: 
                json_val = json.loads(kv.value)
            except Exception:
                pass
            res_dict[kv.name] = json_val
        return res_dict

    async def get_kv(self, folder_name: str, kv_name: str) -> models.KeyValue:
        folder = await self._get_folder(folder_name)
        command = (
            select(models.KeyValue)
            .where(models.KeyValue.folder_id == folder.id)
            .where(models.KeyValue.name == kv_name)
        )
        kvs = await self.db.execute(command)
        kv, = kvs.scalars()
        return kv