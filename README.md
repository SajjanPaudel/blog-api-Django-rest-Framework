# blog-api-Django-rest-Framework

## Installation
After you cloned the repository, you want to create a virtual environment, so you have a clean python installation.
You can do this by running the command
```
python -m venv env
```

After this, it is necessary to activate the virtual environment, you can get more information about this [here](https://docs.python.org/3/tutorial/venv.html)

You can install all the required dependencies by running
```
pip install -r requirements.txt
```

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE.

In our case, we have one single resource, `blogs`, so we will use the following URLS - `api/v1/list/` and `api/v1//detail/<id>` for collections and elements, respectively:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
'List all the blog posts'     :'api/v1/list/',
'Detail View of selected blog':'api/v1/detail/<int:id>',
'Create anew blog'            :'api/v1/create',
'Update an existing blog '    :'api/v1/update/<int:id>',
'Delete a blog'               :'api/v1/delete/<int:id>',
'Get access Token'            :'api/v1/login',
'Register a new author'       :'api/v1/refreshtoken',

## Use
We can test the API using [Postman](https://www.postman.com/)

First, we have to start up Django's development server.
```
python manage.py runserver
```
Only authenticated users can use the Delete and update API services, for that reason if we try this:
```
http    http://127.0.0.1:8000/api/v1/create or
        http://127.0.0.1:8000/api/v1/update/<int:id> or 
        http://127.0.0.1:8000/api/v1/Delete/<int:id
```
we get:
```
{
    "detail": "Authentication credentials were not provided."
}
```
we can access without credentials:
```
http http://127.0.0.1:8000/api/v1/list/
we get the list of all blogs
```
{  "blog_title":  "hello",  "blog_summary  ":  "summary",  "blog_content":  "something" }
```

## Create users and Tokens

First we need to create a user, so we can log in
```
http POST http://127.0.0.1:8000/api/v1/register/  username="USERNAME" password="PASSWORD" password2="PASSWORD" email="email@email.com" first_name="FIRST NAME" last_name= "LAST NAME"
```

After we create an account we can use those credentials to get a token

To get a token first we need to request
```
http http://127.0.0.1:8000/api/v1/login/ username="username" password="password"
```
after that, we get the token
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA2MjIxLCJqdGkiOiJjNTNlNThmYjE4N2Q0YWY2YTE5MGNiMzhlNjU5ZmI0NSIsInVzZXJfaWQiOjN9.Csz-SgXoItUbT3RgB3zXhjA2DAv77hpYjqlgEMNAHps"
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time.
We can use the refresh token to request a need access token.

requesting new access token
```
http http://127.0.0.1:8000/api/v1/login/refresh/ refresh="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA"
```
and we will get a new access token
```
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA4Mjk1LCJqdGkiOiI4NGNhZmMzMmFiZDA0MDQ2YjZhMzFhZjJjMmRiNjUyYyIsInVzZXJfaWQiOjJ9.NJrs-sXnghAwcMsIWyCvE2RuGcQ3Hiu5p3vBmLkHSvM"
}
```
To filter the number of blogs, it has pagination support , by default it is 10 but you can request any maount by using limit
```
http http://127.0.0.1:8000/api/v1/list/?limit=50 for example 

The API has some restrictions:
-   The blogs are always associated with a creator (user who created it).
-   Only authenticated users may create, update and delete blogs.
-   Only the creator of a blog may update or delete it.
-   The API does allow unauthenticated requests but is limited to read only access.