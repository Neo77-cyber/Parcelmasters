from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
import random
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist




app = FastAPI()

SECRET_KEY = "dWd_sAxf65ED-6Yyfi6J0JnXM1tNtDmYa6rl479LlYg"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

password_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")   


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length = 100)
    password_hash = fields.CharField(max_length = 100)

    async def verify_password(self, plain_password):
        return password_context.hash(plain_password)
    
    class PydanticMeta:
        exclude = ["password_hash"]

STATUS_CHOICES = (
    ('awaiting payment', 'AWAITING PAYMENT'),
    ('consignment booked', 'CONSIGNMENT BOOKED'),
    (' delivery scheduled', 'DELIVERY SCHEDULED'),
    ('customs clearance', 'CUSTOMS CLEARANCE'),
    ('delay. temporary volume surge', 'DELAY. TEMPORARY VOLUME SURGE'),
    ('collected by customer at office', 'COLLECTED BY CUSTOMER AT OFFICE' )

)

DELIVERY_CHOICES = (
    ('food', 'FOOD'),
    ('phones', 'PHONES'),
    ('computer accessories', 'COMPUTER ACCESSORIES'),
    ('miscellaneous', 'MISCELLANEOUS')
)

class ShippingDetail(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    tracking_number = fields.IntField(blank=True, null=True)
    customer_name = fields.CharField(max_length=200)
    pickup_phone_number = fields.IntField()
    pickup_address = fields.CharField(max_length=200)
    recipient_name = fields.CharField(max_length=200)
    recipient_phone_number = fields.IntField()
    recipient_address = fields.CharField(max_length=200)
    category= fields.CharField(max_length=200, choices=DELIVERY_CHOICES, default = 'food')
    status = fields.CharField(max_length=100, choices=STATUS_CHOICES, default = 'awaiting payment', blank=True, null=True)

    

    def __str__(self) -> str:
        return str(self.tracking_number)

class ShippingDetailResponse(BaseModel):
    tracking_number: int
    customer_name: str
    pickup_phone_number: int
    pickup_address: str
    recipient_name: str
    recipient_phone_number: int
    recipient_address: str
    category: str
    status: str


register_tortoise(
    app,
    db_url='sqlite:///Users/neo/Documents/Codez/FASTApipractice/parcelfastapi/database.db',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True,
)

async def get_user(username: str):
    return await User.get_or_none(username=username)


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def authenticate_user(user:User, password: str):
    if not user or not verify_password(password, user.password_hash):
        return False
    else:
        return user
    
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post('/register')
async def register(username:str, password:str):
    existing_user = await get_user(username)
    if existing_user:
        raise HTTPException(status_code = 400, detail = 'Username already exists')
    hashed_password = password_context.hash(password)
    user = await User.create(username=username, password_hash = hashed_password)
    return {"message": "Registered successfuly"}

@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

    
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        return {"message": "Protected route accessed successfully."}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    
@app.post("/shipping-create", response_model=ShippingDetailResponse)
async def create_shipping_details(shipping_details:ShippingDetailResponse, token:str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get("sub")
            user = await get_user(username)
            print(user)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid token.")
            
            tracking_number = random.randint(100000, 999999)
            
            new_shipment = await ShippingDetail.create(user=user,
            tracking_number=tracking_number,
            customer_name=shipping_details.customer_name,
            pickup_phone_number=shipping_details.pickup_phone_number,
            pickup_address=shipping_details.pickup_address,
            recipient_name=shipping_details.recipient_name,
            recipient_phone_number=shipping_details.recipient_phone_number,
            recipient_address=shipping_details.recipient_address,
            category=shipping_details.category,
            status=shipping_details.status)

            response = ShippingDetailResponse(
            tracking_number=new_shipment.tracking_number,
            customer_name=new_shipment.customer_name,
            pickup_phone_number=new_shipment.pickup_phone_number,
            pickup_address=new_shipment.pickup_address,
            recipient_name=new_shipment.recipient_name,
            recipient_phone_number=new_shipment.recipient_phone_number,
            recipient_address=new_shipment.recipient_address,
            category=new_shipment.category,
            status=new_shipment.status
                )


            return response
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token.")
        
@app.get("/search")
async def search(query: str):
    
    try:

        result =  await ShippingDetail.filter(tracking_number__icontains=query)
        return result

    except DoesNotExist:
        raise HTTPException(status_code=404, detail='Task not found')
    


        
@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

    
        

    






