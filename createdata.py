from datetime import datetime

from sqlalchemy.exc import IntegrityError

from database import db
from mobility.bike.core.models import (
    Bike,
    Country,
    Gender,
    PasswordHistory,
    PaymentMethod,
    User,
)
from mobility.bike.lib.constants import PaymentsMethodConstants


def create_data():
    bikes = []
    locations = [
        ["3381073970", "-33.4415519", "-70.6470148"],
        ["3459497772", "-33.4366359", "-70.6542890"],
        ["3459497768", "-33.4415519", "-70.6470148"],
        ["3459497770", "-33.4415519", "-70.6470148"],
        ["3459497771", "-33.4415519", "-70.6470148"],
        ["3459497776", "-33.4396813", "-70.6551948"],
        ["3459510456", "-33.4404569", "-70.6521895"],
        ["3459510457", "-33.4423277", "-70.6550342"],
        ["3645490045", "-33.4440988", "-70.6494970"],
        ["4448367824", "-33.4502150", "-70.6431184"],
        ["4453713400", "-33.4492146", "-70.6394576"],
        ["4454050773", "-33.4429179", "-70.6382056"],
        ["4785128463", "-33.4338480", "-70.6428022"],
        ["9945810627", "-33.4408197", "-70.6395907"],
        ["9945810628", "-33.4437817", "-70.6444457"],
        ["10687321845", "-33.4420055", "-70.6443417"],
    ]

    for location in locations:
        bikes.append(
            Bike(
                code=int(location[0]),
                model="BX-200E",
                is_active=True,
                last_lat=location[1],
                last_lon=location[2],
                created_at=datetime.now(),
            )
        )

    print(bikes)

    payment_methods = PaymentsMethodConstants.ALLOWED
    payment_method = [
        PaymentMethod(name=pm, created_at=datetime.now()) for pm in payment_methods
    ]

    gender = [Gender(name="Male"), Gender(name="Female")]

    country = Country(
        code="CL",
        name="Chile",
        timezone="America/Santiago",
        currency="CLP",
        status=True,
        locale="es_CL",
        language="Spanish",
        created_at=datetime.now(),
    )

    db.session.bulk_save_objects(bikes)
    db.session.bulk_save_objects(payment_method)
    db.session.bulk_save_objects(gender)
    db.session.add(country)
    db.session.commit()

    gender = db.session.query(Gender).filter_by(name="Male").scalar()

    user = User(
        first_name="admin",
        last_name="admin",
        email="admin@admin.com",
        phone_number=0,
        external_id=416000,
        birthday=datetime.strptime("2000-01-01", "%Y-%m-%d"),
        gender_id=gender.id,
        country_code="CL",
        created_at=datetime.now(),
    )
    db.session.add(user)
    db.session.flush()

    password_history = PasswordHistory(
        user_uuid=user.uuid,
        password="$2b$12$vw74xbVcnbsDelfYfM6h4.m1X5I/w2.J7UcZbu2n/Ut/3s8UP0kwW",
    )

    db.session.add(password_history)
    db.session.commit()
    print("[OK] Data Created")
    print("Admin User Created -> 416000:admin@admin.com:admin")

    try:
        create_data()
    except IntegrityError as e:
        print("[FAIL] ERROR:", e)
