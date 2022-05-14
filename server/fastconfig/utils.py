from operator import rshift
import re
from tkinter.messagebox import NO
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.session import Session
from .dependencies import get_db
from .database import models

allowed_characters = re.compile("^[A-Za-z0-9_.-]+$")
def check_allowed_characters(string: str):
    return bool(allowed_characters)

class Util:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    @staticmethod
    def parse_path(url_path: str):
        parts = url_path.split("/")
        for p in parts:
            if not check_allowed_characters(p):
                raise HTTPException(400, f"Invalid path name: {p}")
        return list(filter(None, parts))
    
    async def get_item(self, name: str, parent_id: int = None) -> models.Item:
        command = select(models.Item).where(models.Item.name == name)
        if parent_id is not None:
            command = command.where(models.Item.parent_id == parent_id)
        result = await self.db.execute(command)
        print(command, name, parent_id)
        first = result.scalars().first()
        return first

        
    async def get_item_by_path(self, path: List[str] | str):
        if type(path) == str:
            path = self.parse_path(path)
        parent_id = None
        for p in path:
            item = await self.get_item(p, parent_id=parent_id)
            if item is None:
                return None
            parent_id = item.id
        return item
    
    async def get_children(self, item: models.Item):
        if item is None:
            return []
        command = select(models.Item).where(models.Item.id == item.id).options(selectinload(models.Item.children))
        print(command)
        result = await self.db.execute(command)
        item = result.scalars().first()
        if item is None: 
            return []
        return item.children
    
    async def get_children_recursive(self, root_item: models.Item):
        root_children = await self.get_children(root_item)

        if not root_children:
            return root_item.value

        result = dict()
        for c in root_children:
            result[c.name] = await self.get_children_recursive(c)
        
        return result
    
    async def get_path_tree(self, path: List[str]):
        root_item = await self.get_item_by_path(path)
        children = await self.get_children_recursive(root_item)
        res_dict = dict()

        return children
    
    async def create_item(self, name, value, parent_id = None):
        new_item = models.Item()
        new_item.name = name
        new_item.parent_id = parent_id
        new_item.value = value
        self.db.add(new_item)
        self.db.refresh(new_item)
        return new_item

    
    async def save_children_recursive(self, root_item: models.Item, child_dict):
        root_children = await self.get_children(root_item)
        root_children_names = set(c.name for c in root_children)
        
        for key, value in child_dict.items():
            if key not in root_children_names:
                item_value = None if type(value) == dict else value
                root_id = root_item.id if root_item is not None else None
                new_item = await self.create_item(key, item_value, root_id)
                await self.save_children_recursive(new_item, child_dict=value if type(value) == dict else dict())
                 

    async def save_dict_tree(self, dict_to_save, location: List[str] = None):
        root_item = await self.get_item_by_path(location)
        await self.save_children_recursive(root_item, dict_to_save)
        await self.db.commit()
    

    def parse_dict(self, dict_to_parse: dict, location: List[str] = None):
        if location is None:
            location = []
        for key, value in dict_to_parse.items():
            if type(value) == dict:
                print("/".join(location + [key]))
                self.parse_dict(value, location + [key])
            else:
                print("value " + str(value))