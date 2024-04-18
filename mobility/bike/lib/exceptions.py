class InvalidBikeStatusTransition(Exception):
    pass


class UserWithActiveTrip(Exception):
    pass


class UserWithNoActiveTrip(Exception):
    pass


class NoBikesAvailable(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class BikeNotFoundError(Exception):
    pass
