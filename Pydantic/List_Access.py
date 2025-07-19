from pydantic import BaseModel, ValidationError
from typing import List, Optional


class User(BaseModel):
    name: str
    age: Optional[int] = None 

try:
    user = User(name="Riya", age="twenty")  
except ValidationError as e:
    print("Validation Error:", e)

user_list: List[User] = [
    User(name="Riya", age=20),
    User(name="Smita", age=42),
    User(name="Richa"),
    User(name="Kapil", age=49)
]

for student in user_list:
    print(student.name)
    
for student in user_list:
    print(student.age)
    
