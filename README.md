# Django Shopping Cart Project

Welcome to the Django Shopping Cart project! This project is aimed at providing a simple and efficient shopping cart system built with Django and Docker Compose.

## Table of Contents
- [Features](#features)
- [Setup](#setup)
- [Endpoints](#endpoints)
- [Authentication](#authentication)
- [Usage](#usage)

## Features

- Ability to view all products in the shopping cart, add or remove from it.
- Authentication is based on JWT, so shopping cart of each user is recognized based on user request.
- Use NGINX for serving static files.
- Docker Compose setup for easy deployment.

## Setup

To run this project locally, make sure you have Docker and Docker Compose installed on your system. Then, follow these steps:

1. Clone this repository:
`git clone https://github.com/faaraad/shopping_cart_project.git` 
`cd your-project`
2. Build and run the Docker containers:
`docker-compose build && docker-compose up`
3. Once the containers are up and running, you can access the application at `http://localhost`.


## Authentication

This project requires JWT token authentication to access the endpoints. You need to include the token in the request headers.

Example:
```
Authorization: Bearer <your_token_here>
```

## Endpoints
Use Postman or Swagger Doc of the APIs:


The following endpoints are available in this API:

For create user and authenticaton:
- **POST /api/user/create-user/**: create a user with username and password:
```bash
curl --location 'http://localhost/api/user/create-user/' \
--header 'Content-Type: application/json' \
--data '{
    "username":"user",
    "password":"password"
}'
```
---
For obtain jwt token and refresh it:
- **POST /api/authentication/login/**: login a user and obtain token for it:
```bash
curl --location 'http://localhost/api/authentication/login/' \
--header 'Content-Type: application/json' \
--data '{
    "username":"user",
    "password":"password"
}'
```
---
For getting product:
```bash
curl --location 'localhost:8000/api/payment/products'
```
And finally for working with shopping cart, which need to be authenticated:

**GET /api/payment/shopping_cart**: Retrieves all products in the shopping cart.
```bash
curl --location --request POST 'localhost:8000/api/payment/shopping_cart/add/1/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzNDUxNzg3LCJpYXQiOjE3MTM0NTE0ODcsImp0aSI6IjYwOTRjZDhmN2RkNzRhODQ4NGJlYzZlMjMwNjRlNTI4IiwidXNlcl9pZCI6MX0.luOwEca_OM8I-a48-glUR9ozGsxgfMR6rCM1iHYlcN0'
```
**POST /api/payment/shopping_cart/add/{product_id}**: Adds a product to the shopping cart.

3. **POST /api/payment/shopping_cart/add/{product_id}**: Removes a product from the shopping cart.
