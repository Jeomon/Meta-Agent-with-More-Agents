from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional

class Agent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False}, min_length=3, max_length=50)
    description: str = Field(sa_column_kwargs={"nullable": False}, min_length=10, max_length=200)
    tools: str = Field(sa_column_kwargs={"nullable": False}, max_items=10)

class Tool(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False}, min_length=3, max_length=50)
    function_name: str = Field(sa_column_kwargs={"nullable": False}, min_length=3, max_length=50)
    description: str = Field(sa_column_kwargs={"nullable": False}, min_length=10, max_length=200)

class Query(BaseModel):
    query: str=Field(...,description="The query to be searched.")

class ToolDefinition(BaseModel):
    tool_definition: str=Field(...,description="The definition of the tool.")
