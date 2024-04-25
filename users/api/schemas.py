from marshmallow import Schema, ValidationError, fields, validates_schema


class GenderSchema(Schema):
    name = fields.Str(data_key="name")


class UserSchema(Schema):
    uuid = fields.UUID = fields.Str(data_key="uuid")
    external_id = fields.Integer(data_key="external_id")
    first_name = fields.Str(data_key="first_name")
    last_name = fields.Str(data_key="last_name")
    birthday = fields.Date(data_key="birthday")
    gender = fields.Nested(GenderSchema)
    email = fields.Str(data_key="email")
    phone_number = fields.Integer(data_key="phone_number")
    country_code = fields.Str(data_key="country_code")


class CreateUserSchema(Schema):
    first_name = fields.Str(data_key="first_name")
    last_name = fields.Str(data_key="last_name")
    birthday = fields.Date(data_key="birthday")
    gender = fields.Str(data_key="gender")
    email = fields.Email(data_key="email")
    phone_number = fields.Integer(data_key="phone_number")
    country_code = fields.Str(data_key="country_code")
    password = fields.Str(data_key="password")


class UpdateUserContactInfoSchema(Schema):
    email = fields.Email(required=False)
    phone_number = fields.Str(required=False)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if not data:
            raise ValidationError(
                message="email field or phone_number field is required"
            )
        return data
