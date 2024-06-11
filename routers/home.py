from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.tutees import Tutor, TutorForm

router = APIRouter(prefix="", tags=["Home"])
templates = Jinja2Templates(directory="templates")


def get_all_subjects(tutors):
    response = []
    for tutor in tutors:
        if tutor.subject not in response:
            response.append(tutor.subject)
    return response


@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    tutors = await Tutor.find().to_list()
    subjects = get_all_subjects(tutors=tutors)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "subjects": subjects
    })


@router.get("/subjects/{subject}", response_class=HTMLResponse)
async def get_subjects(request: Request, subject: str):
    tutors = await Tutor.find(Tutor.subject == subject).to_list()
    print(tutors)
    return templates.TemplateResponse("subject_detail.html", {
        "request": request,
        "tutors": tutors
    })