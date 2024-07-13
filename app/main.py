from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# validation and schema set of payload send from Frontend
# if extra key values are send by FE, and pydentatic class does not have defined in it than it will show not that key. meaning extra key value pair aaje np
class Post(BaseModel):
    title: str
    content: str
    published: bool = True 

# class update_post(BaseModel):
#     title: str 
#     content: str

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres',
                            password='7087',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connected successfull')
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3)



# store posts in memory if application restart we will lose our data
cnt = 2
my_posts = [{"title":"Top beaches in florida", "content":"Checkout these awesome beaches","published":False,"id":1},
            {"title":"Top beaches in florida 2", "content":"Checkout these awesome beaches 2","published":False,"id":2}]


# routes aka path operations(decorator + function)
@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    cursor.execute(''' select * from post''')
    post = cursor.fetchall()
    # return {"message":"these are posts."}
    return {"data":post}


# @app.post("/create_post")
# def create_posts(payload: dict = (Body(...))): #retrived body raw data from postman
#     print(payload)
#     return {"message":f"new post created with title:{payload['title']} and content:{payload['content']}"}

@app.get("/posts/latest")
def get_latest_posts():
    if len(my_posts) <= 0:
        return {"message":"No post yet"}
    return {"data":my_posts[-1]}

# path parameters should come last as they could mistakely execute earlier for same http method. As path paramets follow top down approach
# path parameter included. if we are not specifing the datatype of path parameter explicitly than it will always be returned as str
@app.get("/posts/{post_id}")
def get_post_by_id(post_id:int, response: Response):
    # print(post_id, type(post_id))
    for item in my_posts:
        if item.get('id') == post_id:
            return item

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message":f"No post found with id = {post_id}"}     
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"No post found with id = {post_id}")

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post): #retrived body raw data from postman
    print(new_post.title.format())
    # new_post is a data type pydantic model and we can convert it into a dict
    # print(new_post.dict())
    # print(new_post.model_dump())
    # return {"data": new_post.model_dump()} # sending data back to FE
    global cnt 
    cnt = cnt + 1
    new_post_dict = new_post.model_dump()
    new_post_dict["id"] = cnt
    # print(new_post)
    my_posts.append(new_post_dict)
    return {"message":f"new post created with title:{new_post.title} and content:{new_post.content}"}

@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id:int, post_updated: Post):

    for index, post in enumerate(my_posts):
        if post["id"] == post_id:
            post_updated_dict = post_updated.model_dump()
            post_updated_dict['id'] = post_id
            my_posts[index] = post_updated_dict
            return {"detail": "Updated post successfull"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post exist for id:{post_id}")


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_post(post_id:int, ):
    for index, post in enumerate(my_posts):
        if post["id"] == post_id:
            del my_posts[index]
            # return {"message":"Post is successfully deleted"} do not return for deleting
            return Response(status_code= status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"No post exist for id: {post_id}")




# json is main language for API
# webserver is hosted on localhost:8000
# google http methods
# if both decorators have same name like / than first one in that file will take into effect. order matters of path operators
# browser send get method by default
# postman replaces webbrowser when we don't want frontend 
# post method: send some data to server
# documenation docs and redoc in localhost
# packages is fancy name of folder, it should contain __init__.py file which is empty. uvicorn app.main:app -> in app folder there is a main file that has our app 


# SQL
# delete from products where id = 8 returning * -> delete row will be returned
# insert into products(name, price) values ('Vape',1) returning id, name -> after inserting return inserted row

# post table
# create table post(
# 	id serial primary key,
# 	title varchar(255) not null,
# 	content text,
# 	published bool default false ,
# 	created_at timestamptz not null default now()
# )