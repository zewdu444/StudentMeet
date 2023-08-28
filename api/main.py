from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app =FastAPI(
    title="Student Meet API",
    description="API for Student Meet",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers= ["*"],
)

@app.get("/")
async def root():
  return {"meesage": "Welcome to Student Meet API please visit /docs for more information"}
