from dataclasses import dataclass
from typing import List
from enum import Flag
from pydantic import BaseModel, validator


VALID_ACCESS_LETTERS = 'crud'

VALID_KINDS = ('token', 'group', 'folder', 'app', 'kv')
VALID_KIND_LETTERS = tuple(i[0] for i in VALID_KINDS)
MSG_KIND = \
"Invalid kind ('{0}')!" + \
f" Must be one of {str(VALID_KINDS)}" # + \
# f" or letters accordingly ('{''.join(VALID_KIND_LETTERS)}')"


class Permission(BaseModel):
    name: str
    kinds: List[str] | str
    access: str
    names: List[str] | None

    @validator('kinds')
    def kind_must_exist(cls, v):
        if type(v) == str:
            v = v.split(',')

        res = set()
        for kind in v:
            # TODO: kind letters
            if not kind or kind not in VALID_KINDS:
                raise ValueError(MSG_KIND.format(kind))
            res.add(kind.lower())

        return list(res)

    @validator('access')
    def access_must_be_crud(cls, v):
        valid = set(VALID_ACCESS_LETTERS)
        set_v = set(v.lower())
        
        if len(valid.union(set_v)) > len(valid):
            raise ValueError(f"Invalid permission! Must be one of '{VALID_ACCESS_LETTERS}'") 

        return ''.join(set_v)


class Group(BaseModel):
    name: str
    permissions: List[Permission]