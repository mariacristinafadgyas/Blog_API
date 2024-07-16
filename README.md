# Blog API

A simple RESTful API for managing blog posts. This API allows users to create, read, update, delete, and search blog posts.

## Features

- **Create** a new blog post
- **Retrieve** all blog posts with optional sorting
- **Update** an existing blog post
- **Delete** a blog post by ID
- **Search** for blog posts by title, content, author, or date

## Technologies Used

- Python
- Flask
- JSON for data storage
- Swagger for API documentation

## Installation

1. Clone the repository:
```
   git clone https://github.com/mariacristinafadgyas/Blog_API
   cd Blog_API
```
2. Create and activate a virtual environment:
```
python3 -m venv venv
```
```
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```
3. Install the required packages:
```
   pip install -r requirements.txt
```

4. Run the application:
```
   python backend/backend_app.py
```
```
   python frontend/frontend_app.py
```
The API for the frontend will be available at http://localhost:5001, and the backend will be available at http://localhost:5002.

## API Endpoints
1. **Get All Posts**
- Endpoint: **/api/posts**
- Method: **GET**
- Query Parameters:
    - `sort`: attribute for sorting based on the following options: `title`, `content`, `author` or `post_date`
    - `direction`: attribute for sorting direction based on the following options: `asc`, `desc`
  
2. **Create a Post**
- Endpoint: **/api/posts**
- Method: **POST**
- Request Body:
```
{
  "title": "Post Title",
  "content": "Post content goes here.",
   "author": "Jane Doe"
}
```
3. **Update a Post**
- Endpoint: **/api/posts/<int:id>**
- Method: **PUT**
- Request Body:
```
{
  "title": "Updated Title",
  "content": "Updated content goes here."
}
```
4. **Delete a Post**
- Endpoint: **/api/posts/<int:id>**
- Method: **DELETE**
5. **Search Posts**
- Endpoint: **/api/posts/search**
- Method: **GET**
- Query Parameters: `title`, `content`, `author`, `post_date`

## Testing with Postman
To test the API endpoints using **Postman**:

- Open Postman and create a new request.
- Set the request type (**GET, POST, PUT, DELETE**) and enter the URL, for example: http://localhost:5002/api/posts.
- For endpoints that require a request body (**POST, PUT**), select the Body tab, choose raw, and set the type to JSON. Enter the request body as shown in the examples above.
- Send the request and check the response.

## Testing with Swagger
To test the API endpoints using **Swagger**:

- Start the backend server:
- Open your web browser and go to http://localhost:5002/api/docs/#/ .
- You will see the Swagger UI with the available endpoints and their documentation. 
- Click on an endpoint to expand its details, fill in the required parameters, and click the Try it out button to execute the request.

