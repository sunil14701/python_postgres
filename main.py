from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# validation and schema set of payload send from Frontend
# if extra key values are send by FE, and pydentatic class does not have defined in it than it will show not that key. meaning extra key value pair aaje np
class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
    location: Optional[int] = None

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
    # return {"message":"these are posts."}
    return {"data":my_posts}


# @app.post("/create_post")
# def create_posts(payload: dict = (Body(...))): #retrived body raw data from postman
#     print(payload)
#     return {"message":f"new post created with title:{payload['title']} and content:{payload['content']}"}

@app.get("/posts/latest")
def get_latest_posts():
    if len(my_posts) <= 0:
        return {"message":"No post yet"}
    return {"data":my_posts[-1]}

# path parameters should come last as they could mistakely execute earlier for same http method. so path paramets follow top down approach
# path parameter included. if we are not specifing the datatype of path parameter explicitly than it will always be returned as str
@app.get("/posts/{post_id}")
def get_post_by_id(post_id:int,):
    # print(post_id, type(post_id))
    for item in my_posts:
        if item.get('id') == post_id:
            return item

    return {"message":f"No post found with id = {post_id}"}


@app.post("/posts")
def create_posts(new_post: Post): #retrived body raw data from postman

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




# json is main language for API
# webserver is hosted on localhost:8000
# google http methods
# if both decorators have same name like / than first one in that file will take into effect. order matters of path operators
# browser send get method by default
# postman replaces webbrowser when we don't want frontend 
# post method: send some data to server