from werkzeug.exceptions import BadRequestKeyError


class InvalidGETRequest(BadRequestKeyError):
    pass


class CampaignDoesNotExist(BadRequestKeyError):
    pass
