import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv(".env")
ACCESS_EXPIRES = timedelta(minutes=int(os.environ["ACCESS_EXPIRES"]))
