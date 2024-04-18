from marshmallow import Schema, ValidationError, fields, validates
from marshmallow.validate import Regexp

from mobility.bike.lib.constants import PaymentsMethodConstants


class BikeSchema(Schema):
    uuid = fields.UUID = fields.Str(data_key="uuid")
    code = fields.Str(data_key="code")
    model = fields.Str(data_key="model")
    status = fields.Str(data_key="status")
    is_active = fields.Boolean(data_key="is_active")
    last_lat = fields.Decimal(data_key="last_lat")
    last_lon = fields.Decimal(data_key="last_lon")
    created_at = fields.DateTime(data_key="created_at")
    updated_at = fields.DateTime(data_key="updated_at")


class UserSchema(Schema):
    uuid = fields.UUID = fields.Str(data_key="uuid")
    external_id = fields.Integer(data_key="external_id")
    first_name = fields.Str(data_key="first_name")
    last_name = fields.Str(data_key="last_name")
    birthday = fields.Date(data_key="birthday")
    gender_id = fields.Integer(data_key="gender_id")
    email = fields.Str(data_key="email")
    phone_number = fields.Integer(data_key="phone_number")
    country_code = fields.String(data_key="country_code")
    created_at = fields.DateTime(data_key="created_at")
    updated_at = fields.DateTime(data_key="updated_at")


class GenderSchema(Schema):
    name = fields.Str(data_key="name")


class TripSchema(Schema):
    uuid = fields.UUID = fields.Str(data_key="uuid")
    user_uuid = fields.UUID = fields.Str(data_key="user_uuid")
    bike_uuid = fields.UUID = fields.Str(data_key="bike_uuid")
    start_time = fields.DateTime(data_key="start_time")
    end_time = fields.DateTime(data_key="end_time")
    start_lat = fields.Decimal(data_key="start_lat")
    start_lon = fields.Decimal(data_key="start_lon")
    end_lat = fields.Decimal(data_key="end_lat")
    end_lon = fields.Decimal(data_key="end_lon")
    time_used = fields.Time(data_key="time_used")
    fare = fields.Float(data_key="fare")
    payment_method_id = fields.Integer(data_key="payment_method_id")
    with_subscription = fields.Boolean(data_key="with_subscription")
    calorie = fields.Integer(data_key="calorie")
    created_at = fields.DateTime(data_key="created_at")
    updated_at = fields.DateTime(data_key="updated_at")


class CountrySchema(Schema):
    code = fields.Str(data_key="code")
    name = fields.Str(data_key="name")
    locale = fields.Str(data_key="locale")


class PaymentMethodSchema(Schema):
    name = fields.Str(data_key="name")


class UserBikeSchema(Schema):
    id = fields.Integer(data_key="id")
    name = fields.Str(data_key="name")
    created_at = fields.DateTime(data_key="created_at")


class UserTripSchema(Schema):
    uuid = fields.UUID = fields.Str(data_key="uuid")
    user_uuid = fields.UUID = fields.Str(data_key="user_uuid")
    start_time = fields.DateTime(data_key="start_time")
    end_time = fields.DateTime(data_key="end_time")
    start_lat = fields.Decimal(data_key="start_lat")
    start_lon = fields.Decimal(data_key="start_lon")
    end_lat = fields.Decimal(data_key="end_lat")
    end_lon = fields.Decimal(data_key="end_lon")
    time_used = fields.Time(data_key="time_used")
    fare = fields.Float(data_key="fare")
    payment_method = fields.Nested(PaymentMethodSchema)
    calorie = fields.Integer(data_key="calorie")
    with_subscription = fields.Boolean(data_key="with_subscription")


class SearchCoordinatesSchema(Schema):
    latitude = fields.String(
        required=True, validate=Regexp(r"^-?([1-8]?[1-9]|[1-9]0)\.{1}\d{1,9}")
    )
    longitude = fields.String(
        required=True, validate=Regexp(r"^-?([1-8]?[1-9]|[1-9]0)\.{1}\d{1,9}")
    )


class AddEndCoordinatesSchema(Schema):
    end_latitude = fields.String(
        required=True, validate=Regexp(r"^-?([1-8]?[1-9]|[1-9]0)\.{1}\d{1,9}")
    )
    end_longitude = fields.String(
        required=True, validate=Regexp(r"^-?([1-8]?[1-9]|[1-9]0)\.{1}\d{1,9}")
    )


class AddTripDataSchema(Schema):
    bike_code = fields.String(required=True)
    payment_method_name = fields.String(required=True)

    @validates("payment_method_name")
    def validate(self, value):
        if value not in PaymentsMethodConstants.ALLOWED:
            raise ValidationError(message=f"Payment method '{value}' not allowed")
        return value
