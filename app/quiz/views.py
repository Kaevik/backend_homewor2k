from aiohttp.web_exceptions import HTTPUnauthorized, HTTPConflict, HTTPBadRequest, HTTPNotFound
from app.web.app import View
from app.web.utils import json_response
from app.quiz.models import Answer

def get_admin_id(request):
    session = request.cookies.get("session")
    if not session:
        raise HTTPUnauthorized()
    try:
        return int(session)
    except ValueError:
        raise HTTPUnauthorized()

class ThemeAddView(View):
    async def post(self):
        get_admin_id(self.request)
        title = (await self.request.json())["title"]
        exists = await self.store.quizzes.get_theme_by_title(title)
        if exists:
            raise HTTPConflict()
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data={"id": theme.id, "title": theme.title})

class ThemeListView(View):
    async def get(self):
        get_admin_id(self.request)
        themes = await self.store.quizzes.list_themes()
        return json_response(data={"themes": [{"id": t.id, "title": t.title} for t in themes]})

class QuestionAddView(View):
    async def post(self):
        get_admin_id(self.request)
        data = await self.request.json()
        title = data.get("title")
        theme_id = data.get("theme_id")
        answers_data = data.get("answers") or []

        if await self.store.quizzes.get_question_by_title(title):
            raise HTTPConflict()
        theme = await self.store.quizzes.get_theme_by_id(theme_id)
        if not theme:
            raise HTTPNotFound()

        if len(answers_data) < 2:
            raise HTTPBadRequest()

        answers = [Answer(title=a.get("title"), is_correct=bool(a.get("is_correct"))) for a in answers_data]
        num_correct = sum(1 for a in answers if a.is_correct)
        if num_correct == 0 or num_correct > 1:
            raise HTTPBadRequest()

        q = await self.store.quizzes.create_question(title=title, theme_id=theme_id, answers=answers)
        return json_response(data={
            "id": q.id,
            "title": q.title,
            "theme_id": q.theme_id,
            "answers": [{"title": a.title, "is_correct": a.is_correct} for a in q.answers],
        })

class QuestionListView(View):
    async def get(self):
        get_admin_id(self.request)
        theme_id_param = self.request.rel_url.query.get("theme_id")
        theme_id = int(theme_id_param) if theme_id_param is not None else None
        questions = await self.store.quizzes.list_questions(theme_id=theme_id)
        return json_response(data={
            "questions": [
                {
                    "id": q.id,
                    "title": q.title,
                    "theme_id": q.theme_id,
                    "answers": [{"title": a.title, "is_correct": a.is_correct} for a in q.answers],
                } for q in questions
            ]
        })
