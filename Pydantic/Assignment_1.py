# Create pydantic model with id, name, price, and in_stock details

from pydantic import BaseModel

class Model(BaseModel):
    id: int
    name: str
    price: int
    in_stock: bool
    
data = [{'id': 1, 'name': 'Esp32', 'price':500, 'in_stock':'True'},
        {'id': 2, 'name': 'Esp8266', 'price':900, 'in_stock':'False'}]

for n in data:
    model = Model(**n)
    print(model)