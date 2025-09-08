
from aiohttp.web_exceptions import (
    HTTPConflict,
    HTTPNotFound,
    HTTPBadRequest,
    HTTPUnprocessableEntity,
)
from app.quiz.schemes import (
    ThemeSchema,
    ThemeListSchema,
    QuestionSchema,
    ListQuestionSchema,
    AnswerSchema,
)
from app.quiz.models import Answer
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response

class ThemeAddView(View, AuthRequiredMixin):
    async def post(self):
        self.require_auth()
        try:
            body = await self.request.json()
        except Exception:
            body = {}
        if "title" not in body:
            raise HTTPUnprocessableEntity(
                text='{"json": {"title": ["Missing data for required field."]}}'
            )
        title = body["title"]
        # uniqueness
        exists = await self.store.quizzes.get_theme_by_title(title)
        if exists:
            raise HTTPConflict()
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))

class ThemeListView(View, AuthRequiredMixin):
    async def get(self):
        self.require_auth()
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))

class QuestionAddView(View, AuthRequiredMixin):
    async def post(self):
        self.require_auth()
        try:
            body = await self.request.json()
        except Exception:
            body = {}
        required_fields = []
        for f in ("title", "theme_id", "answers"):
            if f not in body:
                required_fields.append(f)
        if required_fields:
            # For brevity, report first missing like tests expect
            field = required_fields[0]
            raise HTTPUnprocessableEntity(
                text='{"json": {"%s": ["Missing data for required field."]}}' % field
            )
        title = body["title"]
        theme_id = body["theme_id"]
        answers_payload = body["answers"]

        # answers must be a list with at least 2
        if not isinstance(answers_payload, list) or len(answers_payload) < 2:
            raise HTTPBadRequest()

        # theme must exist
        if await self.store.quizzes.get_theme_by_id(theme_id) is None:
            from aiohttp.web_exceptions import HTTPNotFound as NF
            raise HTTPNotFound()

        # unique question title
        if await self.store.quizzes.get_question_by_title(title) is not None:
            raise HTTPConflict()

        # validate answers entries
        answers = []
        correct_cnt = 0
        for a in answers_payload:
            if not isinstance(a, dict) or "title" not in a or "is_correct" not in a:
                raise HTTPBadRequest()
            ans = Answer(title=a["title"], is_correct=bool(a["is_correct"]))
            answers.append(ans)
            if ans.is_correct:
                correct_cnt += 1
        if correct_cnt == 0 or correct_cnt > 1:
            raise HTTPBadRequest()

        question = await self.store.quizzes.create_question(
            title=title, theme_id=theme_id, answers=answers
        )
        return json_response(data=QuestionSchema().dump(question))

class QuestionListView(View, AuthRequiredMixin):
    async def get(self):
        self.require_auth()
        theme_id = self.request.rel_url.query.get("theme_id")
        if theme_id is not None:
            try:
                theme_id = int(theme_id)
            except ValueError:
                theme_id = None
        questions = await self.store.quizzes.list_questions(theme_id=theme_id)
        return json_response(
            data=ListQuestionSchema().dump({"questions": questions})
        )
