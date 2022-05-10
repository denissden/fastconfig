from __future__ import annotations
from typing import Dict, List, Optional, Set
from enum import Enum
from pydantic import BaseModel, validator, constr, Field


VALID_ACCESS_LETTERS = 'crud'

class PermissionKind(Enum):
    token = 'token'
    group = 'group'
    folder = 'folder'
    app = 'app'
    kv = 'kv'

class PermissionDTO(BaseModel):
    name: str
    kinds: List[PermissionKind]
    access: constr(to_lower=True)
    names: List[str] | None

    @validator('access')
    def access_must_be_crud(cls, v):
        valid = set(VALID_ACCESS_LETTERS)
        set_v = set(v)
        
        if len(valid.union(set_v)) > len(valid):
            raise ValueError(f"Invalid permission! Must be one of '{VALID_ACCESS_LETTERS}'") 

        return ''.join(set_v)


class PermissionInternal(BaseModel):
    create: Optional[Set[int]] = Field(default_factory=set)
    read: Optional[Set[int]] = Field(default_factory=set)
    update: Optional[Set[int]] = Field(default_factory=set)
    delete: Optional[Set[int]] = Field(default_factory=set)
    none: Optional[int] = None

    class Config:
        validate_assignment = True
        exclude_defaults = True
        exclude_none = True
    
    @validator('create', 'read', 'update', 'delete')
    def empty_set_if_none(cls, v):
        return v or set()

    def union(self, other: PermissionInternal) -> PermissionInternal:
        return PermissionInternal(
            create=self.create | other.create,
            read=self.read | other.read,
            update=self.update | other.update,
            delete=self.delete | other.delete
        )
    
    def difference(self, other: PermissionInternal) -> PermissionInternal:
        return PermissionInternal(
            create=self.create - other.create,
            read=self.read - other.read,
            update=self.update - other.update,
            delete=self.delete - other.delete
        )

    def union_with(self, other: PermissionInternal) -> PermissionInternal:
        self.create += other.create
        self.read += other.read
        self.update += other.update
        self.delete += other.delete
    
    def difference_with(self, other: PermissionInternal) -> PermissionInternal:
        self.create -= other.create
        self.read -= other.read
        self.update -= other.update
        self.delete -= other.delete
    
    def dict(self, *args, **kwargs) -> 'DictStrAny':
        """
        remove empty sets from json
        """
        exclude = set()
        for key, value in self.__dict__.items():
            if not value:
                exclude.add(key)
        kwargs['exclude'] = exclude
        return super().dict(*args, **kwargs)


class GroupInternal(BaseModel):
    permissions: Dict[PermissionKind, PermissionInternal] = Field(default_factory=dict)

    def _get(self, kind: PermissionKind) -> PermissionInternal:
        existing_perm = self.permissions.get(kind)
        if existing_perm is None:
            return PermissionInternal()
        return existing_perm
    
    def _get_or_create(self, kind: PermissionKind) -> PermissionInternal:
        if kind not in self.permissions:
            self.permissions[kind] = PermissionInternal()
        return self.permissions[kind]


    def add(self, kind: PermissionKind, permission: PermissionInternal):
        existing_perm = self._get(kind)
        self.permissions[kind] = existing_perm.union(permission)
    
    def remove(self, kind: PermissionKind, permission: PermissionInternal):
        existing_perm = self._get(kind)
        self.permissions[kind] = existing_perm.difference(permission)