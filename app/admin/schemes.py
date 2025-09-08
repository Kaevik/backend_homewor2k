from marshmallow import Schema, fields

class AdminSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Email(required=True)
