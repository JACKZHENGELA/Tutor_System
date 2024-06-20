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


def get_all_names(tutors):
    response = []
    for tutor in tutors:
        if tutor.name not in response:
            response.append(tutor.name)
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
        subject=form.form_data["subject"],
        date=form.form_data["date"]
    )
    try:
        tutors = await Tutor.find(Tutor.subject == new_tutee.subject).to_list()
        res = []
        for tutor in tutors:
            res.append(tutor.name)
        print(res)
        print(new_tutee.name)
        if new_tutee.name not in res:
            await new_tutee.insert()
            return templates.TemplateResponse("form.html", {
                "request": request,
                "msg": "Success :)"
            })
        else:
            return templates.TemplateResponse("form.html", {
                "request": request,
                "msg": "You already signed up for this subject",
                "err": "You already signed up for this subject"
            })
    except Exception as err:
        return templates.TemplateResponse("form.html", {
            "request": request,
            "msg": "There is an error going on, please contact the organizer or try again later ;(",
            "err": err
        })


@router.get("/tutor/name", response_class=HTMLResponse)
async def get_tutee_by_name(request: Request):
    tutors_repeated = await Tutor.find().to_list()
    tutors = get_all_names(tutors=tutors_repeated)
    print(tutors)
    return templates.TemplateResponse("name.html", {
        "request": request,
        "tutors": tutors
    })


@router.get("/tutor/name/{tutor}", response_class=HTMLResponse)
async def get_registrations(request: Request, tutor: str):
    tutors = await Tutor.find(Tutor.name == tutor).to_list()
    return templates.TemplateResponse("personal_registration.html", {
        "request": request,
        "tutors": tutors
    })
