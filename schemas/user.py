from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    username: str
    password: str    

    
    