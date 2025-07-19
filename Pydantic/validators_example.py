from pydantic import BaseModel, field_validator, model_validator, computed_field

class User(BaseModel):
    username = str
    
@field_validator('Username')
def username_length(cls, v):
    if len(v) < 4:
        raise ValueError("enter atleast 4 character")
    return v

# field validators have before running mode, they run before pydantic

class Signup_data(BaseModel):
    password: str
    confirm_pass: str
    
    @model_validator(mode='after')
    def pass_match(cls, value):
        if value.password != value.confirm_pass:
            raise ValueError('password is not matching')
        return value
    
class Product(BaseModel):
    price: float
    quantity: int
    
    @computed_field
    @property
    def total_price(self) -> float:
        return self.price * self.quantity