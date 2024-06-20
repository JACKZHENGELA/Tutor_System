from fastapi import Request
from beanie import Document


class Tutor(Document):
    name: str
    gpa: float
    subject: str
    gender: bool
    grade: int
    date: str
    email: str

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
