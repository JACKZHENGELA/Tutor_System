from datetime import datetime, timezone
from typing import Optional
from fastapi import Request
# from pydantic import BaseModel
from beanie import Document, Indexed


class Tutor(Document):
    name: str
    gpa: float
    subject: str
    gender: bool
    role: bool
    grade: int

    class Settings:
        name = "tutors"


class TutorForm:

    def __init__(self, request: Request):
        self.request: Request = request
        self.form_data = {}

    async def create_form_data(self):
        form = await self.request.form()
        for key, value in form.items():
            self.form_data[key] = value
