from sqlmodel import SQLModel, Field, Relationship
from typing import List
from uuid import uuid4,UUID
from datetime import datetime

class Agent(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False,description='The name of the agent', min_length=3, max_length=50)
    description: str = Field(nullable=False,description='The description of the agent', min_length=10, max_length=200)
    user_id:UUID = Field(foreign_key="user.id",nullable=False)
    tools: List["Tool"] = Relationship(back_populates="agent",sa_relationship_kwargs={"cascade": "save-update, merge"})
    user: 'User' = Relationship(back_populates="agents",sa_relationship_kwargs={'cascade':"save-update, merge"})

class Tool(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False,description='The name of the tool', min_length=3, max_length=50)
    function_name: str = Field(nullable=False,description='The function name of the tool', min_length=3, max_length=50)
    description: str = Field(nullable=False,description='The description of the tool', min_length=10, max_length=200)
    user_id:UUID = Field(foreign_key="user.id",nullable=False)
    agent_id:UUID = Field(foreign_key="agent.id",nullable=True)
    agent: Agent = Relationship(back_populates="tools")
    user: 'User' = Relationship(back_populates="tools",sa_relationship_kwargs={'cascade':"save-update, merge"})

class Integration(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False,description='The name of the integration', min_length=3, max_length=20)
    key: str = Field(nullable=False,description='The key of the integration', min_length=3, max_length=50)
    user_id:UUID = Field(foreign_key="user.id",nullable=False)
    user: 'User' = Relationship(back_populates="integrations",sa_relationship_kwargs={'cascade':"save-update, merge"})

class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str=Field(nullable=False,description='The title of the conversation')
    user_id:UUID = Field(foreign_key="user.id",nullable=False)
    messages: List["Message"] = Relationship(back_populates="conversation",sa_relationship_kwargs={'cascade':"save-update, merge"})
    user: 'User' = Relationship(back_populates="conversations",sa_relationship_kwargs={'cascade':"save-update, merge"})

class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    role: str=Field(nullable=False,description='The role of the message')
    content: str=Field(nullable=False,description='The content of the message')
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: UUID = Field(foreign_key="conversation.id")
    conversation: Conversation = Relationship(back_populates="messages")

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field(nullable=False,description='The first name of the user', min_length=3)
    last_name: str = Field(nullable=False,description='The last name of the user', min_length=3)
    email: str = Field(nullable=False,description='The email of the user', min_length=3)
    password: str = Field(nullable=False,description='The password of the user', min_length=8)
    profile_image:str = Field(nullable=True,description='The profile image of the user')
    agents:List[Agent]=Relationship(back_populates='user')
    tools:List[Tool]=Relationship(back_populates='user')
    integrations:List[Integration]=Relationship(back_populates='user')
    conversations:List[Conversation]=Relationship(back_populates='user')