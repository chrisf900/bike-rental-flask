class InvalidBikeStatusTransition(Exception):
    pass


class UserWithActiveTrip(Exception):
    pass


class UserWithNoActiveTrip(Exception):
    pass


class NoBikesAvailable(Exception):
    pass


class BikeNotFoundError(Exception):
    pass


class CountryNotFoundError(Exception):
    pass
