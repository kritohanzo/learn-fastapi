from fastapi import FastAPI, Cookie, Response, Header, Request, HTTPException
from fastapi.responses import FileResponse
from models.calculate import Calculate
from models.user import User, UserCreate, LoginData
from models.feedback import Feedback
import uvicorn
from typing import Union, Annotated
from models.products import Product
from datetime import datetime
from random import shuffle
import json

app = FastAPI()


feedbacks = []

@app.get('/')
async def root():
    now = datetime.now()
    response = FileResponse('index.html', 200)
    response.set_cookie(key='last_visit', value=now)
    return response

@app.post('/calculate/')
async def calculator(numbers: Calculate):
    return {"answer": numbers.num1 + numbers.num2}

@app.get('/custom/')
async def custom():
    return {"message": "This is a custom message"}

@app.get('/users/')
async def get_users():
    user = User(id=1, name='John Doe', age=30)
    return user

@app.get('/users/{user_id}/')
async def get_user_by_id(user_id: int, limit: int = 10):
    print(limit)
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


@app.post('/feedback/')
async def send_feedback(feedback: Feedback):
    feedbacks.append(feedback.model_dump())
    return {"message": f"Feedback recieved. Thank you, {feedback.name}!"}

@app.get('/feedback/')
async def get_all_feedbacks():
    feedback = {i: data for i, data in enumerate(feedbacks)}
    return feedback

@app.post('/create_user/')
async def create_user(user: UserCreate):
    return user


sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

@app.get('/product/{product_id}', response_model=Product)
async def get_product_by_id(product_id: int):
    for product in sample_products:
        if product_id == product.get('product_id'):
            return Product(**product)
    return {"error": "Product not found"}

@app.get('/products/search/')
async def get_all_products(keyword: str, category: Union[str, None] = None, limit: Union[int, None] = None):
    response = []
    for product in sample_products:
        if limit:
            if len(response) >= limit:
                return response
        if category:
            if keyword in product.get('name') and category == product.get('category'):
                response.append(product)
        else:
            if keyword in product.get('name'):
                response.append(product)
    return response
        
sessions: dict = dict()
sample_user = {"username": "John", "password": "arbuz123"}
fake_users: list = [User(**sample_user)]

@app.post('/login/')
async def login(login_data: LoginData, response: Response):
    for user in fake_users:
        if user.username == login_data.username and user.password == login_data.password:
            session_token = [char for char in (login_data.username + login_data.password)]
            shuffle(session_token)
            session_token = "".join(session_token)
            sessions[session_token] = user
            response.set_cookie(key='session_token', value=session_token, httponly=True)
            return {"message": "куки установлены"}
    return {"message": "Invalid username or password"}

@app.get('/user/')
async def is_adult_user(session_token = Cookie()):
    user = sessions.get(session_token)
    if user:
        return user.dict()
    return {"message": "Unauthorized"}

@app.get("/items/")
async def read_items(user_agent: Annotated[Union[str, None], Header()] = None):
    return {"User-Agent": user_agent}

@app.get('/headers/')
async def get_headers(request: Request):
    if 'user-agent' not in request.headers or 'accept-language' not in request.headers:
        raise HTTPException(detail='Required headers not exists', status_code=400)
    if request.headers['accept-language'].split(',')[0] != "ru-RU" and request.headers['accept-language'].split(',')[0] != 'en-US':
        raise HTTPException(detail='Accept language must be ru-RU or en-US', status_code=400)
    return Response(
        content=json.dumps(
            {
                "User-Agent": request.headers['user-agent'],
                "Accept-Language": request.headers['accept-language']
            }
        ), status_code=200
    )

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, workers=3, reload=True)

