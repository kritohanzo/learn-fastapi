from fastapi import FastAPI
from fastapi.responses import FileResponse
from models.calculate import Calculate
from models.user import User, UserCreate
from models.feedback import Feedback
import uvicorn
from models.products import Product

app = FastAPI()

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com", "age": 25},
    2: {"username": "jane_smith", "email": "jane@example.com", "age": 30},
}

feedbacks = []

@app.get('/')
async def root():
    response = FileResponse('index.html', 200)
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

@app.post('/user/')
async def is_adult_user(user: User):
    return user.model_dump() | {"is_adult": user.age >= 18}

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
async def get_all_products(keyword: str, category: str | None = None, limit: int | None = None):
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
        
if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, workers=3, reload=True)

