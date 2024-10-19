from pydantic import BaseModel, Field

class Node(BaseModel):
    proc: list[str] = Field(default_factory=list)
    func: list[str] = Field(default_factory=list)
    table: list[str] = Field(default_factory=list)