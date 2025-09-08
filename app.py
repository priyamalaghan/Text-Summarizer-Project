from fastapi import FastAPI #To create the FastAPI application
import uvicorn #Uvicorn is an ASGI (Asynchronous Server Gateway Interface) server implementation, use it to run your FastAPI app. Without Uvicorn (or another ASGI server like Hypercorn), your FastAPI app won’t be able to serve requests
import sys #lets you interact with the Python runtime environment (e.g., system arguments, exit, path management)
import os
#Jinja2Templates is a FastAPI utility to integrate Jinja2, a popular template engine.
#It helps you render HTML templates with dynamic data
from fastapi.templating import Jinja2Templates 
#FastAPI is built on Starlette, so you get all Starlette response classes.
#RedirectResponse is used to send an HTTP redirect to another URL.
from starlette.responses import RedirectResponse #RedirectResponse → Redirect users to another page.
from fastapi.responses import Response #Response → Send custom raw responses(text, HTML, bytes, JSON, etc.).
from src.textSummarizer.pipeline.prediction import PredictionPipeline

text:str = "What is Text Summarization"

#app will hold your whole API project.
app = FastAPI() #creates an instance of a FastAPI application       

#Summary of Flow
#You start the FastAPI server:
#bash -> uvicorn main:app --reload
#If you visit http://127.0.0.1:8000/, you will be redirected to the documentation page /docs.
#On /docs, you’ll see an interactive Swagger UI where you can test all your API endpoints.

#Below function defines an asynchronous function called index
@app.get("/", tags=["authentication"])
async def index():#async def means it can handle requests asynchronously (non-blocking). Whenever a request comes to /, FastAPI will call this function
    return RedirectResponse(url="/docs")#/docs is the FastAPI Swagger UI page, where you can test your API interactively.

#This is a FastAPI route decorator.
#If your FastAPI app is running at http://127.0.0.1:8000, going to http://127.0.0.1:8000/train will trigger this function
@app.get("/train")#It tells FastAPI:Whenever someone sends a GET request to the URL /train, run the function below.
async def training():
    try:
        os.system("python main.py")#os.system() runs a terminal command from Python.
        return Response("Training Successful!!")#It returns an HTTP response with the message:
    except Exception as e:
        return Response(f"Error Occurred! {e}")
    
#Summary
#Client POSTs to /predict with a query parameter named text.
#FastAPI calls predict_route(...) and injects that text value.
#Your PredictionPipeline instance runs predict(text) and returns a result.
#The result is sent back as the HTTP response
@app.post("/predict") #Binds it to HTTP POST → means only POST requests will trigger the function.
async def predict_route(text):
    try:
        obj = PredictionPipeline()
        text = obj.predict(text)
        return text
    except Exception as e:
        raise e

#This ensures the server only starts if you run that file directly.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

#host="0.0.0.0"
#"0.0.0.0" means the server will accept requests from all network interfaces (any IP address).
#Useful when running inside Docker or on a server where clients connect from outside.
#If you use "127.0.0.1" or "localhost", the server will only accept requests from the same computer.

#port=8080
#This tells Uvicorn on which port to listen.
#Example: If your server runs on your local machine, you can open http://localhost:8080 to access it.