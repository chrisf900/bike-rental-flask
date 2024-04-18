from datetime import datetime

from database import db
from mobility.bike.lib.constants import BikeConstants
from mobility.bike.lib.exceptions import InvalidBikeStatusTransition


class BikeStatus:
    state_name = ""

    def __init__(self, bike, coords):
        self.bike = bike
        self.db = db
        self.coords = coords

    def new_state(self, state) -> None:
        self.__class__ = state

    def action(self, state) -> None:
        raise NotImplementedError()

    def __str__(self):
        return self.state_name

    def _set_status(self, new_status) -> None:
        """saves the new status in DB"""

        self.bike.status = new_status.state_name
        self.bike.updated_at = datetime.now()

        if self.coords and new_status.state_name == BikeConstants.AVAILABLE:
            self.bike.last_lat = self.coords.get("lat")
            self.bike.last_lon = self.coords.get("lon")

        self.db.session.commit()
        self.db.session.refresh(self.bike)


class Available(BikeStatus):
    state_name = BikeConstants.AVAILABLE

    def action(self, state):
        if state.state_name == BikeConstants.UNAVAILABLE:
            self._set_status(new_status=state)
            self.new_state(state)


class Unavailable(BikeStatus):
    state_name = BikeConstants.UNAVAILABLE

    def action(self, state):
        if state.state_name == BikeConstants.AVAILABLE:
            self._set_status(new_status=state)
            self.new_state(state)


class BikeStateMachine:
    def __init__(self, state, bike, coords=None):
        self.state = state(bike, coords)

    def change(self, state) -> None:
        self.state.action(state)


def get_state_class(state: str):
    if state == BikeConstants.AVAILABLE:
        return Available
    elif state == BikeConstants.UNAVAILABLE:
        return Unavailable
    else:
        raise InvalidBikeStatusTransition("{} status not valid".format(state))
