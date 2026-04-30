
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastmcp import FastMCP

app = FastAPI()
scheduler = FastMCP()

class Task(BaseModel):
    name: str
    hours: int
    minutes: int 
    priority: int 
    deadline: str

class ScheduleRequest(BaseModel):
    tasks: List[Task]
    daily_hours: int

@app.post("/generate_schedule")
def generate_schedule(req: ScheduleRequest):
    result = scheduler.create_schedule([task.dict() for task in req.tasks], req.daily_hours)
    return result
