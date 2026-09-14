from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80)
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6)
    )


class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=120)
    )
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )
    user_id = fields.Int(dump_only=True)
