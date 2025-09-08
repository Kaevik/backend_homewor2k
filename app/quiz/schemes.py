
from marshmallow import Schema, fields

class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)

class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)

class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.List(fields.Nested(AnswerSchema), required=True)

class ThemeListSchema(Schema):
    themes = fields.List(fields.Nested(ThemeSchema), required=True)

class ThemeIdSchema(Schema):
    id = fields.Int(required=True)

class ListQuestionSchema(Schema):
    questions = fields.List(fields.Nested(QuestionSchema), required=True)
