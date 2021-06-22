from typing import List

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    email: str


class Post(BaseModel):
    id: int
    user: User
    text: str


class Topic(BaseModel):
    id: int
    user: User
    title: str
    views: int
    project: str
    group: str
    posts: List[Post]
