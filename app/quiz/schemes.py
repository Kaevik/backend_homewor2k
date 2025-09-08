from marshmallow import Schema, fields

class ThemeSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)

class AnswerSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)

class QuestionSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(AnswerSchema, many=True)
