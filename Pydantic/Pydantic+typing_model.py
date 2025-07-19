from pydantic import BaseModel
from typing import List, Dict, Optional

class Cart(BaseModel):
    user_id: int
    items: List[str]
    price: Dict[str, int]
    
class Blog(BaseModel):
    title: str
    content: str
    image: Optional[str] = None
    
Basket = {'user_id': 1, 'items':['Fresh Veggies', 'Organic Fruits', 'Instant Food', 'Drinks', 'Dairy Products', 'Bakery & Bread', 'Wheat & Cereals'], 
          'price':{'Fresh Veggies': 100, 'Organic Fruits': 200, 'Instant Food': 50, 'Drinks': 30, 'Dairy Products': 20, 'Bakery & Bread': 80,'Wheat & Cereals':150 }}

Med = {'title': 'Typing is a good Library in Python',
       'content':'Used typing library of python in pydantic to specify the type of the dictionary, list, tuples, and also use union and optional'}

blog = Blog(**Med)
cart = Cart(**Basket)

print(blog)
print(cart)