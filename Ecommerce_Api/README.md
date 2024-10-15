# Ecommerce Product Api

## Project Overview

This project is a fully functional E-commerce Product API built with Django and Django REST Framework (DRF). The API allows users to manage products, perform CRUD operations, manage user authentication, and handle advanced features like product reviews, wishlists, and order systems. It’s designed for e-commerce applications where products can be searched, categorized, reviewed, and purchased.

## Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)



## Features
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

## Installation
Prerequisites
Python 3.x
Django 4.x
Django REST Framework
PostgreSQL or MySQL (or SQLite for development)
Docker (Optional for containerization)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/eeyueltesfaye/Alx_Capstone_Project.git
   cd Ecommerce_Api
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   - On Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

4. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```
5. **Set up environment variable**:
Create a .env file in the root directory with the following keys:

 ```bash
  SECRET_KEY=<your_secret_key>
DEBUG=True
DATABASE_URL=<your_database_url>
   ```
6. **Run migrations**:

   ```bash
   python manage.py migrate
   ```
 7. **Create a superuser for accessing the admin panel**:

 ```bash
  python manage.py createsuperuser
   ```

8. **Run the development server** 

   ```bash
   python manage.py runserver
   ```

## Configuration

1. **Environment Variables**: Set up the required environment variables, such as `SECRET_KEY`, `DEBUG`, and database settings.
2. **Settings**: Update the `settings.py` file to configure installed apps, middleware, and authentication backends as necessary.

## Usage

1. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

2. **Access the API**: Open a web browser or an API client (like Postman) and navigate to:

   ```web
   http://127.0.0.1:8000/products/
   ```

3. **URL Roots**

**register**: `http://127.0.0.1:8000/users/register/` # User registration

**login**: `http://127.0.0.1:8000/users/login/` # User login

**logout**: `http://127.0.0.1:8000/users/logout/` # User logout - Use refresh token

**users**: `http://127.0.0.1:8000/users/` # View all users - Authentication required

**products**: `http://127.0.0.1:8000/products/` # View all products - Authentication required

**orders**: `http://127.0.0.1:8000/orders/list/` # View orders

**Token**`http://127.0.0.1:8000/api/token/refresh/` # Generate JWT token





## API Endpoints- use Curl or Postman for Testing 

```sql
## API Endpoints

| Method | Endpoint                                        | Description                                                    |
|--------|-------------------------------------------------|----------------------------------------------------------------|
| POST   | /users/register/                                | Allows a new user to create an account.                        |
| POST   | /users/login/                                   | Allows a user to login to their account.                       |
| POST   | /users/logout/                                  | Allows a user to logout from their account.                    |
|--------|-------------------------------------------------|----------------------------------------------------------------|
| POST   | /users/profiles/                                | Create a new profile for the logged-in user.                   |
| GET    | /users/profiles/                                | Retrieve a list of all profiles. (Authentication required)     |
| GET    | /users/profiles/{id}/                           | Retrieve a specific profile by its ID. (Authentication required)|
| PUT    | /users/profiles/{id}/                           | Update a specific profile. (Authentication required)           |
| DELETE | /users/profiles/{id}/                           | Delete a specific profile. (Authentication required)           |
|--------|-------------------------------------------------|----------------------------------------------------------------|
| GET    | /products/                                      | Retrieve a list of all products.                               |
| POST   | /products/                                      | Create a new product. (Admin Only)                             |
| GET    | /products/{id}/                                 | Retrieve a specific product by its ID.                         |
| PUT    | /products/{id}/                                 | Update a specific product. (Admin Only)                        |
| DELETE | /products/{id}/                                 | Delete a specific product. (Admin Only)                        |
| GET    | /products/?search={query}                       | Search products by name or category.                           |
| GET    | /products/?category={category_name}             | Filter products by category.                                   |
| GET    | /products/?stock_min={min}&stock_max={max}      | Filter products by stock availability.                         |
|--------|-------------------------------------------------|----------------------------------------------------------------|
| POST   | /products/categories/                           | Create a new product category. (Admin Only)                    |
| GET    | /products/categories/                           | Retrieve a list of all product categories.                     |
| PUT    | /products/categories/{id}/                      | Update a specific product category. (Admin Only)               |
| DELETE | /products/categories/{id}/                      | Delete a specific product category. (Admin Only)               |
|--------|-------------------------------------------------|----------------------------------------------------------------|
| GET    | /products/wishlist/                             | Retrieve a list of all wishlisted products.                    |
| POST   | /products/wishlist/add/                         | Add a product to the wishlist.                                 |
| POST   | /products/wishlist/update/                      | Add or remove a product from the wishlist.                     |
|--------|-------------------------------------------------|----------------------------------------------------------------|
| GET    | /products/{id}/reviews/list/                    | Retrieve all reviews for a specific product.                   |
| POST   | /products/{id}/reviews/                         | Post a review for a product.                                   |
| PUT    | /products/{product_id}/reviews/{review_id}/update/ | Update a specific review.                                      |
| DELETE | /products/{product_id}/reviews/{review_id}/delete/ | Delete a specific review.                                      |
|--------|-------------------------------------------------|----------------------------------------------------------------|
| POST   | /orders/create/                                 | Create a new order.                                            |
| GET    | /orders/list/                                   | Retrieve a list of all orders.                                 |
| GET    | /orders/{order_id}/                             | Retrieve a specific order by its ID.                           |
|--------|-------------------------------------------------|----------------------------------------------------------------|
| POST   | /products/discounts/create/                     | Create a discount for a product. (Admin Only)                  |
| GET    | /products/discounts/                            | Retrieve a list of all discounts.                              |
| PUT    | /products/discounts/{id}/                       | Update a specific discount. (Admin Only)                       |
| DELETE | /products/discounts/{id}/                       | Delete a specific discount. (Admin Only)                       |
|--------|-------------------------------------------------|----------------------------------------------------------------|
| POST   | /products/product-images/                       | Upload multiple images for a product.                          |
| GET    | /products/product-images/?product_id={id}       | Retrieve all images for a specific product.                    |
| PUT    | /products/product-images/{id}/                  | Update a specific product image.                               |
| DELETE | /products/product-images/{id}/                  | Delete a specific product image.                               |

```

- **Local Development URL**: `http://localhost:8000/`

---

## Authentication

### User Authentication (JWT)

1. **Create a new user**
   - **Method**: `POST`
   - **Endpoint**: `/users/register/`
   - **Body** (JSON):

```json
{
    "email": "loz@gmail.com",
    "password": "loza90278@",
    "password_confirm": "loza90278@"
}
```

- **Response** (JSON):

```json
     {
         "user": {
            "email": "loz@gmail.com"
         },
        {
    "message": "User registered successfully!"
}
     }
```

> **Note**: For future requests, include the access token in the Postman Authorization tab. Select Bearer Token as the type and paste the token into the field.
---

## API Endpoints

### 1. **Login**

- **Method**: `POST`
- **Endpoint**: `/users/login/`
- **Authorization**: `Bearer <access_token>`
- **Body** (JSON):

  ```json
  {
    "email": "loz@gmail.com",
    "password": "loza90278@"
}

- **Response** (JSON):

```json
  {
    "refresh": "refresh_token_value",
    "access": "access_token_value",
    "user_id": 19,
    "email": "loz@gmail.com"
}
```

### 2. **Creates a user profile**

**Note**: Authenticated Users

- **Method**: `POST`
- **Endpoint**: `/users/profiles/`
- **Authorization**: `Bearer <access_token>`
- **Body** (JSON):
- {
    "first_name": "abushe",
    "last_name": "tesfaye",
    "username": "abu22",
    "address": "BOLE, LL23",
    "country": "Ethiopia",
    "user": "19"
}


- **Response** (JSON):

```json
  {
    "first_name": "abushe",
    "last_name": "tesfaye",
    "username": "abu22",
    "address": "BOLE, LL23",
    "country": "Ethiopia",
    "user": "19"
}
```

### 3. **Create Products**

- **Method**: `POST`
- **Endpoint**: `/products/`
- **Authorization**: `Bearer <access_token>`
- **Body** (JSON):

  ```json
  {
    "name": "Bluetooth Wireless Earbuds",
    "description": "Compact wireless earbuds with noise cancellation and 24-hour battery life.",
    "price": 129.99,
    "category": "Electronics",
    "stock_quantity": 50,
    "image_url": "https://example.com/images/bluetooth-earbuds.jpg",
    "created_by": 19
}


- **Response** (JSON):

```json
 {
    "name": "Bluetooth Wireless Earbuds",
    "description": "Compact wireless earbuds with noise cancellation and 24-hour battery life.",
    "price": 129.99,
    "category": "Electronics",
    "stock_quantity": 50,
    "image_url": "https://example.com/images/bluetooth-earbuds.jpg",
    "created_by": 19
}
```

### 4. **Create an Order**

- **Method**: `POST`
- **Endpoint**: `/orders/create/`
- **Authorization**: `Bearer <access_token>`
- **Body** (JSON):

  ```json
  {
   "product_id": 1,
   "quantity": 2
}



- **Response** (JSON):

```json
{
   "order_id": 123,
   "product": "Wireless Mouse",
   "quantity": 2,
   "total_price": 59.98,
   "status": "pending"
}
```

### 5. **Add a Product to Wishlist**

- **Method**: `POST`
- **Endpoint**: `/products/wishlist/add/`
- **Authorization**: `Bearer <access_token>`
- **Body** (JSON):

  ```json
  {
   "product_id": 1
}



- **Response** (JSON):

```json
{
   "message": "Product added to wishlist",
   "wishlist": [
      {
         "product_id": 1,
         "name": "Wireless Mouse"
      }
   ]
}
```
### 6.Pagination
By default, API responses are paginated. You can control pagination using the query parameters:

?page=1: To get the first page
?page_size=10: To set the number of results per page


### 7.Advanced Filtering
You can filter products using query parameters such as price range, category, or availability.

Example URL to filter products by category: GET /products/?category=Electronics
## Additional Features

### Security Recommendations:
- Set DEBUG=False in production.
- Use a secure and random SECRET_KEY.
- Ensure database credentials are stored securely.
- Set appropriate JWT token lifetimes:
## Deployment

1 Build and run the app with Docker(Optional):
bash:
```bash
docker-compose up --build
```
2  2 Heroku or pythonanywhere
Deploy the app on Heroku or pythonanywhere by following the official guide.

## Authors
 Eyuel Tesfaye 
