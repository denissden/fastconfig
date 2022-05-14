import re
from tkinter.messagebox import NO
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.session import Session
from .dependencies import get_db
from .database import models

allowed_characters = re.compile("^[A-Za-z0-9_.-]+$")
def check_allowed_characters(string: str):
    return bool(allowed_characters)

class ItemCollection:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db
    
    async def get(self, name: str, parent_id: int = None, include_children: bool = False) -> models.Item | None: 
        command = (
            select(models.Item)
            .where(models.Item.name == name)
            .where(models.Item.parent_id == parent_id)
        )

        if include_children:
            command = command.options(selectinload(models.Item.children))

        result = await self.db.execute(command)
        first = result.scalars().first()
        return first
    
    async def get_children(self, id_: int) -> List[models.Item]:
        command = (
            select(models.Item)
            .where(models.Item.parent_id == id_)
        )

        result = await self.db.execute(command)

        return result.scalars().all()

    async def create(self, name: str, parent_id: int = None, value = None) -> models.Item:
        item = models.Item()
        item.name = name
        item.parent_id = parent_id
        item.value = value
        self.db.add(item)
        #self.db.refresh(item)
        await self.db.flush((item,))
        return item
    
    async def update(self, item: models.Item) -> None:
        self.db.refresh(item)
    
    async def delete(self, id_) -> None:
        command = delete(models.Item).where(models.Item.id == id_)
        print(command)
        await self.db.execute(command)

    async def commit(self) -> None:
        await self.db.commit()

    async def get_or_create(self, name: str, parent_id) -> models.Item:
        item = await self.get(name, parent_id)
        if item in None:
            item = self.create(name, parent_id)
        return item
    
    async def insert_or_update(self, name: str, parent_id: int = None, value = None) -> models.Item:
        item = await self.get(name, parent_id)
        if item is None:
            return await self.create(name, parent_id, value)
        else:
            item.value = value
            self.update(item)
            return item
    

class Util:
    def __init__(self, db: Session = Depends(get_db), items: ItemCollection = Depends()) -> None:
        self.db = db
        self.items = items

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
        item = None
        for p in path:
            item = await self.items.get(name=p, parent_id=parent_id)
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

    def parse_dict(self, dict_to_parse: dict, location: List[str] = None):
        if location is None:
            location = []
        for key, value in dict_to_parse.items():
            if type(value) == dict:
                print("/".join(location + [key]))
                self.parse_dict(value, location + [key])
            else:
                print("value " + str(value))
    
    async def put_dict_rec(self, dict_: dict, parent_id: int):
        for name, value in dict_.items():
            if name.startswith("__"):
                continue

            v = value
            is_dict = type(value) == dict
            if is_dict:
                v = None

            item = await self.items.insert_or_update(name, parent_id, v)

            print(item.__dict__.get('parent_id'), name)

            if is_dict:
                await self.put_dict_rec(value, item.id)
        
        # delete not updated entries
        if dict_.get("__delete") is True:
            print("delete", parent_id)
            children = await self.items.get_children(parent_id)
            do_not_delete = set(dict_.keys())
            delete = filter(lambda x: x.name not in do_not_delete, children)
            for d in delete:
                print(d.id, d.name)
                await self.items.delete(d.id)


    async def put_dict(self, dict_: dict, location: List[str] = None):
        parent_id = None
        if location is not None:
            item = await self.get_item_by_path(location)
            if item is not None:
                parent_id = item.id
        
        await self.put_dict_rec(dict_, parent_id)
        await self.items.commit()

    async def get_dict_rec(self, root_item: models.Item = None):
        id_ = None
        if root_item is not None:
            id_ = root_item.id
        children = await self.items.get_children(id_)

        if not children:
            return root_item.value

        dict_ = dict()
        for c in children:
            dict_[c.name] = await self.get_dict_rec(c)
        return dict_

    
    async def get_dict(self, location: List[str] = None):
        item = None
        if location is not None:
            item = await self.get_item_by_path(location)
        
        return await self.get_dict_rec(item)
        
        
            