from aiohttp import web
from app.web.utils import json_response, error_json_response


class AddThemeView(web.View):
    async def post(self):
        data = await self.request.json()
        title = data.get("title")
        if not title:
            return error_json_response(
                http_status=400,
                status="bad_request",
                message="title is required",
                data={"title": ["Missing data."]}
            )

        theme = await self.store.quizzes.get_theme_by_title(title)
        if theme:
            raise web.HTTPConflict(reason="theme already exists")

        theme = await self.store.quizzes.create_theme(title)
        return json_response({"id": theme.id, "title": theme.title})


class ListThemesView(web.View):
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response({
            "themes": [{"id": theme.id, "title": theme.title} for theme in themes]
        })


class AddQuestionView(web.View):
    async def post(self):
        data = await self.request.json()
        title = data.get("title")
        theme_id = data.get("theme_id")
        answers = data.get("answers")

        if not title or not theme_id or not answers:
            return error_json_response(
                http_status=400,
                status="bad_request",
                message="title, theme_id and answers are required",
                data={"title": ["Missing data."] if not title else None,
                      "theme_id": ["Missing data."] if not theme_id else None,
                      "answers": ["Missing data."] if not answers else None}
            )

        # проверки
        if len(answers) < 2:
            return error_json_response(
                http_status=400,
                status="bad_request",
                message="question must have at least two answers",
                data={"answers": ["Too few answers."]}
            )
        if not any(ans.get("is_correct") for ans in answers):
            return error_json_response(
                http_status=400,
                status="bad_request",
                message="question must have at least one correct answer",
                data={"answers": ["No correct answer."]}
            )
        if sum(1 for ans in answers if ans.get("is_correct")) > 1:
            return error_json_response(
                http_status=400,
                status="bad_request",
                message="only one answer can be correct",
                data={"answers": ["Multiple correct answers."]}
            )

        theme = await self.store.quizzes.get_theme_by_id(theme_id)
        if not theme:
            raise web.HTTPNotFound(reason="theme not found")

        question = await self.store.quizzes.get_question_by_title(title)
        if question:
            raise web.HTTPConflict(reason="question already exists")

        question = await self.store.quizzes.create_question(title, theme_id, answers)
        return json_response({
            "id": question.id,
            "title": question.title,
            "theme_id": question.theme_id,
            "answers": [{"title": a.title, "is_correct": a.is_correct} for a in question.answers],
        })


class ListQuestionsView(web.View):
    async def get(self):
        theme_id = self.request.query.get("theme_id")
        questions = await self.store.quizzes.list_questions(theme_id)
        return json_response({
            "questions": [
                {
                    "id": q.id,
                    "title": q.title,
                    "theme_id": q.theme_id,
                    "answers": [{"title": a.title, "is_correct": a.is_correct} for a in q.answers],
                }
                for q in questions
            ]
        })
