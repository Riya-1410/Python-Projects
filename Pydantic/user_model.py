from pydantic import BaseModel

class user(BaseModel):
    id: int
    name: str
    is_active: bool
    
    
input = {'id':4, 'name':'Riya', 'is_active':True}

User = user(**input)
print(User)