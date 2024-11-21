from sqlmodel import SQLModel, Field, Relationship
from typing import List
from datetime import datetime

class Agent(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False}, min_length=3, max_length=50)
    description: str = Field(sa_column_kwargs={"nullable": False}, min_length=10, max_length=200)
    tools: List["Tool"] = Relationship(back_populates="agent",sa_relationship_kwargs={"cascade": "save-update, merge"})

class Tool(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False}, min_length=3, max_length=50)
    function_name: str = Field(sa_column_kwargs={"nullable": False}, min_length=3, max_length=50)
    description: str = Field(sa_column_kwargs={"nullable": False}, min_length=10, max_length=200)
    agent_id:str = Field(foreign_key="agent.id",nullable=True)
    agent: Agent = Relationship(back_populates="tools")

class Integration(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False}, min_length=3, max_length=20)
    key: str = Field(sa_column_kwargs={"nullable": False}, min_length=3, max_length=50)

class Conversation(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    title: str
    messages: List["Message"] = Relationship(back_populates="conversation",sa_relationship_kwargs={'cascade':"all, delete"})

class Message(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    role: str=Field(...,description='The role of the message')
    content: str=Field(...,description='The content of the message')
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: str = Field(foreign_key="conversation.id")
    conversation: Conversation = Relationship(back_populates="messages")

class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False}, min_length=3)
    email: str = Field(sa_column_kwargs={"nullable": False}, min_length=3)
    password: str = Field(sa_column_kwargs={"nullable": False}, min_length=3)
    profile_image:str = Field(sa_column_kwargs={"nullable":True})
