from fastapi import FastAPI, Cookie, Response, Header, Request, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.responses import FileResponse
from pydantic import Field
from models.calculate import Calculate
from models.user import User, UserCreate, LoginData
from models.feedback import Feedback
import uvicorn
from typing import Union, Annotated
from models.products import Product
from datetime import datetime, timedelta
from random import shuffle
import jwt
import json
from db.tools import SqliteTools
from models.models import TodoModel
import time

app = FastAPI()
# security = HTTPBasic()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# feedbacks = []

# @app.get('/')
# async def root():
#     now = datetime.now()
#     response = FileResponse('index.html', 200)
#     response.set_cookie(key='last_visit', value=now)
#     return response

# @app.post('/calculate/')
# async def calculator(numbers: Calculate):
#     return {"answer": numbers.num1 + numbers.num2}

# @app.get('/custom/')
# async def custom():
#     return {"message": "This is a custom message"}

# @app.get('/users/')
# async def get_users():
#     user = User(id=1, name='John Doe', age=30)
#     return user

# @app.get('/users/{user_id}/')
# async def get_user_by_id(user_id: int, limit: int = 10):
#     print(limit)
#     if user_id in fake_users:
#         return fake_users[user_id]
#     return {"error": "User not found"}


# @app.post('/feedback/')
# async def send_feedback(feedback: Feedback):
#     feedbacks.append(feedback.model_dump())
#     return {"message": f"Feedback recieved. Thank you, {feedback.name}!"}

# @app.get('/feedback/')
# async def get_all_feedbacks():
#     feedback = {i: data for i, data in enumerate(feedbacks)}
#     return feedback

# @app.post('/create_user/')
# async def create_user(user: UserCreate):
#     return user


# sample_product_1 = {
#     "product_id": 123,
#     "name": "Smartphone",
#     "category": "Electronics",
#     "price": 599.99
# }

# sample_product_2 = {
#     "product_id": 456,
#     "name": "Phone Case",
#     "category": "Accessories",
#     "price": 19.99
# }

# sample_product_3 = {
#     "product_id": 789,
#     "name": "Iphone",
#     "category": "Electronics",
#     "price": 1299.99
# }

# sample_product_4 = {
#     "product_id": 101,
#     "name": "Headphones",
#     "category": "Accessories",
#     "price": 99.99
# }

# sample_product_5 = {
#     "product_id": 202,
#     "name": "Smartwatch",
#     "category": "Electronics",
#     "price": 299.99
# }

# sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

# @app.get('/product/{product_id}', response_model=Product)
# async def get_product_by_id(product_id: int):
#     for product in sample_products:
#         if product_id == product.get('product_id'):
#             return Product(**product)
#     return {"error": "Product not found"}

# @app.get('/products/search/')
# async def get_all_products(keyword: str, category: Union[str, None] = None, limit: Union[int, None] = None):
#     response = []
#     for product in sample_products:
#         if limit:
#             if len(response) >= limit:
#                 return response
#         if category:
#             if keyword in product.get('name') and category == product.get('category'):
#                 response.append(product)
#         else:
#             if keyword in product.get('name'):
#                 response.append(product)
#     return response
        
sessions: dict = dict()

# @app.post('/login/')
# async def login(login_data: LoginData, response: Response):
#     for user in fake_users:
#         if user.username == login_data.username and user.password == login_data.password:
#             session_token = [char for char in (login_data.username + login_data.password)]
#             shuffle(session_token)
#             session_token = "".join(session_token)
#             sessions[session_token] = user
#             response.set_cookie(key='session_token', value=session_token, httponly=True)
#             return {"message": "куки установлены"}
#     return {"message": "Invalid username or password"}

# @app.get('/user/')
# async def is_adult_user(session_token = Cookie()):
#     user = sessions.get(session_token)
#     if user:
#         return user.dict()
#     return {"message": "Unauthorized"}

# @app.get("/items/")
# async def read_items(user_agent: Annotated[Union[str, None], Header()] = None):
#     return {"User-Agent": user_agent}

# @app.get('/headers/')
# async def get_headers(request: Request):
#     if 'user-agent' not in request.headers or 'accept-language' not in request.headers:
#         raise HTTPException(detail='Required headers not exists', status_code=400)
#     if request.headers['accept-language'].split(',')[0] != "ru-RU" and request.headers['accept-language'].split(',')[0] != 'en-US':
#         raise HTTPException(detail='Accept language must be ru-RU or en-US', status_code=400)
#     return Response(
#         content=json.dumps(
#             {
#                 "User-Agent": request.headers['user-agent'],
#                 "Accept-Language": request.headers['accept-language']
#             }
#         ), status_code=200
#     )

# async def get_user_from_db(username: str):
#     for user in fake_users:
#         if user.username == username:
#             return user
#     return None

# async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
#     user = get_user_from_db(credentials.username)
#     if not user or user.password != credentials.password:
#         raise HTTPException(status_code=401, detail="User not exists or credentials is invalid", headers={"WWW-Authenticate": "Basic"})
#     return user

# @app.get("/protected_resource/")
# async def get_protected_resource(user: User = Depends(authenticate_user)):
#     return {"message": "You have access to the protected resource!", "user_info": user}


# @app.get('/http_basic_login/')
# async def http_basic_login(user: User = Depends(authenticate_user)):
#     return {"message": "You got my secret, welcome"}

# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

# sample_user_1 = {"username": "John", "password": "arbuz123", "role": "admin"}
# sample_user_2 = {"username": "Artur", "password": "arbuz123"}
# fake_users: list = {
#     sample_user_1.get("username"): User(**sample_user_1),
#     sample_user_2.get("username"): User(**sample_user_2)
# }

# def get_user_from_db(username: str):
#     if username in fake_users:
#         return fake_users.get(username)
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# def check_password(user: User, password: str):
#     if not user.password == password:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password not valid")

# def create_jwt_token(username: str, expires_of_hours: int) -> dict:
#     return {"auth_token": jwt.encode({"sub": username, "exp": datetime.utcnow() + timedelta(hours=expires_of_hours)}, "TOPSECRET", "HS256")}

# def get_user_from_token(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, "TOPSECRET", "HS256", verify=True)
#         return get_user_from_db(payload.get("sub"))
#     except jwt.exceptions.DecodeError or jwt.exceptions.InvalidTokenError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid")
#     except jwt.exceptions.ExpiredSignatureError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    
# @app.post("/login/")
# async def login(login_data: LoginData) -> dict:
#     user = get_user_from_db(login_data.username)
#     check_password(user, login_data.password)
#     return create_jwt_token(login_data.username, login_data.expires_of_hours)

# @app.get("/admin_resource/")
# async def jwt_protected(current_user: Annotated[User, Depends(get_user_from_token)]):
#     if not current_user.role == "admin":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must be admin to access this")
#     return {"message": f"Congratulations, {current_user.username}! You win this admin resource!"}

# @app.get("/user_resource/")
# async def jwt_protected(current_user: Annotated[User, Depends(get_user_from_token)]):
#     return {"message": f"Congratulations, {current_user.username}! You win this user resource!"}


@app.get("/todo/{todo_id}/")
async def get_todo_by_id(todo_id: int):
    todo = await SqliteTools.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo

@app.post("/todo/")
async def create_todo(todo_data: TodoModel):
    todo = await SqliteTools.add_todo(todo_data.title, todo_data.description)
    return todo

@app.put("/todo/{todo_id}/")
async def update_todo_by_id(todo_id: int, todo_data: TodoModel):
    todo = await SqliteTools.update_todo_by_id(
        todo_id, todo_data.title, todo_data.description, todo_data.completed
    )
    return todo

@app.delete("/todo/{todo_id}/")
async def delete_todo_by_id(todo_id: int):
    deleted = await SqliteTools.delete_todo_by_id(todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

if __name__ == "__main__":
    SqliteTools.check_exists_db()
    uvicorn.run(
        app="main:app", host="127.0.0.1", port=8000, workers=3, reload=True
    )
