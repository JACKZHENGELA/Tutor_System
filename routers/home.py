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
async def selection(request: Request):
    return templates.TemplateResponse("selection.html", {
        "request": request
    })


@router.get("/subjects", response_class=HTMLResponse)
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

@router.get("/tutor/add", response_class=HTMLResponse)
async def get_tutee_add(request: Request):
    return templates.TemplateResponse("form.html", {
        "request": request
    })

@router.post("/tutor/add", response_class=HTMLResponse)
async def create_tutor(request: Request):
    form = TutorForm(request=request)
    await form.create_form_data()

    # print(form.form_data)
    new_tutee = Tutor(
        name=form.form_data["name"],
        gpa=form.form_data["gpa"],
        gender=form.form_data["gender"],
        grade=form.form_data["grade"],
        subject=form.form_data["subject"]
    )
    try:
        await new_tutee.insert()
        return templates.TemplateResponse("form.html", {
            "request": request,
            "msg": "Success"
        })
    except Exception as err:
        return templates.TemplateResponse("form.html", {
            "request": request,
            "msg": "Error",
            "err": err
        })