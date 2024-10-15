E-commerce API:
This project is a fully functional E-commerce Product API built with Django and Django REST Framework (DRF). The API allows users to manage products, perform CRUD operations, manage user authentication, and handle advanced features like product reviews, wishlists, and order systems. It’s designed for e-commerce applications where products can be searched, categorized, reviewed, and purchased.


Features
1. Product Management (CRUD)
Create, Read, Update, Delete operations for products.
Each product has fields like name, description, price, category, stock quantity, image URLs, and created date.
Stock management: Stock quantity is reduced when an order is placed.
Supports multiple product images.
2. User Management (CRUD)
User registration, login, and logout with JWT authentication.
Users can perform product-related actions if authenticated (manage products, reviews, and orders).
Supports password hashing and secure authentication.
3. Product Search and Filtering
Search products by name, category, and partial matches.
Pagination support for large product listings.
Filter products by category, price range, and stock availability.
4. Product Reviews
Authenticated users can submit reviews for products.
Retrieve all reviews for a product.
5. Wishlists
Authenticated users can add products to their wishlist.
Endpoints to view, add, and remove products from a wishlist.
6. Order System
Users can place orders for products.
Automatic stock management when an order is placed or marked as reserved.
7. Authentication with JWT
Token-based authentication using Simple JWT.
Access token and refresh token management.
Token expiration and refresh functionality.
8. Admin Panel
Full control over products, categories, users, orders, and reviews from the Django admin panel.
Admins can manage the stock, update product details, and handle user permissions.
9. Deployment
Ready to be deployed on platforms like Heroku or PythonAnywhere.

Installation
Prerequisites
Python 3.x
Django 4.x
Django REST Framework
PostgreSQL or MySQL (or SQLite for development)
Docker (Optional for containerization)

Steps
 1 Clone the repository:

git clone https://github.com/eeyueltesfaye/Alx_Capstone_Project/.git
cd Ecommerce_Api

 2 Create a virtual environment:

python -m venv .venv

 3 Activate the virtual environment:

On Windows:

.venv\Scripts\activate

On macOS/Linux:

source .venv/bin/activate

 4 Install dependencies:

pip install -r requirements.txt

 5 Set up environment variables:
Create a .env file in the root directory with the following keys:

SECRET_KEY=<your_secret_key>
DEBUG=True
DATABASE_URL=<your_database_url>

 6 Run migrations:

python manage.py migrate 

 7 Create a superuser for accessing the admin panel:

python manage.py createsuperuser

 8 Run the development server:

python manage.py runserver


API ENDPONINTS   

User Authentication
Registration
Endpoint: POST /users/register/
Description: Registers a new user.
Request:

json

{
    "email": "loz@gmail.com",
    "password": "loza90278@",
    "password_confirm": "loza90278@"
}
Response:

json

{
    "message": "User registered successfully!"
}

Login
Endpoint: POST /users/login/
Description: Logs in the user and returns JWT tokens.
Request:

json

{
    "email": "loz@gmail.com",
    "password": "loza90278@"
}
Response:

json

{
    "refresh": "refresh_token_value",
    "access": "access_token_value",
    "user_id": 19,
    "email": "loz@gmail.com"
}

Profiles
Create Profile
Endpoint: POST /users/profiles/
Description: Creates a user profile.
Request:

json

{
    "first_name": "abushe",
    "last_name": "tesfaye",
    "username": "abu22",
    "address": "BOLE, LL23",
    "country": "Ethiopia",
    "user": "19"
}

Retrieve All Profiles
Endpoint: GET /users/profiles/
Description: Retrieves all user profiles (authentication required).

Retrieve Specific Profile
Endpoint: GET /users/profiles/<int:pk>/
Description: Retrieves a specific profile by profile ID.

Update Profile
Endpoint: PUT /users/profiles/<int:pk>/ or PATCH /users/profiles/<int:pk>/
Description: Updates a specific profile.

Delete Profile
Endpoint: DELETE /users/profiles/<int:pk>/
Description: Deletes a specific profile.


Product Management
Retrieve All Products
Endpoint: GET /products/
Description: Retrieves a list of all products.

Create Product
Endpoint: POST /products/
Description: Creates a new product.
Request:

json

{
    "name": "Bluetooth Wireless Earbuds",
    "description": "Compact wireless earbuds with noise cancellation and 24-hour battery life.",
    "price": 129.99,
    "category": "Electronics",
    "stock_quantity": 50,
    "image_url": "https://example.com/images/bluetooth-earbuds.jpg",
    "created_by": 19
}
Update Product
Endpoint: PUT /products/{id}/ or PATCH /products/{id}/
Description: Updates a product by product ID.

Delete Product
Endpoint: DELETE /products/{id}/
Description: Deletes a product by product ID.


Search and Filtering
Search Products
Endpoint: GET /products/?search=wire
Description: Search for products using keywords.

Filter by Category
Endpoint: GET /products/?category=elec
Description: Filter products by category.

Filter by Stock Availability
Endpoint: GET /products/?stock_min=10&stock_max=100
Description: Filter products based on stock availability.

Categories
Create Category
Endpoint: POST /products/categories/
Request:

json

{
    "name": "Home Appliances",
    "description": "Devices designed to assist in household tasks."
}
Retrieve Categories
Endpoint: GET /products/categories/
Description: Retrieves all categories.

Update Category
Endpoint: PUT /products/categories/{id}/ or PATCH /products/categories/{id}/
Description: Updates a category.

Delete Category
Endpoint: DELETE /products/categories/{id}/
Description: Deletes a category.

Wishlist
Retrieve Wishlist
Endpoint: GET /products/wishlist/
Description: Retrieves the user's wishlist.

Add to Wishlist
Endpoint: POST /products/wishlist/add/
Request:

json

{
    "product_id": 2
}
Update Wishlist (Add/Remove)
Endpoint: POST /products/wishlist/update/
Request:

json

{
    "product_id": 3,
    "action": "add"  // or "remove"
}


Reviews
Retrieve Product Reviews
Endpoint: GET /products/{id}/reviews/list/
Description: Retrieves all reviews for a specific product.

Post a Review
Endpoint: POST /products/{id}/reviews/
Request:

json

{
    "rating": "5",
    "comment": "Best Product"
}
Update Review
Endpoint: PUT /products/{product_id}/reviews/{review_id}/update/

Delete Review
Endpoint: DELETE /products/{product_id}/reviews/{review_id}/delete/

Orders
Create Order
Endpoint: POST /orders/create/
Request:

json

{
    "items": [
        {
            "product": 3,
            "quantity": 2
        }
    ]
}
Response:

json

{
    "message": "Order created successfully!",
    "order_id": 10
}
Retrieve Orders
Endpoint: GET /orders/list/
Description: Retrieves all orders.

Retrieve Specific Order
Endpoint: GET /orders/{order_Id}/
Description: Retrieves a specific order by its ID.

Discounts
Create Discount
Endpoint: POST /products/discounts/create/
Request:

json

{
    "product_id": 1,
    "discount_percentage": 20,
    "start_date": "2024-10-10T00:00:00Z",
    "end_date": "2024-10-20T23:59:59Z"
}
Retrieve Discounts
Endpoint: GET /products/discounts/

Update Discount
Endpoint: PUT /products/discounts/update/{id}/

Delete Discount
Endpoint: DELETE /products/discounts/delete/{id}/

Upload Multiple Images
Upload Images
Endpoint: POST /products/product-images/
Request:

json

{
    "product_id": 3,
    "image_urls": [
        "https://example.com/image3.jpg",
        "https://example.com/image4.jpg"
    ]
}
Get All Images for a Product
Endpoint: GET /products/product-images/?product_id=<product_id>

Update an Image
Endpoint: PUT /products/product-images/{id}/

Delete an Image
Endpoint: DELETE /products/product-images/{id}/

Admin Access
After creating the superuser, you can access the Django admin panel to manage products, orders, users, and more.
Admin panel URL: /admin/

This API documentation provides clear examples and JSON payloads for interacting with the endpoints. Please refer to each section to see the exact details required for your requests.


Security Recommendations:

Set DEBUG=False in production.
Use a secure and random SECRET_KEY.
Ensure database credentials are stored securely.
Set appropriate JWT token lifetimes:

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}


Deployment

 1 Build and run the app with Docker(Optional):
bash
docker-compose up --build

 2 Heroku or pythonanywhere
Deploy the app on Heroku or pythonanywhere by following the official guide.



Authors
Eyuel Tesfaye 